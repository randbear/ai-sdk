"""
AI SDK 异步客户端

提供异步包装器，用于在 asyncio 环境中使用 AI SDK。
支持自动重试间歇性失败、System Prompt 自动补全等功能。

示例用法:
    ```python
    from ai_sdk import AsyncAIClient

    client = AsyncAIClient()

    # 异步生成文本
    response = await client.generate(
        system="You are a helpful assistant.",
        user="Hello!"
    )
    print(response.text)
    ```
"""

import asyncio
import concurrent.futures
import logging
import re
from typing import Optional, List
from dataclasses import dataclass

from .client import AIClient
from .types.chat import ChatMessage

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """LLM 响应数据类"""
    text: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0


class AsyncAIClient:
    """
    AI SDK 异步客户端

    在 asyncio 环境中使用 AI SDK 的包装器，提供以下增强功能：
    - 异步 API
    - 自动重试间歇性失败（"任务执行失败"错误）
    - Gemini 模型 System Prompt 自动补全
    - 成本估算
    - Markdown 内容提取

    示例:
        ```python
        from ai_sdk import AsyncAIClient

        async def main():
            client = AsyncAIClient(model="gemini")

            response = await client.generate(
                system="You are helpful.",
                user="What is Python?"
            )
            print(response.text)
        ```
    """

    # Gemini 是推荐的文本生成模型
    DEFAULT_MODEL = "gemini"

    def __init__(
        self,
        api_token: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 120,
        max_retries: int = 3,
        retry_on_rate_limit: bool = True,
        auto_system_prompt: bool = True,
    ):
        """
        初始化异步客户端

        Args:
            api_token: API Token，不提供则从 AI_API_TOKEN 环境变量读取
            model: 模型名称 (yuanbao, gemini, deepseek, gpt)
            base_url: 自定义 API 基础 URL
            timeout: 请求超时时间（秒）
            max_retries: 间歇性失败最大重试次数
            retry_on_rate_limit: 遇到限流时是否重试
            auto_system_prompt: 是否自动为 Gemini 添加 System Prompt
        """
        self._model = model or self.DEFAULT_MODEL
        self.timeout = timeout
        self.max_retries = max_retries
        self.auto_system_prompt = auto_system_prompt

        # 初始化同步客户端
        self.client = AIClient(
            api_token=api_token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_on_rate_limit=retry_on_rate_limit,
        )

        logger.info(f"AsyncAIClient initialized with model: {self._model}")

    @property
    def model(self) -> str:
        """获取当前模型名称"""
        return self._model

    async def generate(
        self,
        system: str,
        user: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        priority: int = 50,
    ) -> str:
        """
        异步生成文本响应

        Args:
            system: System Prompt
            user: 用户消息
            max_tokens: 最大生成 token 数（AI SDK 不直接支持，仅作记录）
            temperature: 采样温度（AI SDK 不直接支持，仅作记录）
            priority: 任务优先级

        Returns:
            生成的文本内容
        """
        response = await self.generate_with_metadata(
            system=system,
            user=user,
            max_tokens=max_tokens,
            temperature=temperature,
            priority=priority,
        )
        return response.text

    async def generate_with_metadata(
        self,
        system: str,
        user: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        priority: int = 50,
    ) -> LLMResponse:
        """
        异步生成文本响应，包含元数据

        Args:
            system: System Prompt
            user: 用户消息
            max_tokens: 最大生成 token 数
            temperature: 采样温度
            priority: 任务优先级

        Returns:
            LLMResponse 包含文本和元数据
        """
        # 构建消息列表
        messages = self._build_messages(system, user)

        # 重试逻辑
        last_error = None

        for attempt in range(self.max_retries):
            try:
                # 在线程池中执行同步调用
                def _sync_call():
                    return self.client.chat.completions.create(
                        model=self._model,
                        messages=messages,
                        priority=priority,
                    )

                loop = asyncio.get_running_loop()
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    response = await asyncio.wait_for(
                        loop.run_in_executor(executor, _sync_call),
                        timeout=self.timeout,
                    )

                # 提取响应
                if not response.choices or len(response.choices) == 0:
                    raise ValueError("AI SDK 返回空结果")

                text = response.choices[0].message.content

                # 提取 usage
                input_tokens = 0
                output_tokens = 0
                if response.usage:
                    input_tokens = response.usage.prompt_tokens
                    output_tokens = response.usage.completion_tokens

                return LLMResponse(
                    text=text,
                    model=response.model or self._model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost=self._estimate_cost(input_tokens, output_tokens),
                )

            except asyncio.TimeoutError:
                logger.error(f"请求超时 ({self.timeout}s)")
                raise
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    # 检查是否为可重试的间歇性失败
                    error_str = str(e).lower()
                    if "任务执行失败" in error_str or "task" in error_str:
                        logger.warning(
                            f"间歇性失败 (尝试 {attempt + 1}/{self.max_retries})，正在重试..."
                        )
                        await asyncio.sleep(1)
                        continue
                logger.error(f"AI SDK 错误: {e}")
                raise

        raise last_error or RuntimeError("重试后仍然失败")

    def _build_messages(self, system: str, user: str) -> List[ChatMessage]:
        """
        构建消息列表

        Gemini 模型要求必须有 System Prompt，否则请求会失败。
        如果启用 auto_system_prompt，会自动添加默认值。

        Args:
            system: System Prompt
            user: 用户消息

        Returns:
            ChatMessage 列表
        """
        messages = []

        if system:
            messages.append(ChatMessage(role="system", content=system))
        elif self.auto_system_prompt and "gemini" in self._model.lower():
            # Gemini 要求必须有 system prompt
            messages.append(ChatMessage(role="system", content="You are a helpful assistant."))

        messages.append(ChatMessage(role="user", content=user))
        return messages

    def _estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        估算成本

        根据模型类型估算 token 费用。
        注意：AI SDK 可能有自己的定价，这只是基于底层模型的估算。

        Args:
            input_tokens: 输入 token 数
            output_tokens: 输出 token 数

        Returns:
            估算成本（美元）
        """
        model_lower = self._model.lower()

        if "deepseek" in model_lower:
            # DeepSeek: $0.14/1M input, $0.28/1M output
            input_cost = input_tokens * 0.14 / 1_000_000
            output_cost = output_tokens * 0.28 / 1_000_000
        elif "gpt" in model_lower:
            # GPT-4o: $2.5/1M input, $10/1M output
            input_cost = input_tokens * 2.5 / 1_000_000
            output_cost = output_tokens * 10.0 / 1_000_000
        elif "gemini" in model_lower:
            # Gemini Pro: $0.5/1M input, $1.5/1M output
            input_cost = input_tokens * 0.5 / 1_000_000
            output_cost = output_tokens * 1.5 / 1_000_000
        else:
            # 默认（yuanbao 等）
            input_cost = input_tokens * 0.1 / 1_000_000
            output_cost = output_tokens * 0.3 / 1_000_000

        return input_cost + output_cost

    async def generate_markdown(
        self,
        system: str,
        user: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """
        生成 Markdown 格式响应

        注意：Gemini 模型不能可靠地输出 Markdown 格式。
        此方法会添加格式提示，但模型可能忽略。
        如需可靠的 Markdown 输出，建议使用 Claude 或 GPT-4。

        Args:
            system: System Prompt
            user: 用户消息
            max_tokens: 最大生成 token 数
            temperature: 采样温度

        Returns:
            提取后的响应文本（可能没有正确的 Markdown 格式）
        """
        # 添加 Markdown 格式提示
        markdown_system = f"""{system}

Please format your response with clear structure:
- Use headers to organize sections
- Use bullet points for lists
- Emphasize key terms"""

        response = await self.generate(
            system=markdown_system,
            user=user,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return self._extract_markdown(response)

    def _extract_markdown(self, text: str) -> str:
        """
        从 LLM 响应中提取 Markdown 内容

        模型经常添加前缀如 'Markdown', 'Output:' 等。
        此方法移除这些前缀并从代码块中提取内容。

        Args:
            text: 原始 LLM 响应

        Returns:
            清理后的 Markdown 内容
        """
        text = text.strip()

        # 策略1：从 markdown 代码块中提取
        match = re.search(r"```(?:markdown|md)?\s*([\s\S]*?)\s*```", text)
        if match:
            return match.group(1).strip()

        # 策略2：移除已知前缀
        prefixes = [
            "Markdown",
            "markdown",
            "MD",
            "md",
            "Output:",
            "output:",
            "Response:",
            "response:",
        ]
        for prefix in prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):].lstrip()
                break

        return text

    async def is_available(self) -> bool:
        """
        检查服务是否可用

        Returns:
            True 如果可用
        """
        try:
            return self.client is not None
        except Exception:
            return False

    def close(self):
        """关闭客户端"""
        if self.client:
            self.client.close()

    def __repr__(self) -> str:
        return f"<AsyncAIClient model='{self._model}'>"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
