import sys
import threading
import time
import json
import requests

# Configuration
URL = "https://owlstg.mspbots.ai/owl-mcp"
TOKEN = "29:1x4mT5DGTUzDwIrn6zLbDOnEp7uxBdhgvTGHFdMTQ5F5Td8xThOcICOOXUTgTKEoNtTEhdmkqa-L5zRylVkQTDQ"

def run_mcp_flow():
    session_id = None
    
    print("--- Step 1: Get Session ID ---")
    # We expect this to fail with 400 but give us a header
    try:
        init_headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "text/event-stream"
        }
        res = requests.get(URL, headers=init_headers)
        if "mcp-session-id" in res.headers:
            session_id = res.headers["mcp-session-id"]
            print(f"Got Session ID: {session_id}")
        else:
            print("Failed to get session ID on first attempt.")
            print(res.headers)
            return
    except Exception as e:
        print(f"Init failed: {e}")
        return

    # Step 2: Connect to SSE with the ID
    print(f"--- Step 2: Connecting to SSE with ID {session_id} ---")
    # Use the base URL, pass ID in headers
    sse_url = URL 
    sse_headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "text/event-stream",
        "mcp-session-id": session_id  # <--- Critical change: Pass ID in header
    }
    
    try:
        with requests.get(sse_url, headers=sse_headers, stream=True, timeout=30) as response:
            print(f"SSE Status Code: {response.status_code}")
            
            # Start the POST thread
            def send_post_request():
                time.sleep(2) # Wait for SSE to be ready
                print(f"--- Step 3: Sending POST with Session ID: {session_id} ---")
                
                # Try passing ID in query param AND header just to be safe
                post_url = f"{URL}?sessionId={session_id}"
                post_headers = {
                    "Authorization": f"Bearer {TOKEN}",
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "mcp-session-id": session_id # <--- Pass ID in header here too
                }
                payload = {
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "id": 1
                }
                
                try:
                    p_res = requests.post(post_url, headers=post_headers, json=payload, timeout=10)
                    print(f"POST Status: {p_res.status_code}")
                    print("POST Response:", p_res.text)
                except Exception as e:
                    print(f"POST Failed: {e}")

            t = threading.Thread(target=send_post_request)
            t.start()
            
            # Read SSE
            print("--- Listening to SSE stream ---")
            # We'll just read a few chunks/lines to see the response to our POST
            start_time = time.time()
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    print(f"SSE Payload: {decoded_line}")
                
                if time.time() - start_time > 10:
                    print("Timeout reached, closing.")
                    break
            
            t.join(timeout=5)

    except Exception as e:
        print(f"SSE Connection Failed: {e}")

if __name__ == "__main__":
    run_mcp_flow()
