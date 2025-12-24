"""
Chat资源模块
实现类似OpenAI的chat.completions接口
"""
import logging
import time
from typing import TYPE_CHECKING, List, Optional

from ..types.chat import (
    ChatCompletion,
    ChatCompletionRequest,
    ChatMessage,
    Choice,
    Usage,
)
from .._utils import (
    extract_question_from_messages,
    get_timestamp,
    model_name_to_type,
)
from ..exceptions import (
    InvalidRequestError,
    RateLimitError,
    APIConnectionError,
    TimeoutError as AITimeoutError,
    AIAPIError,
)

if TYPE_CHECKING:
    from ..client import AIClient

logger = logging.getLogger(__name__)


class Completions:
    """Chat completions资源类"""

    def __init__(self, client: "AIClient"):
        self._client = client

    def create(
        self,
        model: str = "yuanbao",
        messages: Optional[List[ChatMessage]] = None,
        image_url: Optional[str] = None,
        image_data: Optional[str] = None,
        deep_research: bool = False,
        generate_image: bool = False,
        priority: int = 0,
        **kwargs,
    ) -> ChatCompletion:
        """
        创建chat completion（兼容OpenAI SDK接口）

        Args:
            model: 模型名称，可选 "yuanbao" 或 "gemini"，默认 "yuanbao"
            messages: 对话消息列表
            image_url: 图片URL（可选）
            image_data: 图片Base64数据（可选）
            deep_research: 是否进行深度研究，默认False
            generate_image: 是否生成图片，默认False
            priority: 任务优先级，默认0
            **kwargs: 其他参数

        Returns:
            ChatCompletion对象

        Raises:
            InvalidRequestError: 参数错误
            AIAPIError: API调用错误
        """
        # 参数验证
        if not messages or len(messages) == 0:
            raise InvalidRequestError("messages参数不能为空")

        # 验证 image_url 和 image_data 不能同时使用
        if image_url and image_data:
            raise InvalidRequestError(
                "image_url 和 image_data 不能同时提供，请只使用其中一个"
            )

        # 转换messages为字典列表（如果传入的是ChatMessage对象）
        if isinstance(messages[0], ChatMessage):
            messages_list = messages
        else:
            # 如果传入的是字典，转换为ChatMessage对象
            messages_list = [
                ChatMessage(**msg) if isinstance(msg, dict) else msg
                for msg in messages
            ]

        # 从messages中提取question
        question = extract_question_from_messages(messages_list)

        # 构建请求参数
        request_data = {
            "type": model_name_to_type(model),
            "question": question,
            "imageUrl": image_url or "",
            "imageData": image_data or "",
            "deepResearch": 1 if deep_research else 0,
            "generateImage": 1 if generate_image else 0,
            "priority": priority,
        }

        logger.info(f"Creating chat completion with model: {model}")
        logger.debug(f"Request data: {request_data}")

        # 调用API
        response = self._client._post("/chatCompletion", json=request_data)

        # 检查响应格式和错误
        code = response.get("code")
        message = response.get("message", "")

        # 如果返回错误码（成功时 code 为 0）
        if code != 0:
            error_msg = f"API请求失败: {message}" if message else "API请求失败"
            raise InvalidRequestError(error_msg)

        # 解析响应数据 - data 直接就是任务ID
        task_id = response.get("data")
        if not task_id:
            raise InvalidRequestError("API响应中缺少任务ID")

        # 验证并转换任务ID为整数
        try:
            task_id_int = int(task_id)
        except (ValueError, TypeError) as e:
            raise InvalidRequestError(f"无效的任务ID格式: {task_id}") from e

        logger.info(f"Chat completion created, task_id: {task_id_int}")

        # 等待结果（轮询，带重试机制）
        return self._wait_for_result_with_retry(task_id_int, model, generate_image)

    def _wait_for_result_with_retry(
        self, task_id: int, model: str, is_image_generation: bool = False
    ) -> ChatCompletion:
        """
        带重试机制的任务等待

        Args:
            task_id: 任务ID
            model: 模型名称
            is_image_generation: 是否为图片生成任务

        Returns:
            ChatCompletion对象

        Raises:
            RateLimitError: 达到限流限制
            其他异常: 任务执行失败
        """
        max_retry_attempts = self._client.max_retries
        retry_on_rate_limit = self._client.retry_on_rate_limit
        retry_delay = self._client.retry_delay

        # 图片生成使用不同的轮询参数
        if is_image_generation:
            max_retries = 100  # 图片生成：100次重试
            interval = 10      # 图片生成：10秒间隔
            logger.info(f"Image generation mode: max_retries={max_retries}, interval={interval}s")
        else:
            max_retries = 60   # 普通任务：60次重试
            interval = 2       # 普通任务：2秒间隔

        for attempt in range(max_retry_attempts + 1):
            try:
                # 尝试等待结果
                return self._wait_for_result(
                    task_id, model, max_retries, interval, is_image_generation
                )

            except RateLimitError as e:
                # 如果不启用限流重试，或已达最大重试次数，直接抛出
                if not retry_on_rate_limit or attempt >= max_retry_attempts:
                    logger.error(f"Rate limit reached, no more retries")
                    raise

                # 计算退避时间（指数退避）
                wait_time = retry_delay * (2**attempt)
                logger.warning(
                    f"⚠️  遇到限流错误，{wait_time:.1f}秒后进行第 {attempt + 1}/{max_retry_attempts} 次重试..."
                )
                logger.warning(f"原始错误: {e.response.get('original_error') if e.response else 'unknown'}")

                # 等待后重试
                time.sleep(wait_time)

            except Exception:
                # 其他错误不重试，直接抛出
                raise

        # 理论上不会到这里
        raise RateLimitError("达到最大重试次数，请求仍然失败")

    def _wait_for_result(
        self, task_id: int, model: str, max_retries: int = 60, interval: int = 2,
        is_image_generation: bool = False
    ) -> ChatCompletion:
        """
        等待任务完成并获取结果

        Args:
            task_id: 任务ID（整数）
            model: 模型名称
            max_retries: 最大重试次数，默认60次
            interval: 重试间隔（秒），默认2秒
            is_image_generation: 是否为图片生成任务，默认False

        Returns:
            ChatCompletion对象

        Raises:
            TimeoutError: 超时错误
            AIAPIError: API调用错误
        """
        import time

        logger.info(f"Waiting for task result: {task_id}")

        # 如果是图片生成任务，首次查询前等待30秒
        if is_image_generation and max_retries > 0:
            logger.info(f"Image generation task detected, waiting 30 seconds before first check...")
            time.sleep(30)

        for retry in range(max_retries):
            try:
                # 查询任务结果
                result_response = self._client._post(
                    "/chatResult", json={"id": task_id}
                )

                # 获取响应字段
                code = result_response.get("code")
                message = result_response.get("message", "")
                answer = result_response.get("answer", "")

                # 检查API调用是否成功
                if code != 0:
                    # code != 0 表示API调用失败（不是任务失败）
                    logger.warning(f"API call failed (code={code}): {message}")
                    time.sleep(interval)
                    continue

                # code == 0，通过 message 判断任务状态

                # 1. 检查任务失败
                if message == "AI任务处理失败":
                    error_msg = answer if answer else "任务执行失败"
                    logger.error(f"Task {task_id} failed: {error_msg}")

                    # 识别限流错误
                    if (
                        "账号达到使用限制" in error_msg
                        or "限制" in error_msg
                        or "quota" in error_msg.lower()
                        or "rate limit" in error_msg.lower()
                    ):
                        raise RateLimitError(
                            message=error_msg,
                            response={"task_id": task_id, "original_error": error_msg},
                        )

                    raise InvalidRequestError(f"任务执行失败: {error_msg}")

                # 2. 检查任务完成
                if message == "AI任务处理完成":
                    # 验证是否有有效答案（根据文档：长度>10）
                    has_result = bool(answer and answer.strip() and len(answer.strip()) > 10)
                    if has_result:
                        logger.info(f"Task {task_id} completed successfully")
                        # 构造ChatCompletion响应
                        return ChatCompletion(
                            id=str(task_id),
                            object="chat.completion",
                            created=get_timestamp(),
                            model=model,
                            choices=[
                                Choice(
                                    index=0,
                                    message=ChatMessage(role="assistant", content=answer),
                                    finish_reason="stop",
                                )
                            ],
                            usage=Usage(
                                prompt_tokens=0, completion_tokens=0, total_tokens=0
                            ),
                        )
                    else:
                        logger.warning(f"Task {task_id} completed but answer is empty or too short")
                        # 可能需要继续等待
                        time.sleep(interval)
                        continue

                # 3. 任务处理中（"AI任务待处理" 或 "AI任务处理中"）
                if "处理中" in message or "待处理" in message:
                    logger.debug(f"Task {task_id}: {message}, retry {retry + 1}/{max_retries}")
                    time.sleep(interval)
                    continue

                # 4. 兜底：有答案就返回（文档中提到的情况）
                has_result = bool(answer and answer.strip() and len(answer.strip()) > 10)
                if has_result:
                    logger.info(f"Task {task_id} has result (message: {message})")
                    return ChatCompletion(
                        id=str(task_id),
                        object="chat.completion",
                        created=get_timestamp(),
                        model=model,
                        choices=[
                            Choice(
                                index=0,
                                message=ChatMessage(role="assistant", content=answer),
                                finish_reason="stop",
                            )
                        ],
                        usage=Usage(
                            prompt_tokens=0, completion_tokens=0, total_tokens=0
                        ),
                    )

                # 5. 未知状态，继续等待
                logger.warning(f"Task {task_id} unknown message: {message}, will retry")
                time.sleep(interval)

            except InvalidRequestError:
                # 请求参数错误，立即抛出，不重试
                raise
            except (APIConnectionError, AITimeoutError) as e:
                # 网络错误或超时，可以重试
                if retry == max_retries - 1:
                    raise
                logger.warning(f"Network error checking task status, will retry: {str(e)}")
                time.sleep(interval)
            except AIAPIError as e:
                # 其他API错误，可以重试
                if retry == max_retries - 1:
                    raise
                logger.warning(f"API error checking task status, will retry: {str(e)}")
                time.sleep(interval)
            except Exception as e:
                # 未知错误，立即抛出，不重试
                logger.error(f"Unexpected error in task polling: {str(e)}")
                raise

        # 超时
        raise AITimeoutError(f"任务{task_id}等待超时，已重试{max_retries}次")


class Chat:
    """Chat资源类"""

    def __init__(self, client: "AIClient"):
        self.completions = Completions(client)
