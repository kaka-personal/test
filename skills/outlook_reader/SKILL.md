# Outlook Reader Skill

## Description
Reads emails from Microsoft Outlook (Graph API) and analyzes them using "Deep Read" logic (Identity + Context + Intent).

## Capabilities
1.  **Briefing Mode**: Fetches emails from the last 24 hours (configurable) for daily reporting.
2.  **Sentinel Mode**: Scans recent emails (last 15 mins) for high-priority risks.

## Technical Architecture

### 1. Dynamic Identity Logic
The skill does NOT use hardcoded users. It derives identity at runtime:
- **Step 1**: Fetch `MSPBOTS_TOKEN` from `.env`.
- **Step 2**: Call MSPBots API (`/web/um/sys/user/info`) to get User Profile.
- **Step 3**: Generate Context:
    - **Target Email**: Matches the token's email.
    - **Company**: Matches the token's `companyName`.
    - **Keywords**: Automatically watches for `[FirstName]`, `[LastName]`, `[EmailPrefix]`.

### 2. Deep Read Protocol (Scoring)
Emails are scored to determine priority:
- **Direct To**: +4 points (Action required)
- **Direct Cc**: +2 points (FYI)
- **Group To**: +1 point
- **Group Cc**: +0.5 point
- **VIP Sender**: Multiplier or Immediate Override.

## Usage

```bash
# Daily Briefing (Last 24h)
python3 read_outlook.py --mode briefing

# Sentinel Check (Last 15m)
python3 read_outlook.py --mode sentinel
```

## Configuration
- **API Endpoint**: Hardcoded to `https://app.mspbots.ai/web/um/sys/user/info` (Staging).
- **Credentials**: Uses `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `MSPBOTS_TOKEN` from `.env`.
