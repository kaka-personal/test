# Skill: Owl MCP

## Description
Interact with the MSPBots Owl MCP service to search datasets, tables, and integrations.

## Dependencies
- python3
- requests
- sseclient-py

## Configuration
- **MCP_URL**: `https://owlstg.mspbots.ai/owl-mcp`
- **Token**: Managed internally via `call_tool.py` (Hardcoded for now, should be env var in production).

## Tools

### get_integration_list
Get the list of user-integrated applications.
```bash
python3 /app/workspace/skills/owl_mcp/call_tool.py get_integration_list '{}'
```

### search_dataset
Search for datasets based on a natural language query.
- `query`: String describing data requirement.
- `top_k`: (Optional) Max results (default 5).
- `integrations`: (Optional) List of integration names to filter by.
```bash
python3 /app/workspace/skills/owl_mcp/call_tool.py search_dataset '{"query": "ticket statistics", "top_k": 3}'
```

### search_table
Find relevant tables using natural language.
- `query`: Natural language query.
```bash
python3 /app/workspace/skills/owl_mcp/call_tool.py search_table '{"query": "user active hours"}'
```

### get_dataset_data_preview
Preview data from a dataset.
- `dataset_id`: The ID of the dataset.
- `size`: (Optional) Number of records (max 10).
```bash
python3 /app/workspace/skills/owl_mcp/call_tool.py get_dataset_data_preview '{"dataset_id": "12345", "size": 5}'
```

### chat_with_owl_agent
Chat with the Owl Agent to create datasets or widgets.
- `content`: The message content.
```bash
python3 /app/workspace/skills/owl_mcp/call_tool.py chat_with_owl_agent '{"content": "Help me create a widget for open tickets"}'
```
