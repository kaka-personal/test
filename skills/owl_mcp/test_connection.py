import sys
import json
import requests
import sseclient
import time

# Configuration
MCP_URL = "https://owlstg.mspbots.ai/owl-mcp"
TOKEN = "Bearer 29:1x4mT5DGTUzDwIrn6zLbDOnEp7uxBdhgvTGHFdMTQ5F5Td8xThOcICOOXUTgTKEoNtTEhdmkqa-L5zRylVkQTDQ"

headers = {
    "Authorization": TOKEN,
    "Accept": "text/event-stream"
}

def run_session():
    print(f"Connecting to SSE at {MCP_URL}...")
    try:
        # 1. Connect to SSE endpoint
        # Try base URL directly first
        response = requests.get(MCP_URL, headers=headers, stream=True)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response Body: {response.text}")
            return
        
        client = sseclient.SSEClient(response)
        
        endpoint_url = None
        session_id = None
        
        for event in client.events():
            # print(f"DEBUG: Event type={event.event}, data={event.data}")
            
            if event.event == "endpoint":
                endpoint_path = event.data
                print(f"Endpoint received: {endpoint_path}")
                
                # Construct full POST URL
                # If the path is relative, append to base URL
                if endpoint_path.startswith("/"):
                     endpoint_url = f"{MCP_URL}{endpoint_path}"
                else:
                     endpoint_url = endpoint_path # Assume absolute if not starting with /
                
                print(f"Initializing via POST to {endpoint_url}...")
                
                # 2. Send Initialize Request
                # JSON-RPC 2.0
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
                
                post_headers = {
                    "Authorization": TOKEN,
                    "Content-Type": "application/json"
                }
                
                r = requests.post(endpoint_url, headers=post_headers, json=init_payload)
                print(f"Init response: {r.status_code}")
                print(f"Init body: {r.text}")

                # 3. Send Notifications Initialized
                requests.post(endpoint_url, headers=post_headers, json={
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized"
                })
                
                # 4. List Tools
                print("Listing tools...")
                list_tools_payload = {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                }
                
                r_tools = requests.post(endpoint_url, headers=post_headers, json=list_tools_payload)
                print(f"Tools response: {r_tools.status_code}")
                # print(f"Tools body: {r_tools.text}")
                
                tools_data = r_tools.json()
                if "result" in tools_data and "tools" in tools_data["result"]:
                    tools = tools_data["result"]["tools"]
                    print(f"\nFound {len(tools)} tools:")
                    for t in tools:
                        print(f"- {t['name']}: {t.get('description', 'No description')}")
                else:
                    print("No tools found in response.")

                # We are done for the test, break the loop
                break
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_session()
