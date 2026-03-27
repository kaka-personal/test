import requests
import json
import os
from pathlib import Path

# Load token from .env or environment
# Note: In a real scenario, we'd use a more robust way to load .env
# For this script, we'll assume the environment has MSPBOTS_TOKEN
TOKEN = os.getenv("MSPBOTS_TOKEN")

def search_dataset_via_rag(requirements, top_k=5):
    """Search existing datasets on MSPbots platform using natural language."""
    url = "https://owlstg.mspbots.ai/owl-agent/api/v1/search_dataset_via_rag"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "mspbots_token": TOKEN,
        "requirements": requirements,
        "top_k": top_k
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def generate_dataset_via_chat(chat, thread_id=None):
    """Automatically create a dataset via chat."""
    url = "https://owlstg.mspbots.ai/owl-agent/api/v1/generate_dataset_via_chat"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "mspbots_token": TOKEN,
        "chat": chat
    }
    if thread_id:
        payload["thread_id"] = thread_id
        
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def dataset_data_preview(dataset_id, filter=None, order_by=None, order_fields=None, size=10, current=1):
    """Get a preview of the data content for a specified dataset."""
    url = f"https://app.mspbots.ai/web/query/sys/dataset/{dataset_id}/data"
    headers = {
        "token": TOKEN
    }
    params = {
        "size": size,
        "current": current
    }
    if filter:
        params["filter"] = filter
    if order_by:
        params["orderBy"] = order_by
    if order_fields:
        params["orderFields"] = order_fields
        
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="MSPBots Dataset API Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    # Search
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("requirements", help="Natural language requirements")
    search_parser.add_argument("--top_k", type=int, default=5)
    
    # Generate
    gen_parser = subparsers.add_parser("generate")
    gen_parser.add_argument("chat", help="Chat instruction")
    gen_parser.add_argument("--thread_id", help="Thread ID")
    
    # Preview
    prev_parser = subparsers.add_parser("preview")
    prev_parser.add_argument("dataset_id", help="Dataset ID")
    prev_parser.add_argument("--filter", help="SQL-style filter")
    prev_parser.add_argument("--size", type=int, default=10)
    prev_parser.add_argument("--current", type=int, default=1)
    
    args = parser.parse_args()
    
    if args.command == "search":
        print(json.dumps(search_dataset_via_rag(args.requirements, args.top_k), indent=2))
    elif args.command == "generate":
        print(json.dumps(generate_dataset_via_chat(args.chat, args.thread_id), indent=2))
    elif args.command == "preview":
        print(json.dumps(dataset_data_preview(args.dataset_id, args.filter, size=args.size, current=args.current), indent=2))
    else:
        parser.print_help()
