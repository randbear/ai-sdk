"""
内部工具函数
"""
import time
from typing import List
from .types.chat import ChatMessage


def get_timestamp() -> int:
    """获取当前时间戳"""
    return int(time.time())


def extract_question_from_messages(messages: List[ChatMessage]) -> str:
    """
    从消息列表中提取问题内容
    将所有消息合并为一个question字符串

    Args:
        messages: 消息列表

    Returns:
        合并后的问题字符串
    """
    parts = []
    for msg in messages:
        if msg.role == "system":
            parts.append(f"[System]: {msg.content}")
        elif msg.role == "user":
            parts.append(msg.content)
        elif msg.role == "assistant":
            parts.append(f"[Assistant]: {msg.content}")

    return "\n".join(parts)


def model_name_to_type(model: str) -> int:
    """
    将模型名称转换为API需要的type参数

    Args:
        model: 模型名称 "yuanbao" 或 "gemini"

    Returns:
        type参数值: 1-元宝, 2-gemini
    """
    model_mapping = {"yuanbao": 1, "gemini": 2}
    return model_mapping.get(model.lower(), 1)
