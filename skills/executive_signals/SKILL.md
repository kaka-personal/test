# Skill: Executive Signals (V2)

## Description
Generates the **V2 Executive Signals Brief** for the MSP CEO. This skill queries PSA, Financial, and RMM datasets via the MSPbots Dataset REST API to identify business exceptions, risks, and actionable insights.

It implements the full V2 PRD logic, including cross-domain risk weighting and client watchlist generation.

## Usage

### Daily Brief
Generates the high-level morning report. Prioritizes clients with multi-domain risks.
```bash
python skills/executive_signals/brief_engine.py
```

## Internal Logic
The `brief_engine.py` script:
1.  **Discovers** datasets dynamically via `dynamic_discovery.py`, which calls the `mspbots-dataset` skill's REST API to search for relevant datasets by intent (e.g., PSA Tickets, Financial Invoices, RMM Alerts).
2.  **Fetches** live data previews from resolved datasets using `dataset_api.py`.
3.  **Normalizes** client names to link data across disparate systems (PSA/QBO/Datto).
4.  **Applies V2 Ranking**:
    -   **Critical Severity**: SLA Breaches, Server Outages.
    -   **Cross-Domain Boost**: If a client has issues in >1 domain, they are promoted to top priority.
5.  **Outputs** structured Markdown briefing with Top Issues, Watchlist, Domain Anomalies, and Recommended Actions.

## Dependencies
- `requests`
- `mspbots-dataset` skill (sibling skill for dataset search and preview)
- `mspbots_api` skill (for user identity resolution)

## Configuration
- **MSPBOTS_TOKEN**: Required in `.env` for API authentication.
