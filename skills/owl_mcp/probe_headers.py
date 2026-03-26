import requests
import sseclient
import json

MCP_URL = "https://owlstg.mspbots.ai/owl-mcp"
TOKEN = "Bearer 29:1x4mT5DGTUzDwIrn6zLbDOnEp7uxBdhgvTGHFdMTQ5F5Td8xThOcICOOXUTgTKEoNtTEhdmkqa-L5zRylVkQTDQ"

# The server explicitly asked for this Accept header in the 406 error
headers = {
    "Authorization": TOKEN,
    "Accept": "application/json, text/event-stream"
}

def connect():
    print(f"Connecting to {MCP_URL} with strict headers...")
    
    try:
        # Try GET to root with the required headers
        response = requests.get(MCP_URL, headers=headers, stream=True)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            print("Connection successful! Reading stream...")
            client = sseclient.SSEClient(response)
            for event in client.events():
                print(f"EVENT: {event.event}")
                print(f"DATA: {event.data}")
                if event.event == 'endpoint':
                    print("Endpoint found! Exiting probe.")
                    break
        else:
            print(f"Failed. Body: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    connect()
