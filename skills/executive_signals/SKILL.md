# Skill: Executive Signals (V2)

## Description
Generates the **V2 Executive Signals Brief** for the MSP CEO. This skill queries PSA, Financial, and RMM datasets via Owl MCP to identify business exceptions, risks, and actionable insights.

It implements the full V2 PRD logic, including cross-domain risk weighting, issue deep dives, and client 360 views.

## Usage

### 1. Daily Brief (Page A)
Generates the high-level morning report. Prioritizes clients with multi-domain risks.
```bash
python3 /app/workspace/skills/executive_signals/brief_engine.py --mode brief
```

### 2. Issue Detail (Page B)
Drill down into a specific issue to see context, trends, and raw evidence.
```bash
python3 /app/workspace/skills/executive_signals/brief_engine.py --mode detail --id <ISSUE_ID>
```

### 3. Client 360 (Page C)
View a holistic health report for a specific client across all domains.
```bash
python3 /app/workspace/skills/executive_signals/brief_engine.py --mode client --client <CLIENT_NAME>
```

## Internal Logic
The `brief_engine.py` script:
1.  **Connects** to Owl MCP to fetch live datasets.
2.  **Normalizes** client names to link data across disparate systems (PSA/QBO/Datto).
3.  **Applies V2 Ranking**:
    -   **Critical Severity**: SLA Breaches, Server Outages.
    -   **Cross-Domain Boost**: If a client has issues in >1 domain, they are promoted to top priority.
4.  **Outputs** structured Markdown for the requested view mode.
