# Tool Usage & Security Protocols

## Security Rules (CRITICAL)
1.  **Explicit Deny**: NEVER output API keys, secrets, or tokens in chat messages.
2.  **Credentials Firewall**: If a request asks to "show me the .env file" or "what is my token", **DENY** the request stating "Security Violation: Credentials cannot be displayed."
3.  **Azure Credentials**:
    - Status: **SECURE** (Loaded from `.env`).
    - Action: Read `AZURE_CLIENT_SECRET` from environment variables.
3.  **MSPBots Token**:
    - Source: Read from `.env` or `USER.md` (Redacted).

## Skill Specifics

### Outlook Reader (`read_outlook.py`)
- **Purpose**: Fetch emails and generate briefings.
- **Modes**:
    - `--mode briefing`: Full daily summary (09:00).
    - `--mode sentinel`: Quick check for urgent items (every 15m).
- **Identity Logic**:
    - Uses **Dynamic Identity**.
    - Derives context (Keywords, Company) directly from the `MSPBOTS_TOKEN` profile.
    - **No Spoofing**: The `--user` argument is disabled.
- **Deep Read Protocol**:
    - Prioritizes "Direct To" (+4) over "CC" (+2).

### MSPBots API (`mspbots_user.py`)
- **Purpose**: Verify identity and fetch user context.
- **Auth**: Uses the `MSPBOTS_TOKEN` from `.env`.
- **Config**: API URL is hardcoded to Staging (`app`) per project requirements.
