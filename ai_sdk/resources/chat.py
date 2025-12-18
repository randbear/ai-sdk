"""
Chat资源模块
实现类似OpenAI的chat.completions接口
"""
import logging
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
        }

        logger.info(f"Creating chat completion with model: {model}")
        logger.debug(f"Request data: {request_data}")

        # 调用API
        response = self._client._post("/chatCompletion", json=request_data)

        # 解析响应
        task_id = response.get("data", {}).get("id")
        if not task_id:
            raise InvalidRequestError("API响应中缺少任务ID")

        # 验证并转换任务ID为整数
        try:
            task_id_int = int(task_id)
        except (ValueError, TypeError) as e:
            raise InvalidRequestError(f"无效的任务ID格式: {task_id}") from e

        logger.info(f"Chat completion created, task_id: {task_id_int}")

        # 等待结果（轮询）
        return self._wait_for_result(task_id_int, model)

    def _wait_for_result(
        self, task_id: int, model: str, max_retries: int = 60, interval: int = 2
    ) -> ChatCompletion:
        """
        等待任务完成并获取结果

        Args:
            task_id: 任务ID（整数）
            model: 模型名称
            max_retries: 最大重试次数，默认60次
            interval: 重试间隔（秒），默认2秒

        Returns:
            ChatCompletion对象

        Raises:
            TimeoutError: 超时错误
            AIAPIError: API调用错误
        """
        import time

        logger.info(f"Waiting for task result: {task_id}")

        for retry in range(max_retries):
            try:
                # 查询任务结果
                result_response = self._client._post(
                    "/chatResult", json={"id": task_id}
                )

                data = result_response.get("data", {})
                status = data.get("status")

                # 检查status字段是否存在
                if status is None:
                    logger.warning(f"Task {task_id} response missing status field")
                    time.sleep(interval)
                    continue

                # 检查任务完成（字符串或数字格式）
                if status == "completed" or status == 2:
                    # 任务完成
                    content = data.get("answer")
                    if content is None:
                        logger.warning(f"Task {task_id} completed but missing 'answer' field")
                        content = ""

                    logger.info(f"Task {task_id} completed")

                    # 构造ChatCompletion响应
                    return ChatCompletion(
                        id=str(task_id),
                        object="chat.completion",
                        created=get_timestamp(),
                        model=model,
                        choices=[
                            Choice(
                                index=0,
                                message=ChatMessage(role="assistant", content=content),
                                finish_reason="stop",
                            )
                        ],
                        usage=Usage(
                            prompt_tokens=0, completion_tokens=0, total_tokens=0
                        ),
                    )

                # 检查任务失败
                elif status == "failed" or status == 3:
                    # 任务失败
                    error_msg = data.get("error") or data.get("message") or "任务执行失败"
                    logger.error(f"Task {task_id} failed: {error_msg}")
                    raise InvalidRequestError(f"任务执行失败: {error_msg}")

                # 处理中状态（pending, processing, running等）
                elif status in ["pending", "processing", "running", 0, 1]:
                    logger.debug(
                        f"Task {task_id} status: {status}, retry {retry + 1}/{max_retries}"
                    )
                    time.sleep(interval)

                # 未知状态
                else:
                    logger.warning(f"Task {task_id} unknown status: {status}, will retry")
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
