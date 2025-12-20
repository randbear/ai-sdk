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

    def __init__(
        self,
        message: str = "API 请求配额已用尽",
        status_code: Optional[int] = None,
        response: Optional[dict] = None,
    ):
        # 添加友好的建议
        friendly_message = f"{message}\n\n"
        friendly_message += "💡 建议：\n"
        friendly_message += "  1. 稍后重试（建议等待几分钟）\n"
        friendly_message += "  2. 检查账号配额使用情况\n"
        friendly_message += "  3. 联系服务提供商增加配额\n"
        friendly_message += "  4. 或在初始化时启用自动重试：\n"
        friendly_message += "     client = AIClient(retry_on_rate_limit=True, max_retries=3)"

        super().__init__(friendly_message, status_code, response)


class TimeoutError(AIAPIError):
    """请求超时错误"""

    pass
