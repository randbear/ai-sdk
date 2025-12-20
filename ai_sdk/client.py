"""
AI SDK核心客户端
提供与API交互的主要接口
"""
import os
import logging
from typing import Optional, Dict, Any
import requests
from dotenv import load_dotenv

from .resources.chat import Chat
from .resources.tasks import Tasks
from .exceptions import (
    AIAPIError,
    AuthenticationError,
    InvalidRequestError,
    APIConnectionError,
    RateLimitError,
    TimeoutError as AITimeoutError,
)

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)


class AIClient:
    """
    AI API客户端

    用法示例:
        ```python
        from ai_sdk import AIClient

        # 方式1: 使用环境变量
        client = AIClient()

        # 方式2: 直接传入参数
        client = AIClient(api_token="spsw.your_token")

        # 发起chat completion请求
        response = client.chat.completions.create(
            model="yuanbao",
            messages=[
                {"role": "user", "content": "你好"}
            ]
        )
        ```
    """

    def __init__(
        self,
        api_token: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 0,
        retry_on_rate_limit: bool = False,
        retry_delay: float = 5.0,
    ):
        """
        初始化AI客户端

        Args:
            api_token: API Token，如果不提供则从环境变量AI_API_TOKEN读取
            base_url: API基础URL（可选），默认使用内置的服务地址
            timeout: 请求超时时间（秒），默认30秒
            max_retries: 最大重试次数，默认0（不重试）
            retry_on_rate_limit: 遇到限流错误时是否自动重试，默认False
            retry_delay: 重试延迟基数（秒），使用指数退避策略，默认5.0秒

        Raises:
            AuthenticationError: Token未提供或无效
        """
        # 默认的 API base URL
        DEFAULT_BASE_URL = "http://156.254.5.245:8088/api/v1"

        # 获取配置
        self.api_token = api_token or os.getenv("AI_API_TOKEN")
        self.base_url = (
            base_url or
            os.getenv("AI_API_BASE_URL") or
            DEFAULT_BASE_URL
        ).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_on_rate_limit = retry_on_rate_limit
        self.retry_delay = retry_delay

        # 验证配置
        if not self.api_token:
            raise AuthenticationError(
                "API Token未提供。请设置AI_API_TOKEN环境变量或在初始化时传入api_token参数"
            )

        # 创建session
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "x-custom-token": self.api_token,
            }
        )

        # 初始化资源
        self.chat = Chat(self)
        self.tasks = Tasks(self)

        logger.info(f"AIClient initialized with base_url: {self.base_url}")

    def _request(
        self,
        method: str,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        发送HTTP请求

        Args:
            method: HTTP方法 (GET, POST等)
            endpoint: API端点 (例如 "/chatCompletion")
            json: JSON请求体
            params: URL查询参数

        Returns:
            API响应的JSON数据

        Raises:
            AuthenticationError: 认证失败
            InvalidRequestError: 请求参数错误
            APIConnectionError: 网络连接错误
            RateLimitError: 请求频率限制
            AITimeoutError: 请求超时
            AIAPIError: 其他API错误
        """
        url = f"{self.base_url}{endpoint}"

        try:
            logger.debug(f"Sending {method} request to {url}")

            response = self.session.request(
                method=method,
                url=url,
                json=json,
                params=params,
                timeout=self.timeout,
            )

            # 记录响应
            logger.debug(
                f"Response status: {response.status_code}, body: {response.text[:200]}"
            )

            # 辅助函数：安全地解析JSON响应
            def safe_json_parse():
                try:
                    return response.json() if response.text else None
                except ValueError:
                    return None

            # 处理HTTP错误
            if response.status_code == 401 or response.status_code == 403:
                raise AuthenticationError(
                    "认证失败，请检查API Token是否正确", status_code=response.status_code
                )
            elif response.status_code == 400:
                raise InvalidRequestError(
                    f"请求参数错误: {response.text}",
                    status_code=response.status_code,
                    response=safe_json_parse(),
                )
            elif response.status_code == 429:
                raise RateLimitError(
                    "请求频率超限，请稍后再试", status_code=response.status_code
                )
            elif response.status_code >= 500:
                raise AIAPIError(
                    f"服务器错误: {response.text}",
                    status_code=response.status_code,
                    response=safe_json_parse(),
                )
            elif response.status_code != 200:
                raise AIAPIError(
                    f"请求失败: {response.text}",
                    status_code=response.status_code,
                    response=safe_json_parse(),
                )

            # 解析响应
            try:
                data = response.json()
            except ValueError:
                raise AIAPIError(f"无法解析API响应: {response.text}")

            # 检查业务错误
            if not data.get("success", True):
                error_msg = data.get("message", "未知错误")
                raise AIAPIError(f"API返回错误: {error_msg}", response=data)

            return data

        except requests.exceptions.Timeout:
            raise AITimeoutError(f"请求超时 ({self.timeout}秒)")
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError(f"网络连接错误: {str(e)}")
        except (AuthenticationError, InvalidRequestError, RateLimitError, AITimeoutError, AIAPIError):
            # 已经是我们定义的异常，直接抛出
            raise
        except Exception as e:
            # 其他未知错误
            raise AIAPIError(f"未知错误: {str(e)}")

    def _post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        发送POST请求

        Args:
            endpoint: API端点
            json: JSON请求体
            params: URL查询参数

        Returns:
            API响应
        """
        return self._request("POST", endpoint, json=json, params=params)

    def _get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        发送GET请求

        Args:
            endpoint: API端点
            params: URL查询参数

        Returns:
            API响应
        """
        return self._request("GET", endpoint, params=params)

    def close(self):
        """关闭客户端，清理资源"""
        self.session.close()
        logger.info("AIClient closed")

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理器"""
        self.close()
