"""
AI SDK 异常定义
定义SDK中可能出现的各种异常类型
"""
from typing import Optional


class AIAPIError(Exception):
    """AI API 基础异常类"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[dict] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(AIAPIError):
    """认证错误 - Token无效或缺失"""

    pass


class InvalidRequestError(AIAPIError):
    """请求参数错误"""

    pass


class APIConnectionError(AIAPIError):
    """API连接错误"""

    pass


class RateLimitError(AIAPIError):
    """请求频率限制错误"""

    pass


class TimeoutError(AIAPIError):
    """请求超时错误"""

    pass
