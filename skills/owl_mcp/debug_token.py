import requests
import urllib.parse

url = "https://owlstg.mspbots.ai/owl-mcp"
raw_token = "29%3A1Pj3svhFYJo65hFm0sRt8vIp4LMIMijIbev_L41dtj-hOpZ8-FxvdzssUcqFVCZDn8dZo_LroinHnYGCtx7F1Zw"
decoded_token = urllib.parse.unquote(raw_token)

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

def test(token_val, label):
    headers = {
        "Authorization": f"Bearer {token_val}",
        "Content-Type": "application/json"
    }
    try:
        r = requests.post(url, headers=headers, json=payload)
        print(f"[{label}] Status: {r.status_code}")
        if r.status_code == 200:
            print(f"[{label}] Success!")
        else:
            print(f"[{label}] Response: {r.text[:100]}")
    except Exception as e:
        print(f"[{label}] Error: {e}")

print(f"Testing Raw: {raw_token}")
test(raw_token, "RAW")

print(f"Testing Decoded: {decoded_token}")
test(decoded_token, "DECODED")
