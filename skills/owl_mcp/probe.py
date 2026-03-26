import requests
import json

MCP_URL = "https://owlstg.mspbots.ai/owl-mcp"
TOKEN = "Bearer 29:1x4mT5DGTUzDwIrn6zLbDOnEp7uxBdhgvTGHFdMTQ5F5Td8xThOcICOOXUTgTKEoNtTEhdmkqa-L5zRylVkQTDQ"

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def probe():
    print(f"Probing {MCP_URL}...")
    
    # Try POST to root to see if it creates a session
    try:
        print("Attempting POST to root...")
        r = requests.post(MCP_URL, headers=headers, json={})
        print(f"POST root: {r.status_code}")
        print(f"Body: {r.text}")
    except Exception as e:
        print(f"POST failed: {e}")

    # Try GET to /sse with a made up session ID just in case
    try:
        print("Attempting GET /sse with query param...")
        r = requests.get(f"{MCP_URL}/sse?session_id=test", headers=headers)
        print(f"GET /sse?session_id=test: {r.status_code}")
    except Exception as e:
        print(f"GET failed: {e}")

if __name__ == "__main__":
    probe()
