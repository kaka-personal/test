import json
import subprocess
import sys

OWL_TOOL_PATH = "/app/workspace/skills/owl_mcp/call_tool.py"

def debug_search(query):
    print(f"DEBUG: Searching for '{query}'...")
    try:
        # Added top_k as required
        args = {"query": query, "top_k": 5}
        cmd = ["python3", OWL_TOOL_PATH, "search_dataset", json.dumps(args)]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("--- STDOUT ---")
        print(result.stdout)
        
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    debug_search("ConnectWise Manage Ticket SLA")
