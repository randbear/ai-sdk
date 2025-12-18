"""
AI SDK - 兼容OpenAI SDK的AI API客户端

示例用法:
    ```python
    from ai_sdk import AIClient

    # 初始化客户端
    client = AIClient(
        api_token="spsw.your_token",
        base_url="http://your_server/api/v1"
    )

    # 发起chat请求
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "什么是SEO?"}
        ]
    )

    print(response.choices[0].message.content)
    ```
"""

__version__ = "0.1.0"

from .client import AIClient
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

__all__ = [
    # 版本
    "__version__",
    # 客户端
    "AIClient",
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
]
