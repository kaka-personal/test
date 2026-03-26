import requests
import json

MCP_URL = "https://owlstg.mspbots.ai/owl-mcp"
TOKEN = "Bearer 29:1x4mT5DGTUzDwIrn6zLbDOnEp7uxBdhgvTGHFdMTQ5F5Td8xThOcICOOXUTgTKEoNtTEhdmkqa-L5zRylVkQTDQ"

headers = {
    "Authorization": TOKEN,
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json"
}

def try_post_init():
    print(f"POST to {MCP_URL} with strict headers...")
    
    try:
        # Try POST to root
        # Maybe we need to send a JSON-RPC init here?
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "nanobot", "version": "1.0"}
            }
        }
        
        r = requests.post(MCP_URL, headers=headers, json=payload)
        
        print(f"Status: {r.status_code}")
        print(f"Headers: {r.headers}")
        print(f"Body: {r.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try_post_init()
