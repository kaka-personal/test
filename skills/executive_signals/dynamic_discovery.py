import json
import os
import subprocess
import time
from pathlib import Path

# --- Configuration ---
CACHE_FILE = Path("/app/workspace/skills/executive_signals/dataset_cache.json")
CACHE_TTL = 86400  # 24 hours

OWL_TOOL_PATH = "/app/workspace/skills/owl_mcp/call_tool.py"

# Signatures for Intent-Based Discovery
DATASET_SIGNATURES = {
    "PSA_TICKETS": {
        "query": "{psa} Ticket SLA",
        "must_contain": ["Ticket", "SLA"],
        "prefer": ["Live", "V2", "Data"],
        "avoid": ["Archive", "Legacy", "Test", "History"]
    },
    "FIN_INVOICES": {
        "query": "{psa} Agreement Recap",
        "must_contain": ["Agreement", "Recap"],
        "prefer": ["Manage", "V2"],
        "avoid": ["Detail", "Addition"]
    },
    "FIN_UNBILLED": {
        "query": "{psa} Time Entry",
        "must_contain": ["Time", "Entry"],
        "prefer": ["Layered", "Unbilled"],
        "avoid": ["Archive"]
    },
    "RMM_ALERTS": {
        "query": "Datto RMM Alerts", # RMM is often specific, can be dynamic too
        "must_contain": ["Alert"],
        "prefer": ["Lite", "Active"],
        "avoid": ["Archive"]
    },
    "COMPANY_TEAMS": {
        "query": "{psa} Company Team",
        "must_contain": ["Team"],
        "prefer": ["Member"],
        "avoid": []
    }
}

def call_owl_search(query):
    """Calls the Owl MCP search_dataset tool."""
    try:
        cmd = ["python3", OWL_TOOL_PATH, "search_dataset", json.dumps({"query": query, "top_k": 5})]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Search failed: {result.stderr}")
            return []
        
        # Parse the output. call_tool.py usually returns a JSON object.
        # We need to handle potentially wrapped responses.
        data = json.loads(result.stdout)
        
        # The tool might return { "result": [ ... ] } or just [ ... ] depending on implementation
        # Based on SKILL.md, it returns titles, URLs, snippets? No, that's web_search.
        # Owl MCP search_dataset returns a list of datasets.
        
        if isinstance(data, dict):
            if "content" in data and isinstance(data["content"], list):
                 # MCP standard response text? No, call_tool usually outputs the tool result directly.
                 pass
            if "result" in data:
                return data["result"]
            
        if isinstance(data, list):
            return data
            
        return []
    except Exception as e:
        print(f"Error calling Owl search: {e}")
        return []

def resolve_dataset_id(intent_name, psa_name="ConnectWise Manage"):
    """
    Resolves a dataset ID based on intent and PSA context.
    Uses caching to avoid frequent API calls.
    """
    # 1. Load Cache
    cache = {}
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
        except:
            cache = {}

    cache_key = f"{intent_name}:{psa_name}"
    
    # 2. Check Cache Validity
    if cache_key in cache:
        entry = cache[cache_key]
        if time.time() - entry['timestamp'] < CACHE_TTL:
            return entry['id']

    # 3. Perform Discovery
    if intent_name not in DATASET_SIGNATURES:
        raise ValueError(f"Unknown intent: {intent_name}")

    sig = DATASET_SIGNATURES[intent_name]
    
    # Format query with PSA name (e.g., "ConnectWise Manage Ticket SLA")
    # If the signature query doesn't use {psa}, it stays as is (e.g. RMM)
    search_query = sig["query"].format(psa=psa_name)
    
    print(f"🔍 Discovering dataset for '{intent_name}' using query: '{search_query}'...")
    results = call_owl_search(search_query)
    
    if not results:
        print(f"⚠️ No datasets found for {intent_name}. Using fallback or failing.")
        return None

    # 4. Scoring Logic
    best_match = None
    highest_score = -100

    for ds in results:
        score = 0
        name = ds.get('name', '')
        if not name and 'rag-content' in ds:
             # Fallback: Extract name from rag-content if available
             import re
             m = re.search(r"Dataset Name: (.*?)\\n", ds['rag-content'])
             if m: name = m.group(1)
        
        # Must contain
        if not all(k.lower() in name.lower() for k in sig["must_contain"]):
            continue

        # Avoid
        if any(k.lower() in name.lower() for k in sig["avoid"]):
            continue

        # Prefer (Bonus points)
        for p in sig["prefer"]:
            if p.lower() in name.lower():
                score += 10
        
        # Penalty for length (prefer concise names)
        score -= len(name) * 0.05

        if score > highest_score:
            highest_score = score
            best_match = ds

    if best_match:
        # Normalize ID key
        final_id = best_match.get('id') or best_match.get('dataset_id')
        print(f"✅ Resolved '{intent_name}' -> '{best_match.get('name', 'Unknown')}' (ID: {final_id})")
        
        # 5. Update Cache
        cache[cache_key] = {
            "id": final_id,
            "name": best_match.get('name', 'Unknown'),
            "timestamp": time.time()
        }
        
        # Ensure directory exists
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
            
        return final_id
    else:
        print(f"❌ No suitable match found for '{intent_name}' after filtering.")
        return None

if __name__ == "__main__":
    # Test run
    print("Testing dynamic discovery...")
    id = resolve_dataset_id("PSA_TICKETS", "ConnectWise Manage")
    print(f"Result: {id}")
