import requests
import sseclient
import json
import threading
import time
import sys
import argparse

# Configuration
MCP_URL = "https://owlstg.mspbots.ai/owl-mcp"
TOKEN = "Bearer 29:1Pj3svhFYJo65hFm0sRt8vIp4LMIMijIbev_L41dtj-hOpZ8-FxvdzssUcqFVCZDn8dZo_LroinHnYGCtx7F1Zw"

headers = {
    "Authorization": TOKEN,
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json"
}

def read_stream(response, event_store):
    """Reads SSE stream and stores relevant events."""
    client = sseclient.SSEClient(response)
    for event in client.events():
        # Store latest event of interest if needed, or log
        # For a tool call, we might get progress or log messages via stream
        pass

def call_tool(tool_name, tool_args):
    # 1. Initialize Session
    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "nanobot", "version": "1.0"}
        }
    }
    
    try:
        r_init = requests.post(MCP_URL, headers=headers, json=init_payload, stream=True)
        r_init.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to init session: {e}"}

    session_id = r_init.headers.get('mcp-session-id')
    if not session_id:
        return {"error": "No session ID returned"}

    # Update headers with session ID
    headers["mcp-session-id"] = session_id

    # Start stream reader in background to keep connection alive and drain buffer
    t = threading.Thread(target=read_stream, args=(r_init, {}))
    t.daemon = True
    t.start()
    
    # Wait briefly for init to settle
    time.sleep(1)

    # 2. Notify Initialized
    post_url = f"{MCP_URL}?sessionId={session_id}"
    requests.post(post_url, headers=headers, json={
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    })

    # 3. Call Tool
    call_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": tool_args
        }
    }
    
    try:
        r_call = requests.post(post_url, headers=headers, json=call_payload)
        r_call.raise_for_status()
        
        # Check if response is SSE format (starts with 'event:')
        if r_call.text.strip().startswith("event:"):
            # Extract data line
            for line in r_call.text.splitlines():
                if line.startswith("data:"):
                    json_str = line[5:].strip()
                    response_data = json.loads(json_str)
                    break
            else:
                return {"error": "Could not find data in SSE response", "raw": r_call.text}
        else:
            # Assume standard JSON
            response_data = r_call.json()
        
        if "error" in response_data:
            return {"error": response_data["error"]}
        
        if "result" in response_data:
            return response_data["result"]
            
        return response_data

    except Exception as e:
        return {"error": f"Tool call failed: {e}", "response": r_call.text if 'r_call' in locals() else "N/A"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Call an Owl MCP tool.")
    parser.add_argument("tool", help="Name of the tool to call")
    parser.add_argument("args", help="JSON string of arguments")
    
    args = parser.parse_args()
    
    try:
        arguments = json.loads(args.args)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON arguments"}))
        sys.exit(1)
        
    result = call_tool(args.tool, arguments)
    print(json.dumps(result, indent=2))
