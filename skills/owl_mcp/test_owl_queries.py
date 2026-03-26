import requests
import sseclient
import json
import threading
import time

MCP_URL = "https://owlstg.mspbots.ai/owl-mcp"
TOKEN = "Bearer 29:1x4mT5DGTUzDwIrn6zLbDOnEp7uxBdhgvTGHFdMTQ5F5Td8xThOcICOOXUTgTKEoNtTEhdmkqa-L5zRylVkQTDQ"

headers = {
    "Authorization": TOKEN,
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json"
}

def read_stream(response):
    client = sseclient.SSEClient(response)
    for event in client.events():
        pass # Just consume the stream to keep connection alive

def run_queries():
    print("--- Initializing Session ---")
    
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
    
    r_init = requests.post(MCP_URL, headers=headers, json=init_payload, stream=True)
    session_id = r_init.headers.get('mcp-session-id')
    
    if not session_id:
        print("No session ID returned.")
        return

    # Update headers with session ID
    headers["mcp-session-id"] = session_id
    
    post_url = f"{MCP_URL}?sessionId={session_id}"

    # Start reading the stream in background
    t = threading.Thread(target=read_stream, args=(r_init,))
    t.daemon = True
    t.start()
    
    time.sleep(1) 
    
    # Notify initialized
    requests.post(post_url, headers=headers, json={
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    })

    queries = [
        ("PSA", "ticket SLA queue priority customer"),
        ("Financial", "invoice accounts receivable agreement payment"),
        ("RMM", "alert backup patch device")
    ]

    for category, query in queries:
        print(f"\n--- Testing Category: {category} ---")
        print(f"Query: {query}")
        
        payload = {
            "jsonrpc": "2.0",
            "id": int(time.time()),
            "method": "tools/call",
            "params": {
                "name": "search_dataset",
                "arguments": {
                    "query": query,
                    "top_k": 3
                }
            }
        }
        
        try:
            # Construct the JSON-RPC payload for tool execution
            # Note: MCP spec says params should have "name" and "arguments"
            payload = {
                "jsonrpc": "2.0",
                "id": int(time.time()),
                "method": "tools/call",
                "params": {
                    "name": "search_dataset",
                    "arguments": {
                        "query": query,
                        "top_k": 5
                    }
                }
            }
            
            r = requests.post(post_url, headers=headers, json=payload)
            if r.status_code == 200:
                print(f"Response Status: {r.status_code}")
                # Parse the JSON response
                try:
                    resp_json = r.json()
                    if "result" in resp_json and "content" in resp_json["result"]:
                         # content is a list of objects with type='text' and text='...'
                         for item in resp_json["result"]["content"]:
                             if item.get("type") == "text":
                                 print(f"Result: {item.get('text')}")
                    else:
                        print(f"Raw Result: {json.dumps(resp_json, indent=2)}")
                except:
                    print(f"Raw Text: {r.text[:500]}")
            else:
                print(f"Error: {r.status_code} - {r.text}")
        except Exception as e:
            print(f"Exception: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    run_queries()
