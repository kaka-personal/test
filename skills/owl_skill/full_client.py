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
        print(f"\n[STREAM] Event: {event.event}")
        print(f"[STREAM] Data: {event.data}")

def run_session():
    print("--- Step 1: Initialize Session ---")
    
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
    
    # Start the long-lived connection
    r_init = requests.post(MCP_URL, headers=headers, json=init_payload, stream=True)
    
    print(f"Init Status: {r_init.status_code}")
    session_id = r_init.headers.get('mcp-session-id')
    print(f"Session ID: {session_id}")
    
    if not session_id:
        print("No session ID returned. Exiting.")
        return

    # Update headers with session ID
    headers["mcp-session-id"] = session_id

    # Start reading the stream in background
    t = threading.Thread(target=read_stream, args=(r_init,))
    t.daemon = True
    t.start()
    
    time.sleep(2) # Wait for init response to print
    
    print("\n--- Step 2: Send Notifications Initialized ---")
    # Where do we post? Try root with sessionId param (camelCase)
    post_url = f"{MCP_URL}?sessionId={session_id}"
    
    print(f"Posting to: {post_url}")

    r_notif = requests.post(post_url, headers=headers, json={
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    })
    
    print("\n--- Step 3: List Tools ---")
    list_tools_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    r_tools = requests.post(post_url, headers=headers, json=list_tools_payload)
    print(f"Tools Request Status: {r_tools.status_code}")
    print(f"Tools Request Body: {r_tools.text}")
    
    # Wait a bit to see if response comes via stream
    time.sleep(5)

if __name__ == "__main__":
    run_session()
