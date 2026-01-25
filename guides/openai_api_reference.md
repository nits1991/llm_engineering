# OpenAI API Reference Guide

A comprehensive guide to OpenAI's API endpoints with examples for Postman testing.

## Table of Contents

1. [Authentication](#authentication)
2. [Chat Completions API](#chat-completions-api)
3. [Embeddings API](#embeddings-api)
4. [Image Generation API (DALL-E)](#image-generation-api)
5. [Text-to-Speech API](#text-to-speech-api)
6. [Speech-to-Text API (Whisper)](#speech-to-text-api)
7. [Moderations API](#moderations-api)
8. [Models API](#models-api)
9. [Files API](#files-api)
10. [Fine-tuning API](#fine-tuning-api)
11. [Batches API](#batches-api)

---

## Authentication

All OpenAI API requests require authentication using an API key.

**Header Format:**

```
Authorization: Bearer YOUR_API_KEY
```

**Getting Your API Key:**

1. Visit https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy and store it securely (you won't see it again!)

**Security Best Practices:**

- Never commit API keys to version control
- Use environment variables in production
- Rotate keys regularly
- Use separate keys for development and production
- Monitor usage at https://platform.openai.com/usage

**Organization IDs (Optional):**
For users in multiple organizations, specify which one to use:

```
OpenAI-Organization: org-YOUR_ORG_ID
```

---

## Chat Completions API

**Purpose:** Generate conversational responses using GPT models.

**Endpoint:** `POST https://api.openai.com/v1/chat/completions`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
Content-Type: application/json
```

**Request Body:**

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "What is the capital of France?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 150
}
```

**Available Models:**

- `gpt-4o` - Most capable model
- `gpt-4o-mini` - Fast and affordable
- `gpt-4-turbo` - Previous generation
- `gpt-3.5-turbo` - Budget option

**All Parameters:**

| Parameter           | Type          | Default  | Description                                                   |
| ------------------- | ------------- | -------- | ------------------------------------------------------------- |
| `model`             | string        | Required | Model ID to use (e.g., `gpt-4o-mini`)                         |
| `messages`          | array         | Required | List of messages in conversation format                       |
| `temperature`       | number        | 1        | Sampling temperature (0-2). Higher = more random              |
| `max_tokens`        | integer       | inf      | Maximum tokens to generate in response                        |
| `top_p`             | number        | 1        | Nucleus sampling: consider tokens with top_p probability mass |
| `n`                 | integer       | 1        | Number of chat completion choices to generate                 |
| `stream`            | boolean       | false    | Stream back partial progress                                  |
| `stop`              | string/array  | null     | Up to 4 sequences where API stops generating                  |
| `presence_penalty`  | number        | 0        | (-2 to 2) Penalize new topics. Positive = more diverse        |
| `frequency_penalty` | number        | 0        | (-2 to 2) Penalize repetition. Positive = less repetitive     |
| `logit_bias`        | map           | null     | Modify likelihood of specified tokens                         |
| `user`              | string        | null     | Unique identifier for end-user (helps monitoring)             |
| `response_format`   | object        | null     | Format of output. Use `{"type": "json_object"}` for JSON      |
| `seed`              | integer       | null     | For deterministic sampling (beta)                             |
| `tools`             | array         | null     | Functions the model can call                                  |
| `tool_choice`       | string/object | null     | Controls which tool is called                                 |

**Advanced Features:**

### Function Calling / Tools

Enable models to call functions you define:

```json
{
  "model": "gpt-4o-mini",
  "messages": [{ "role": "user", "content": "What's the weather in Boston?" }],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": { "type": "string", "description": "City name" },
            "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] }
          },
          "required": ["location"]
        }
      }
    }
  ]
}
```

### JSON Mode

Force model to respond with valid JSON:

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant that outputs JSON."
    },
    { "role": "user", "content": "List 3 fruits with colors" }
  ],
  "response_format": { "type": "json_object" }
}
```

### Streaming Responses

Get partial results as they're generated:

```json
{
  "model": "gpt-4o-mini",
  "messages": [{ "role": "user", "content": "Write a story" }],
  "stream": true
}
```

Stream response format (Server-Sent Events):

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","choices":[{"delta":{"content":"The"}}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","choices":[{"delta":{"content":" story"}}]}

data: [DONE]
```

**Response Example:**

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4o-mini",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The capital of France is Paris."
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 10,
    "total_tokens": 30
  },
  "system_fingerprint": "fp_44709d6fcb"
}
```

**Finish Reasons:**

- `stop` - Natural stopping point or provided stop sequence reached
- `length` - Maximum token limit reached
- `content_filter` - Content filtered due to policy violations
- `tool_calls` - Model called a function/tool
- `function_call` - (Deprecated) Model called a function

---

## Embeddings API

**Purpose:** Convert text into numerical vectors for semantic search, clustering, and recommendations.

**Endpoint:** `POST https://api.openai.com/v1/embeddings`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
Content-Type: application/json
```

**Request Body:**

```json
{
  "model": "text-embedding-3-small",
  "input": "The quick brown fox jumps over the lazy dog"
}
```

**Available Models:**

- `text-embedding-3-large` - Most powerful, 3072 dimensions, better performance
- `text-embedding-3-small` - Fast and affordable, 1536 dimensions, good for most tasks
- `text-embedding-ada-002` - Legacy model (still supported)

**All Parameters:**

| Parameter         | Type         | Default  | Description                                         |
| ----------------- | ------------ | -------- | --------------------------------------------------- |
| `model`           | string       | Required | Model ID to use                                     |
| `input`           | string/array | Required | Text(s) to embed. Can be string or array of strings |
| `encoding_format` | string       | float    | Format of embeddings: `float` or `base64`           |
| `dimensions`      | integer      | varies   | Number of dimensions (only for v3 models)           |
| `user`            | string       | null     | Unique identifier for end-user                      |

**Dimensions Parameter (v3 models only):**
You can reduce embedding dimensions for efficiency:

```json
{
  "model": "text-embedding-3-large",
  "input": "Your text here",
  "dimensions": 256
}
```

This maintains performance while reducing storage/processing costs.

**Batch Processing:**
Process multiple texts efficiently:

```json
{
  "model": "text-embedding-3-small",
  "input": ["Text one", "Text two", "Text three"]
}
```

**Response for Batch:**

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "index": 0,
      "embedding": [0.002, -0.009, ...]
    },
    {
      "object": "embedding",
      "index": 1,
      "embedding": [0.001, -0.008, ...]
    }
  ],
  "model": "text-embedding-3-small",
  "usage": {
    "prompt_tokens": 24,
    "total_tokens": 24
  }
}
```

**Use Cases:**

- Semantic search
- Document similarity
- Recommendation systems
- Clustering and categorization

**Response Example:**

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "index": 0,
      "embedding": [
        0.002345, -0.009876, 0.012345
        // ... 1536 or 3072 values
      ]
    }
  ],
  "model": "text-embedding-3-small",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}
```

---

## Image Generation API (DALL-E)

**Purpose:** Generate images from text descriptions.

**Endpoint:** `POST https://api.openai.com/v1/images/generations`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
Content-Type: application/json
```

**Request Body:**

```json
{
  "model": "dall-e-3",
  "prompt": "A futuristic city with flying cars at sunset, digital art",
  "size": "1024x1024",
  "quality": "standard",
  "n": 1
}
```

**Available Models:**

- `dall-e-3` - Latest, most capable, best quality (released Nov 2023)
- `dall-e-2` - Previous generation, multiple images per request

**All Parameters:**

| Parameter         | Type    | Default   | Description                                             |
| ----------------- | ------- | --------- | ------------------------------------------------------- |
| `model`           | string  | Required  | `dall-e-3` or `dall-e-2`                                |
| `prompt`          | string  | Required  | Text description of image (max 4000 chars for DALL-E 3) |
| `n`               | integer | 1         | Number of images (1 for DALL-E 3, 1-10 for DALL-E 2)    |
| `size`            | string  | 1024x1024 | Image dimensions (see below)                            |
| `quality`         | string  | standard  | `standard` or `hd` (DALL-E 3 only)                      |
| `style`           | string  | vivid     | `vivid` or `natural` (DALL-E 3 only)                    |
| `response_format` | string  | url       | `url` or `b64_json`                                     |
| `user`            | string  | null      | Unique identifier for end-user                          |

**Size Options:**

**DALL-E 3:**

- `1024x1024` (square)
- `1792x1024` (landscape)
- `1024x1792` (portrait)

**DALL-E 2:**

- `256x256`
- `512x512`
- `1024x1024`

**Style Parameter (DALL-E 3):**

- `vivid` - Hyper-real and dramatic images
- `natural` - More natural, less hyper-real

**Advanced Example:**

```json
{
  "model": "dall-e-3",
  "prompt": "A serene Japanese garden with cherry blossoms, koi pond, and traditional pagoda, painted in watercolor style",
  "size": "1792x1024",
  "quality": "hd",
  "style": "natural",
  "n": 1
}
```

**Response with Revised Prompt:**

```json
{
  "created": 1677652288,
  "data": [
    {
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/...",
      "revised_prompt": "A tranquil Japanese garden featuring blooming cherry blossoms..."
    }
  ]
}
```

Note: DALL-E 3 often revises prompts for safety and quality. Check `revised_prompt` in response.

**Response Example:**

```json
{
  "created": 1677652288,
  "data": [
    {
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/...",
      "revised_prompt": "A futuristic cityscape..."
    }
  ]
}
```

---

## Text-to-Speech API

**Purpose:** Convert text to realistic spoken audio.

**Endpoint:** `POST https://api.openai.com/v1/audio/speech`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
Content-Type: application/json
```

**Request Body:**

```json
{
  "model": "tts-1",
  "input": "Hello! Welcome to OpenAI's text-to-speech API.",
  "voice": "alloy"
}
```

**Available Models:**

- `tts-1` - Fast, lower latency
- `tts-1-hd` - Higher quality audio

**Voice Options:**

- `alloy` - Neutral
- `echo` - Male
- `fable` - British accent
- `onyx` - Deep male
- `nova` - Female
- `shimmer` - Female

**Audio Formats:**

- `mp3` (default)
- `opus` - Internet streaming
- `aac` - Digital audio compression
- `flac` - Lossless audio
- `wav` - Uncompressed
- `pcm` - Raw audio

**Response:** Binary audio file

**Note for Postman:** You'll need to save the response as a file. In Postman, go to "Send and Download" instead of just "Send".

---

## Speech-to-Text API (Whisper)

**Purpose:** Transcribe or translate audio to text.

### Transcription Endpoint

**Endpoint:** `POST https://api.openai.com/v1/audio/transcriptions`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
Content-Type: multipart/form-data
```

**Form Data:**

- `file`: Audio file (mp3, mp4, mpeg, mpga, m4a, wav, webm)
- `model`: `whisper-1`
- `language`: (optional) ISO-639-1 code (e.g., "en" for English)
- `response_format`: `json` (default), `text`, `srt`, `verbose_json`, `vtt`

**Request Body (multipart/form-data):**

```
file: [audio file]
model: whisper-1
language: en
```

**Response Example:**

```json
{
  "text": "Hello, this is a test transcription."
}
```

### Translation Endpoint

**Endpoint:** `POST https://api.openai.com/v1/audio/translations`

Translates audio in any language to English text.

**Same structure as transcription, but always outputs English.**

---

## Moderations API

**Purpose:** Check if content complies with OpenAI's usage policies.

**Endpoint:** `POST https://api.openai.com/v1/moderations`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
Content-Type: application/json
```

**Request Body:**

```json
{
  "model": "text-moderation-latest",
  "input": "I want to hurt someone"
}
```

**Available Models:**

- `text-moderation-latest` - Most current model
- `text-moderation-stable` - Stable version

**Response Example:**

```json
{
  "id": "modr-123",
  "model": "text-moderation-007",
  "results": [
    {
      "flagged": true,
      "categories": {
        "sexual": false,
        "hate": false,
        "harassment": false,
        "self-harm": false,
        "sexual/minors": false,
        "hate/threatening": false,
        "violence/graphic": false,
        "self-harm/intent": false,
        "self-harm/instructions": false,
        "harassment/threatening": true,
        "violence": true
      },
      "category_scores": {
        "sexual": 0.0000012,
        "hate": 0.0234,
        "harassment": 0.156,
        "self-harm": 0.000023,
        "sexual/minors": 0.0000001,
        "hate/threatening": 0.0012,
        "violence/graphic": 0.0034,
        "self-harm/intent": 0.00012,
        "self-harm/instructions": 0.000001,
        "harassment/threatening": 0.789,
        "violence": 0.892
      }
    }
  ]
}
```

**Use Cases:**

- Content filtering
- User input validation
- Compliance checking

---

## Models API

**Purpose:** List available models and get model details.

### List Models

**Endpoint:** `GET https://api.openai.com/v1/models`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
```

**Response Example:**

```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4o",
      "object": "model",
      "created": 1687882410,
      "owned_by": "openai"
    },
    {
      "id": "gpt-4o-mini",
      "object": "model",
      "created": 1687882411,
      "owned_by": "openai"
    }
  ]
}
```

### Retrieve Model

**Endpoint:** `GET https://api.openai.com/v1/models/{model_id}`

**Example:** `GET https://api.openai.com/v1/models/gpt-4o-mini`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
```

**Response Example:**

```json
{
  "id": "gpt-4o-mini",
  "object": "model",
  "created": 1687882411,
  "owned_by": "openai"
}
```

---

## Files API

**Purpose:** Upload and manage files for use with other APIs like Fine-tuning and Assistants.

### Upload File

**Endpoint:** `POST https://api.openai.com/v1/files`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
Content-Type: multipart/form-data
```

**Form Data:**

- `file`: File to upload
- `purpose`: Purpose of file - `fine-tune`, `assistants`, or `batch`

**Supported Formats:**

- `.jsonl` for fine-tuning and batch
- Various formats for assistants (txt, pdf, docx, etc.)

**Example Request:**

```
file: training_data.jsonl
purpose: fine-tune
```

**Response:**

```json
{
  "id": "file-abc123",
  "object": "file",
  "bytes": 120000,
  "created_at": 1677652288,
  "filename": "training_data.jsonl",
  "purpose": "fine-tune"
}
```

### List Files

**Endpoint:** `GET https://api.openai.com/v1/files`

**Parameters:**

- `purpose` (optional): Filter by purpose

**Response:**

```json
{
  "data": [
    {
      "id": "file-abc123",
      "object": "file",
      "bytes": 120000,
      "created_at": 1677652288,
      "filename": "training_data.jsonl",
      "purpose": "fine-tune"
    }
  ],
  "object": "list"
}
```

### Retrieve File

**Endpoint:** `GET https://api.openai.com/v1/files/{file_id}`

### Delete File

**Endpoint:** `DELETE https://api.openai.com/v1/files/{file_id}`

**Response:**

```json
{
  "id": "file-abc123",
  "object": "file",
  "deleted": true
}
```

### Retrieve File Content

**Endpoint:** `GET https://api.openai.com/v1/files/{file_id}/content`

Returns the raw file content.

---

## Fine-tuning API

**Purpose:** Create custom models trained on your data.

### Create Fine-tuning Job

**Endpoint:** `POST https://api.openai.com/v1/fine_tuning/jobs`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
Content-Type: application/json
```

**Request Body:**

```json
{
  "training_file": "file-abc123",
  "model": "gpt-4o-mini-2024-07-18",
  "hyperparameters": {
    "n_epochs": 3
  }
}
```

**Available Base Models:**

- `gpt-4o-mini-2024-07-18`
- `gpt-4o-2024-08-06`
- `gpt-3.5-turbo`

**All Parameters:**

| Parameter         | Type    | Default  | Description                                           |
| ----------------- | ------- | -------- | ----------------------------------------------------- |
| `model`           | string  | Required | Base model to fine-tune                               |
| `training_file`   | string  | Required | File ID of training data                              |
| `validation_file` | string  | null     | File ID of validation data                            |
| `hyperparameters` | object  | {}       | Training hyperparameters                              |
| `suffix`          | string  | null     | String to add to fine-tuned model name (max 40 chars) |
| `seed`            | integer | null     | Random seed for reproducibility                       |

**Hyperparameters:**

- `n_epochs`: Number of training epochs (auto, 1-50)
- `batch_size`: Batch size (auto, or specific value)
- `learning_rate_multiplier`: Learning rate multiplier (auto, 0.05-5.0)

**Training Data Format (.jsonl):**

```jsonl
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}, {"role": "assistant", "content": "Hi there!"}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "How are you?"}, {"role": "assistant", "content": "I'm doing great!"}]}
```

**Response:**

```json
{
  "id": "ftjob-abc123",
  "object": "fine_tuning.job",
  "model": "gpt-4o-mini-2024-07-18",
  "created_at": 1677652288,
  "fine_tuned_model": null,
  "organization_id": "org-123",
  "result_files": [],
  "status": "queued",
  "validation_file": null,
  "training_file": "file-abc123"
}
```

### List Fine-tuning Jobs

**Endpoint:** `GET https://api.openai.com/v1/fine_tuning/jobs`

**Parameters:**

- `after` (optional): Pagination cursor
- `limit` (optional): Number of jobs to return (default 20)

### Retrieve Fine-tuning Job

**Endpoint:** `GET https://api.openai.com/v1/fine_tuning/jobs/{job_id}`

### Cancel Fine-tuning Job

**Endpoint:** `POST https://api.openai.com/v1/fine_tuning/jobs/{job_id}/cancel`

### List Fine-tuning Events

**Endpoint:** `GET https://api.openai.com/v1/fine_tuning/jobs/{job_id}/events`

Track training progress and metrics.

**Job Status Values:**

- `queued` - Job is waiting to start
- `running` - Training in progress
- `succeeded` - Training completed successfully
- `failed` - Training failed
- `cancelled` - Job was cancelled

---

## Batches API

**Purpose:** Process multiple API requests asynchronously at 50% cost.

### Create Batch

**Endpoint:** `POST https://api.openai.com/v1/batches`

**Headers:**

```
Authorization: Bearer {{OPENAI_API_KEY}}
Content-Type: application/json
```

**Request Body:**

```json
{
  "input_file_id": "file-abc123",
  "endpoint": "/v1/chat/completions",
  "completion_window": "24h"
}
```

**Parameters:**

- `input_file_id`: File containing batch requests (.jsonl)
- `endpoint`: API endpoint (`/v1/chat/completions` or `/v1/embeddings`)
- `completion_window`: `24h` (currently only option)
- `metadata`: Optional metadata (key-value pairs)

**Input File Format (.jsonl):**

```jsonl
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "Hello!"}]}}
{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "How are you?"}]}}
```

**Response:**

```json
{
  "id": "batch_abc123",
  "object": "batch",
  "endpoint": "/v1/chat/completions",
  "errors": null,
  "input_file_id": "file-abc123",
  "completion_window": "24h",
  "status": "validating",
  "created_at": 1677652288
}
```

### Retrieve Batch

**Endpoint:** `GET https://api.openai.com/v1/batches/{batch_id}`

**Status Values:**

- `validating` - Input file is being validated
- `failed` - Input validation failed
- `in_progress` - Batch is being processed
- `finalizing` - Batch completed, output file being generated
- `completed` - Batch successfully completed
- `expired` - Batch didn't complete within 24 hours
- `cancelling` - Cancellation in progress
- `cancelled` - Batch was cancelled

### List Batches

**Endpoint:** `GET https://api.openai.com/v1/batches`

**Parameters:**

- `after` (optional): Pagination cursor
- `limit` (optional): Number to return (default 20, max 100)

### Cancel Batch

**Endpoint:** `POST https://api.openai.com/v1/batches/{batch_id}/cancel`

**Benefits:**

- 50% lower cost than synchronous API
- Dedicated higher rate limits
- Fast 24-hour turnaround
- Same models and features

**Use Cases:**

- Processing large datasets
- Bulk evaluations
- Non-urgent batch jobs
- Cost optimization

---

## Common Response Status Codes

| Code  | Status                | Description                          | Solution                               |
| ----- | --------------------- | ------------------------------------ | -------------------------------------- |
| `200` | OK                    | Success                              | Request completed successfully         |
| `400` | Bad Request           | Invalid parameters or request format | Check request body and parameters      |
| `401` | Unauthorized          | Invalid or missing API key           | Verify API key in Authorization header |
| `403` | Forbidden             | Insufficient permissions or blocked  | Check organization permissions         |
| `404` | Not Found             | Invalid endpoint or model            | Verify endpoint URL and model name     |
| `413` | Payload Too Large     | Request too large                    | Reduce request size or use batches     |
| `429` | Too Many Requests     | Rate limit exceeded                  | Implement backoff, upgrade tier        |
| `500` | Internal Server Error | OpenAI server issue                  | Retry with exponential backoff         |
| `503` | Service Unavailable   | Server overloaded or maintenance     | Wait and retry                         |

**Error Response Format:**

```json
{
  "error": {
    "message": "Invalid API key provided",
    "type": "invalid_request_error",
    "param": null,
    "code": "invalid_api_key"
  }
}
```

**Error Types:**

- `invalid_request_error` - Invalid request parameters
- `authentication_error` - Authentication failed
- `permission_error` - Insufficient permissions
- `not_found_error` - Resource not found
- `rate_limit_error` - Rate limit exceeded
- `api_error` - OpenAI server error
- `timeout_error` - Request timed out

**Handling Rate Limits:**

```python
import time
from openai import OpenAI, RateLimitError

client = OpenAI()

max_retries = 5
for attempt in range(max_retries):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello!"}]
        )
        break
    except RateLimitError as e:
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
        else:
            raise
```

---

## Rate Limits

Rate limits are enforced at multiple levels:

### Limit Types

1. **RPM (Requests Per Minute)** - Number of API requests per minute
2. **TPM (Tokens Per Minute)** - Total tokens (input + output) per minute
3. **TPD (Tokens Per Day)** - Total tokens per day
4. **IPM (Images Per Minute)** - For DALL-E API
5. **RPD (Requests Per Day)** - Daily request limit (for batches)

### Rate Limits by Tier

| Tier   | Usage   | GPT-4o TPM | GPT-4o-mini TPM | Batch Queue |
| ------ | ------- | ---------- | --------------- | ----------- |
| Free   | $0      | 30,000     | 200,000         | 100,000 TPD |
| Tier 1 | $5+     | 2M         | 30M             | 2M TPD      |
| Tier 2 | $50+    | 5M         | 150M            | 10M TPD     |
| Tier 3 | $100+   | 10M        | 200M            | 20M TPD     |
| Tier 4 | $250+   | 30M        | 300M            | 50M TPD     |
| Tier 5 | $1,000+ | 60M        | 600M            | 100M TPD    |

**Check Your Limits:**

- Dashboard: https://platform.openai.com/account/rate-limits
- Response headers include current usage:
  ```
  x-ratelimit-limit-requests: 500
  x-ratelimit-remaining-requests: 499
  x-ratelimit-reset-requests: 1s
  ```

### Best Practices for Rate Limits

1. **Implement Exponential Backoff**

   ```python
   import time
   wait_time = min(2 ** retry_count, 60)  # Max 60 seconds
   time.sleep(wait_time)
   ```

2. **Use Batch API** for non-urgent requests (50% cheaper)

3. **Monitor Headers** in responses to track usage

4. **Spread Requests** across time instead of bursts

5. **Upgrade Tier** if consistently hitting limits

6. **Cache Results** when appropriate to reduce API calls

7. **Use Streaming** for long responses (doesn't affect rate limits but improves UX)

### Increasing Rate Limits

Limits automatically increase with usage tier:

- Spend $5: Tier 1 (higher limits)
- Spend $50: Tier 2
- Continue climbing with sustained usage

Contact OpenAI for custom enterprise limits.

---

## Best Practices

### 🔐 Security

1. **Never Hardcode API Keys**

   ```python
   # ❌ Bad
   api_key = "sk-proj-abc123..."

   # ✅ Good
   api_key = os.getenv("OPENAI_API_KEY")
   ```

2. **Use Environment Variables** in Postman and production
3. **Rotate Keys Regularly** (every 90 days recommended)
4. **Use Separate Keys** for dev/staging/production
5. **Monitor Usage** at https://platform.openai.com/usage
6. **Set Usage Limits** in your organization settings

### 💰 Cost Optimization

1. **Start with Smaller Models** for testing

   - Use `gpt-4o-mini` instead of `gpt-4o` when appropriate
   - `gpt-4o-mini` is 10x cheaper with good performance

2. **Use Batch API** for non-urgent tasks (50% discount)

3. **Implement Caching**

   - Cache embeddings (they're deterministic)
   - Cache common completions
   - Use Redis or similar for production

4. **Control Token Usage**

   ```json
   {
     "max_tokens": 150,  // Limit response length
     "messages": [...],   // Keep context minimal
   }
   ```

5. **Monitor with `max_tokens` and `stop` sequences**

6. **Use Streaming** for better UX without extra cost

### 🎯 Prompt Engineering

1. **Be Specific and Clear**

   ```json
   // ❌ Vague
   {"content": "Write about dogs"}

   // ✅ Specific
   {"content": "Write a 150-word summary about dog training techniques for puppies"}
   ```

2. **Use System Prompts** to set consistent behavior

3. **Temperature Settings**

   - `0.0-0.3`: Factual, consistent outputs (docs, code, analysis)
   - `0.7-1.0`: Creative, varied outputs (stories, brainstorming)
   - `1.0-2.0`: Very creative, experimental

4. **Few-Shot Learning**: Include examples in prompts

   ```json
   {
     "messages": [
       {
         "role": "system",
         "content": "Classify sentiment as positive/negative/neutral"
       },
       { "role": "user", "content": "I love this product!" },
       { "role": "assistant", "content": "positive" },
       { "role": "user", "content": "This is the new text to classify" }
     ]
   }
   ```

5. **Use JSON Mode** for structured outputs
   ```json
   {
     "response_format": { "type": "json_object" },
     "messages": [{ "role": "system", "content": "Output valid JSON only" }]
   }
   ```

### ⚡ Performance

1. **Use Streaming** for long responses

   ```json
   { "stream": true }
   ```

2. **Implement Timeout Handling**

   ```python
   from openai import OpenAI
   client = OpenAI(timeout=30.0)  # 30 second timeout
   ```

3. **Async Operations** for multiple requests

   ```python
   import asyncio
   from openai import AsyncOpenAI

   async def main():
       client = AsyncOpenAI()
       responses = await asyncio.gather(
           client.chat.completions.create(...),
           client.chat.completions.create(...),
       )
   ```

4. **Batch Processing** for bulk operations

5. **Reduce Context Size** - only include necessary message history

### 🔍 Monitoring & Debugging

1. **Log All Requests** with unique IDs

   ```json
   { "user": "user-123" } // Include for tracking
   ```

2. **Track Token Usage** in responses

   ```python
   usage = response.usage
   print(f"Tokens: {usage.total_tokens}")
   ```

3. **Monitor Errors** and implement retry logic

4. **Check `finish_reason`** to understand why generation stopped

   - `stop`: Natural completion
   - `length`: Hit token limit
   - `content_filter`: Filtered content

5. **Use `seed` Parameter** for reproducible results (beta)
   ```json
   { "seed": 12345 }
   ```

### 🛡️ Content Safety

1. **Use Moderation API** before processing user input

   ```python
   moderation = client.moderations.create(input=user_text)
   if moderation.results[0].flagged:
       # Handle flagged content
   ```

2. **Implement Input Validation**
3. **Set Up Content Filters** in your application
4. **Review Usage Policies**: https://openai.com/policies/usage-policies

### 📊 Production Considerations

1. **Implement Circuit Breakers** for API failures
2. **Use Load Balancing** for high-traffic applications
3. **Set Up Monitoring/Alerting** for errors and usage
4. **Implement Fallback Strategies** when API is unavailable
5. **Cache Strategically** for common queries
6. **Test Thoroughly** before production deployment
7. **Have Manual Review** for high-stakes applications

---

## Cost Considerations

### Chat Completions Pricing (per 1M tokens)

| Model             | Input  | Output | Use Case                              |
| ----------------- | ------ | ------ | ------------------------------------- |
| **GPT-4o**        | $2.50  | $10.00 | Most capable, complex tasks           |
| **GPT-4o-mini**   | $0.15  | $0.60  | Fast, affordable, good for most tasks |
| **GPT-4-turbo**   | $10.00 | $30.00 | Previous generation                   |
| **GPT-3.5-turbo** | $0.50  | $1.50  | Budget option, simple tasks           |

**Batch API (50% discount):**

- GPT-4o: $1.25 input / $5.00 output
- GPT-4o-mini: $0.075 input / $0.30 output

### Embeddings Pricing (per 1M tokens)

| Model                      | Price | Dimensions |
| -------------------------- | ----- | ---------- |
| **text-embedding-3-large** | $0.13 | 3072       |
| **text-embedding-3-small** | $0.02 | 1536       |
| **text-embedding-ada-002** | $0.10 | 1536       |

### Images Pricing

**DALL-E 3:**

- `1024x1024`: $0.040 per image
- `1024x1792` or `1792x1024`: $0.080 per image
- HD quality: 2x price

**DALL-E 2:**

- `1024x1024`: $0.020 per image
- `512x512`: $0.018 per image
- `256x256`: $0.016 per image

### Audio Pricing

**Text-to-Speech:**

- TTS: $15.00 per 1M characters
- TTS-HD: $30.00 per 1M characters

**Speech-to-Text (Whisper):**

- $0.006 per minute of audio

### Fine-tuning Pricing

**Training:**

- GPT-4o-mini: $3.00 per 1M tokens
- GPT-3.5-turbo: $8.00 per 1M tokens

**Usage (after training):**

- GPT-4o-mini: $0.30 input / $1.20 output (per 1M tokens)
- GPT-3.5-turbo: $3.00 input / $6.00 output (per 1M tokens)

### Cost Estimation Examples

**Example 1: Customer Support Bot**

- Model: `gpt-4o-mini`
- Average: 100 input tokens, 200 output tokens per conversation
- Volume: 10,000 conversations/month

**Calculation:**

- Input: (100 × 10,000) / 1,000,000 × $0.15 = $0.15
- Output: (200 × 10,000) / 1,000,000 × $0.60 = $1.20
- **Total: $1.35/month**

**Example 2: Document Embeddings**

- Model: `text-embedding-3-small`
- 1,000 documents × 500 tokens each = 500,000 tokens

**Calculation:**

- 500,000 / 1,000,000 × $0.02 = $0.01
- **Total: $0.01 (one-time)**

**Example 3: Image Generation**

- Model: `dall-e-3`
- 100 images at 1024x1024

**Calculation:**

- 100 × $0.040 = $4.00
- **Total: $4.00**

### Cost Optimization Strategies

1. **Use gpt-4o-mini** when possible (10x cheaper than GPT-4o)
2. **Batch API** for non-urgent work (50% discount)
3. **Limit max_tokens** to prevent runaway costs
4. **Cache embeddings** (they're deterministic)
5. **Use streaming** (doesn't cost extra, better UX)
6. **Implement request throttling** to prevent abuse
7. **Monitor usage** at https://platform.openai.com/usage
8. **Set usage limits** in organization settings
9. **Reduce context size** - only include necessary history
10. **Use function calling** to reduce token usage vs. long prompts

### Setting Usage Limits

In your OpenAI account:

1. Go to Settings → Limits
2. Set monthly budget limits
3. Receive email alerts at thresholds
4. Auto-disable API key if limit exceeded

_Prices as of January 2025 - check current pricing at https://openai.com/api/pricing_

---

## Next Steps

1. Import the Postman collection (see separate JSON file)
2. Set up your environment variable for `OPENAI_API_KEY`
3. Test each endpoint
4. Experiment with different parameters
5. Build your own applications!

## Additional Resources

- **[OpenAI API Documentation](https://platform.openai.com/docs)** - Official comprehensive docs
- **[OpenAI Cookbook](https://github.com/openai/openai-cookbook)** - Code examples and guides
- **[OpenAI Community Forum](https://community.openai.com/)** - Ask questions, share projects
- **[Rate Limits Guide](https://platform.openai.com/docs/guides/rate-limits)** - Understanding limits
- **[Error Codes Reference](https://platform.openai.com/docs/guides/error-codes)** - Troubleshooting
- **[Usage Dashboard](https://platform.openai.com/usage)** - Monitor your API usage
- **[API Status Page](https://status.openai.com/)** - Check service health
- **[Pricing Calculator](https://openai.com/api/pricing)** - Estimate costs

---

## Quick Reference Cheat Sheet

### Common Endpoints

```bash
# Chat Completions
POST https://api.openai.com/v1/chat/completions

# Embeddings
POST https://api.openai.com/v1/embeddings

# Images
POST https://api.openai.com/v1/images/generations

# Audio (TTS)
POST https://api.openai.com/v1/audio/speech

# Audio (STT)
POST https://api.openai.com/v1/audio/transcriptions

# Moderations
POST https://api.openai.com/v1/moderations

# Models
GET https://api.openai.com/v1/models

# Files
GET/POST/DELETE https://api.openai.com/v1/files

# Fine-tuning
POST https://api.openai.com/v1/fine_tuning/jobs

# Batches
POST https://api.openai.com/v1/batches
```

### Authentication Header

```bash
Authorization: Bearer YOUR_API_KEY
```

### Model Recommendations

| Task              | Best Model             | Alternative            |
| ----------------- | ---------------------- | ---------------------- |
| General chat      | gpt-4o-mini            | gpt-4o                 |
| Complex reasoning | gpt-4o                 | gpt-4-turbo            |
| Code generation   | gpt-4o                 | gpt-4o-mini            |
| Simple tasks      | gpt-4o-mini            | gpt-3.5-turbo          |
| Embeddings        | text-embedding-3-small | text-embedding-3-large |
| Image generation  | dall-e-3               | dall-e-2               |
| Text-to-Speech    | tts-1                  | tts-1-hd               |
| Speech-to-Text    | whisper-1              | -                      |

### Temperature Guide

| Temperature | Use Case               | Example                |
| ----------- | ---------------------- | ---------------------- |
| 0.0-0.3     | Factual, deterministic | Code, math, analysis   |
| 0.4-0.7     | Balanced               | General conversation   |
| 0.8-1.2     | Creative               | Stories, brainstorming |
| 1.3-2.0     | Very creative          | Experimental, artistic |

### Token Estimation

**Rule of thumb:** 1 token ≈ 4 characters or ≈ 0.75 words

**Examples:**

- "Hello, world!" ≈ 4 tokens
- Average sentence ≈ 15-20 tokens
- 1 page of text ≈ 300-500 tokens

**Check exact count:** Use the [Tokenizer tool](https://platform.openai.com/tokenizer)

### Common Parameters Quick Guide

```json
{
  "model": "gpt-4o-mini",           // Required: Model to use
  "messages": [...],                 // Required: Conversation
  "temperature": 0.7,                // 0-2: Randomness
  "max_tokens": 150,                 // Max response length
  "top_p": 1,                        // 0-1: Nucleus sampling
  "frequency_penalty": 0,            // -2 to 2: Reduce repetition
  "presence_penalty": 0,             // -2 to 2: Encourage variety
  "stream": false,                   // Enable streaming
  "stop": ["\n"],                    // Stop sequences
  "n": 1,                            // Number of completions
  "user": "user-123"                 // User identifier
}
```

### Error Handling Template

```python
from openai import OpenAI, APIError, RateLimitError, APIConnectionError

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello!"}]
    )
except RateLimitError as e:
    # Handle rate limit
    print("Rate limit exceeded, try again later")
except APIConnectionError as e:
    # Handle connection error
    print("Connection error, check network")
except APIError as e:
    # Handle API error
    print(f"API error: {e}")
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error: {e}")
```

### Postman Collection Variables

Set these in your Postman environment:

```
OPENAI_API_KEY: sk-proj-...
BASE_URL: https://api.openai.com/v1
MODEL: gpt-4o-mini
```

Then use in requests:

```
{{BASE_URL}}/chat/completions
Bearer {{OPENAI_API_KEY}}
```

---

## FAQ

**Q: Which model should I use?**  
A: Start with `gpt-4o-mini` for most tasks. Use `gpt-4o` only when you need maximum capability.

**Q: How much will this cost?**  
A: `gpt-4o-mini` costs about $0.75 per 1M tokens total. Most conversations use 100-500 tokens.

**Q: Why am I getting rate limited?**  
A: Free tier has low limits. Spend $5 to reach Tier 1 with much higher limits.

**Q: Can I use OpenAI for production?**  
A: Yes! Use environment variables, implement error handling, monitor usage, and set spending limits.

**Q: How do I reduce costs?**  
A: Use `gpt-4o-mini`, limit max_tokens, use Batch API (50% off), cache results, and monitor usage.

**Q: Is my data used for training?**  
A: No, API data is not used for training unless you opt in. See [Data Usage Policy](https://openai.com/policies/usage-policies).

**Q: How do I make requests faster?**  
A: Use streaming, reduce context size, use faster models (gpt-4o-mini), implement async requests.

**Q: What's the difference between temperature and top_p?**  
A: Both control randomness. Use one or the other, not both. Temperature is more common.

**Q: Can I fine-tune models?**  
A: Yes! Use the Fine-tuning API with `gpt-4o-mini` or `gpt-3.5-turbo` base models.

---

## Support

- **Technical Issues:** https://help.openai.com/
- **Community Forum:** https://community.openai.com/
- **Status Updates:** https://status.openai.com/
- **Email Support:** Available for paid tier users

---

**Document Version:** 2.0  
**Last Updated:** January 2025  
**Author:** Enhanced OpenAI API Reference Guide
