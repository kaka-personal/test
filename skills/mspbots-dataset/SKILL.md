---
name: mspbots-dataset
description: This skill is used to search, create datasets, and preview data content on the MSPbots platform. It supports natural language search, automatic dataset creation, and data preview.
---

# MSPbots Dataset Skill
## Skill Metadata
- Author: Leo
- Version: 1.0.1
- Tags: dataset, MSPbots, data query, creation
- Required Assets: assets/mspbots.token

## Introduction
This skill is used to search, create datasets, and preview data content on the MSPbots platform. It supports natural language search, automatic dataset creation, and data preview.

## Dependencies & Configuration

Users must first provide the token from the MSPbots platform before you can update the user configuration and proceed with the next steps.

- Requires MSPbots platform token (see [mspbots.token](assets/mspbots.token) example):

## Main Tools & Interfaces

### 1. search_dataset_via_rag
Search existing datasets on MSPbots platform using natural language.

**API Endpoint**: `POST https://owlstg.mspbots.ai/owl-agent/api/v1/search_dataset_via_rag`

**Parameters**:
- mspbots_token (optional): MSPbots authentication token
- requirements (required): Natural language description of dataset requirements
- top_k (optional): Number of results to return

**Returns**: List of datasets and their basic information

Example:
```bash
curl --location 'https://owlstg.mspbots.ai/owl-agent/api/v1/search_dataset_via_rag' \
--header 'Content-Type: application/json' \
--data '{
    "mspbots_token": "your token",
    "requirements": "Leo Yang Teams dataset email",
    "top_k": 5
}'
```

### 2. generate_dataset_via_chat
If no suitable dataset is found, automatically create one via chat.

**API Endpoint**: `POST https://owlstg.mspbots.ai/owl-agent/api/v1/generate_dataset_via_chat`

**Parameters**:
- mspbots_token (optional): MSPbots authentication token
- chat (required): Natural language instruction for dataset creation
- thread_id (optional): Conversation thread ID for continuity

**Returns**: Detailed information of the newly created dataset

Example:
```bash
curl --location 'https://owlstg.mspbots.ai/owl-agent/api/v1/generate_dataset_via_chat' \
--header 'Content-Type: application/json' \
--data '{
    "mspbots_token": "your token", 
    "chat": "Hello",
    "thread_id": "221cdcc9-2943-413d-9da6-c7164ee7243d"
}'
```

### 3. dataset_data_preview
Get a preview of the data content for a specified dataset.

**API Endpoint**: `GET https://app.mspbots.ai/web/query/sys/dataset/{datasetId}/data`

### Request Example

```bash
GET https://app.mspbots.ai/web/query/sys/dataset/2010931613545922561/data?filter=mspbots_id%20in%20(11%2C12)&size=10&current=1
```

### Query Parameters

| Name         | Type    | Required | Description                                   | Example                  |
|--------------|---------|----------|-----------------------------------------------|--------------------------|
| filter       | string  | No       | Data filter condition (SQL WHERE style)       | mspbots_id in (11,12)    |
| orderBy      | string  | No       | Sort order (asc / desc)                       | asc                      |
| orderFields  | string  | No       | Sort field                                    | create_time              |
| size         | int     | Yes      | Page size                                     | 10                       |
| current      | int     | Yes      | Current page                                  | 1                        |

### Path Parameters

| Name      | Type  | Required | Description      |
|-----------|-------|----------|-----------------|
| datasetId | long  | Yes      | Dataset ID      |

### Header Parameters

| Name           | Required | Description                | Example                        |
|----------------|----------|----------------------------|--------------------------------|
| token          | Yes      | User login token           | 53ae9a8d48833421c8e9e1d97748f8ef |

**Required headers:**

- token

**Returns**: List of data records, total count, and pagination info

Request Example:
```bash
curl --location 'https://app.mspbots.ai/web/query/sys/dataset/1478973401475702786/data?filter=teams_mail%20ilike%20%27%25leo%25%27&size=10&current=1' \
--header 'token: your token' 
```

## Workflow Description
1. Use `search_dataset_via_rag` to search for datasets.
2. If no suitable dataset is found, automatically call `generate_dataset_via_chat` to create one.
3. Use `dataset_data_preview` to get a preview of the dataset content.

## Error Handling
API error response format:
```json
{
  "ok": false,
  "error": "Invalid token"
}
```

HTTP Status Codes:
- 200: Success
- 400: Bad request
- 401: Unauthorized
- 500: Internal server error

## References
- [Owl API Docs](https://owlstg.mspbots.ai/owl-agent/api/docs)
- [Token Configuration](assets/mspbots.token)
