"""
AI SDK - 兼容OpenAI SDK的AI API客户端

同步客户端用法:
    ```python
    from ai_sdk import AIClient

    client = AIClient(api_token="spsw.your_token")

    response = client.chat.completions.create(
        model="gemini",
        messages=[
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "什么是SEO?"}
        ]
    )
    print(response.choices[0].message.content)
    ```

异步客户端用法:
    ```python
    from ai_sdk import AsyncAIClient

    async def main():
        client = AsyncAIClient(model="gemini")
        response = await client.generate(
            system="You are helpful.",
            user="什么是SEO?"
        )
        print(response)
    ```
"""

__version__ = "0.2.0"

from .client import AIClient
from .async_client import AsyncAIClient, LLMResponse
from .exceptions import (
    AIAPIError,
    AuthenticationError,
    InvalidRequestError,
    APIConnectionError,
    RateLimitError,
    TimeoutError,
)
from .types import (
    ChatMessage,
    ChatCompletion,
    ChatCompletionRequest,
    Choice,
    Usage,
)
from .helpers import (
    extract_markdown,
    extract_json,
    estimate_cost,
    count_tokens_approx,
    truncate_to_tokens,
)

__all__ = [
    # 版本
    "__version__",
    # 客户端
    "AIClient",
    "AsyncAIClient",
    "LLMResponse",
    # 异常
    "AIAPIError",
    "AuthenticationError",
    "InvalidRequestError",
    "APIConnectionError",
    "RateLimitError",
    "TimeoutError",
    # 类型
    "ChatMessage",
    "ChatCompletion",
    "ChatCompletionRequest",
    "Choice",
    "Usage",
    # 辅助函数
    "extract_markdown",
    "extract_json",
    "estimate_cost",
    "count_tokens_approx",
    "truncate_to_tokens",
]
