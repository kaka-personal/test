#!/usr/bin/env python3
import json
import subprocess
import sys

OWL_TOOL_PATH = "/app/workspace/skills/owl_mcp/call_tool.py"
DATASET_ID = "1639215741534023681" # PSA Ticket SLA

def call_owl_tool(tool_name, arguments):
    try:
        cmd = ["python3", OWL_TOOL_PATH, tool_name, json.dumps(arguments)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Exception: {e}")
        return None

print("Fetching preview...")
data = call_owl_tool("get_dataset_data_preview", {"dataset_id": DATASET_ID, "size": 2})
print(f"Type: {type(data)}")
print(json.dumps(data, indent=2))
