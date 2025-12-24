# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **ai-sdk**, a Python SDK that provides an OpenAI-compatible API interface for AI services (Yuanbao and Gemini models). The SDK wraps a custom chat completion API and presents it in a familiar OpenAI-style interface.

**Key constraints:**
- Python 3.8+ compatibility required: use `typing.List`, `typing.Optional`, etc. (NOT `list[]` or `str | None`)
- Task-based API: submit task → poll for result (no streaming support)
- All tests require real API calls with valid token in `.env`

## Development Commands

```bash
# Install for development
pip install -e .

# Run main test suite
python test_sdk.py

# Run specific tests
python test_rate_limit_handling.py    # Rate limit and retry tests
python test_improved_prompt.py        # Prompt processing tests

# Run examples
python examples/basic_chat.py

# Documentation (requires mkdocs)
mkdocs serve                          # Local preview
mkdocs gh-deploy                      # Deploy to GitHub Pages
```

## Architecture

### Core API Flow

1. **Submit task**: `POST /chatCompletion` → returns task ID as string
2. **Poll for result**: `POST /chatResult` → check `message` field for status
3. **Return result**: Convert to OpenAI-compatible `ChatCompletion` object

### Task Status Detection (`resources/chat.py:_wait_for_result`)

**Critical**: Status is determined by `message` field, NOT `code`:
- `"AI任务处理完成"` → success (validate answer length > 10)
- `"AI任务处理失败"` → failed (check for rate limit in answer text)
- `"AI任务处理中"` / `"AI任务待处理"` → still processing

Rate limit detection (line 252-261): checks for "账号达到使用限制", "限制", "quota", or "rate limit" in error message.

### Polling Parameters

| Task Type | Max Retries | Interval | Initial Wait |
|-----------|-------------|----------|--------------|
| Regular   | 60          | 2s       | 0            |
| Image Gen | 100         | 10s      | 30s          |

### Module Organization

```
ai_sdk/
├── client.py           # AIClient, HTTP handling, retry config
├── exceptions.py       # Exception hierarchy
├── _utils.py           # Message extraction, model name mapping
├── resources/chat.py   # Main logic: create(), _wait_for_result()
├── resources/tasks.py  # Task retrieval API
└── types/chat.py       # Pydantic models (ChatCompletion, ChatMessage, etc.)
```

## API Response Quirks

**Task Creation** (`/chatCompletion`):
```json
{"code": 0, "message": "success", "data": "1234567890"}  // data is task_id as STRING
```

**Task Result** (`/chatResult`):
```json
{"code": 0, "message": "AI任务处理完成", "answer": "..."}  // status in message, NOT code
```

### Known Quirks

1. **Task ID conversion**: API returns string, must convert to int for polling (`chat.py:125`)
2. **Answer validation**: Only valid if `len(answer.strip()) > 10` (`chat.py:268`)
3. **Token usage**: Not provided by backend, SDK returns zeros
4. **Default base URL**: `http://156.254.5.245:8088/api/v1` (`client.py:76`)

## Configuration

```env
AI_API_TOKEN=spsw.your_token_here    # Required
AI_API_BASE_URL=http://...           # Optional
AI_API_TIMEOUT=30                    # Optional
```

**Rate limit retry config:**
```python
AIClient(retry_on_rate_limit=True, max_retries=3, retry_delay=5.0)
```

## Exception Hierarchy

All exceptions inherit from `AIAPIError`:
- `AuthenticationError` - Token invalid/missing
- `InvalidRequestError` - Bad parameters
- `RateLimitError` - Rate limit hit (supports auto-retry)
- `APIConnectionError` - Network issues
- `TimeoutError` - Request timeout

## Code Conventions

- Google-style docstrings
- User-friendly Chinese error messages
- Private methods prefixed with `_`
- Update `__version__` in `__init__.py` for releases
