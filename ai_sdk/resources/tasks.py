"""
任务管理资源模块
提供任务查询等功能
"""
import logging
from typing import TYPE_CHECKING, Optional, Dict, Any

from ..exceptions import InvalidRequestError

if TYPE_CHECKING:
    from ..client import AIClient

logger = logging.getLogger(__name__)


class Tasks:
    """任务管理资源类"""

    def __init__(self, client: "AIClient"):
        self._client = client

    def retrieve(self, task_id: str) -> Dict[str, Any]:
        """
        查询任务结果

        Args:
            task_id: 任务ID

        Returns:
            任务结果字典，包含status, answer等字段

        Raises:
            InvalidRequestError: 参数错误
            AIAPIError: API调用错误
        """
        if not task_id:
            raise InvalidRequestError("task_id不能为空")

        # 验证并转换任务ID为整数
        try:
            task_id_int = int(task_id)
        except (ValueError, TypeError) as e:
            raise InvalidRequestError(f"无效的任务ID格式: {task_id}") from e

        logger.info(f"Retrieving task: {task_id_int}")

        response = self._client._post("/chatResult", json={"id": task_id_int})

        data = response.get("data", {})
        logger.debug(f"Task {task_id} data: {data}")

        return data

    def batch_retrieve(self, task_ids: list[str]) -> list[Dict[str, Any]]:
        """
        批量查询任务结果

        Args:
            task_ids: 任务ID列表

        Returns:
            任务结果列表

        Raises:
            InvalidRequestError: 参数错误
            AIAPIError: API调用错误
        """
        if not task_ids or len(task_ids) == 0:
            raise InvalidRequestError("task_ids不能为空")

        logger.info(f"Batch retrieving {len(task_ids)} tasks")

        # 注意：这里假设API支持批量查询，根据实际API调整
        # 如果API不支持批量查询，可以循环调用单个查询
        results = []
        for task_id in task_ids:
            try:
                result = self.retrieve(task_id)
                results.append(result)
            except Exception as e:
                logger.warning(f"Failed to retrieve task {task_id}: {str(e)}")
                results.append({"id": task_id, "error": str(e)})

        return results
