import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta

# Add path to mspbots_api skill to allow import
script_dir = os.path.dirname(os.path.abspath(__file__))
skills_dir = os.path.dirname(script_dir)
mspbots_api_path = os.path.join(skills_dir, "mspbots_api")
sys.path.append(mspbots_api_path)
try:
    import mspbots_user
except ImportError:
    print(f"Error: Could not import mspbots_user skill from {mspbots_api_path}.", file=sys.stderr)
    sys.exit(1)

# Load .env manually if python-dotenv is not installed
workspace_dir = os.path.dirname(skills_dir)
ENV_PATH = os.path.join(workspace_dir, ".env")
if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

def get_access_token():
    """
    Acquire a fresh Access Token from Azure AD using Client Credentials.
    """
    client_id = os.environ.get("AZURE_CLIENT_ID")
    client_secret = os.environ.get("AZURE_CLIENT_SECRET")
    tenant_id = os.environ.get("AZURE_TENANT_ID")
    
    if not client_id or not client_secret or not tenant_id:
        return os.environ.get("MSGRAPH_TOKEN")

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        print(f"Error acquiring Azure token: {e}", file=sys.stderr)
        return None

def get_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def analyze_email(email, user_context):
    """
    Analyze email based on dynamic user context.
    """
    subject = email.get("subject", "") or ""
    body_preview = email.get("bodyPreview", "") or ""
    sender = email.get("sender", {}).get("emailAddress", {})
    sender_email = sender.get("address", "").lower()
    sender_name = sender.get("name", "")
    
    user_email = user_context.get("email", "").lower()
    keywords = user_context.get("keywords", [])
    
    score = 0
    tags = []
    
    # 1. Identity Check (Sender)
    # Dynamic logic: Check if sender shares the same domain
    user_domain = user_email.split("@")[-1] if "@" in user_email else ""
    
    if user_domain and user_domain in sender_email:
        sender_type = "Internal"
    else:
        sender_type = "External"

    # 2. Recipient Context
    to_recipients = [r.get("emailAddress", {}).get("address", "").lower() for r in email.get("toRecipients", [])]
    cc_recipients = [r.get("emailAddress", {}).get("address", "").lower() for r in email.get("ccRecipients", [])]
    
    if user_email in to_recipients:
        score += 4
        tags.append("Direct To")
    elif user_email in cc_recipients:
        score += 2
        tags.append("Direct Cc")
    else:
        score += 1
        tags.append("Group/List")

    # 3. Content Relevance (Dynamic Keywords)
    subject_lower = subject.lower()
    body_lower = body_preview.lower()
    
    # Check for user's name or company
    for kw in keywords:
        if kw and kw.lower() in subject_lower:
            score += 3
            tags.append(f"Keyword: {kw}")
            break # Match once is enough

    # Check for universal high priority words
    if "urgent" in subject_lower or "risk" in subject_lower:
        score += 5
        tags.append("Urgent")
    
    # System/Noise Filtering
    if "no-reply" in sender_email or "notification" in sender_email:
        score -= 2
        tags.append("System")
        
    # Fathom check
    if "fathom" in sender_name.lower():
        score = 0
        tags.append("FYI_ONLY")

    return {
        "id": email.get("id"),
        "subject": subject,
        "sender": {"name": sender_name, "address": sender_email, "type": sender_type},
        "receivedDateTime": email.get("receivedDateTime"),
        "score": score,
        "tags": tags,
        "body_preview": body_preview,
        "webLink": email.get("webLink")
    }

def fetch_emails(user_email, hours=0, minutes=0):
    token = get_access_token()
    if not token:
        print("Error: No Access Token available.")
        return []

    headers = get_headers(token)
    
    # Default to 24 hours if nothing specified
    if hours == 0 and minutes == 0:
        hours = 24
        
    dt = datetime.utcnow() - timedelta(hours=hours, minutes=minutes)
    time_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Use the dynamic user_email to fetch THEIR inbox
    url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages?$filter=receivedDateTime ge {time_str}&$top=50&$orderby=receivedDateTime desc"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("value", [])
    except Exception as e:
        # print(f"Error fetching emails for {user_email}: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["briefing", "sentinel"], default="briefing")
    parser.add_argument("--hours", type=int, default=0)
    parser.add_argument("--minutes", type=int, default=0)
    args = parser.parse_args()

    # 1. Resolve Identity via MSPBots Token
    api_response = mspbots_user.fetch_user_info_data()
    
    if "error" in api_response:
        print(f"CRITICAL: Failed to identify user from token. {api_response['error']}")
        sys.exit(1)
    
    # Extract the actual user data payload
    user_data = api_response.get("data", {})
    if not user_data:
        # Fallback: maybe the response IS the data (legacy behavior check)
        if "email" in api_response:
             user_data = api_response
        else:
             print(f"CRITICAL: API returned success but 'data' field is missing or empty. Response: {json.dumps(api_response)}")
             sys.exit(1)
        
    # Extract Identity Context
    user_email = user_data.get("email")
    first_name = user_data.get("firstName", "")
    last_name = user_data.get("lastName", "")
    company = user_data.get("companyName", "")
    
    if not user_email:
        print("CRITICAL: Token valid but no email address found in user profile.")
        sys.exit(1)

    # Build Dynamic Context
    user_context = {
        "email": user_email,
        "keywords": [first_name, last_name, company, "Urgent", "Risk", "@ceo"]
    }
    
    # print(f"DEBUG: Acting as {user_email} (Company: {company})")

    # 2. Fetch Emails for THIS user
    raw_emails = fetch_emails(user_email, args.hours, args.minutes)
    
    # 3. Analyze
    analyzed_emails = []
    for email in raw_emails:
        analysis = analyze_email(email, user_context)
        
        if args.mode == "sentinel":
            # Sentinel Mode: Strict filtering (Score >= 6 OR Urgent/Risk)
            is_urgent = analysis.get('score', 0) >= 6 or "Urgent" in analysis.get('tags', []) or "Risk" in analysis.get('tags', [])
            if is_urgent:
                analyzed_emails.append(analysis)
        else:
            # Briefing Mode: Include everything
            analyzed_emails.append(analysis)

    # Output JSON
    print(json.dumps(analyzed_emails, indent=2))

if __name__ == "__main__":
    main()
