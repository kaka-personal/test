import requests
import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='/app/workspace/.env')

def fetch_user_info_data():
    """
    Fetch user info from MSPBots API using the token in .env.
    Returns a dictionary with user data or error info.
    """
    # Read configuration from environment
    token = os.getenv('MSPBOTS_TOKEN')
    
    if not token:
        return {"error": "MSPBOTS_TOKEN not found in environment variables."}

    # Hardcoded URL as per instruction
    url = "https://app.mspbots.ai/web/um/sys/user/info"
    
    headers = {
        "token": token,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    data = fetch_user_info_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))
