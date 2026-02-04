"""
AI SDK 辅助工具

提供文本处理、成本估算等辅助功能。
"""

import re
import json
from typing import Any, Dict, Optional


def extract_markdown(text: str) -> str:
    """
    从 LLM 响应中提取 Markdown 内容

    模型（特别是 Gemini）经常在输出前添加前缀如 'Markdown', 'Output:' 等，
    或将内容包裹在代码块中。此方法清理这些并返回纯净的内容。

    Args:
        text: 原始 LLM 响应

    Returns:
        清理后的内容

    示例:
        >>> extract_markdown("Markdown\\n# Hello World")
        "# Hello World"

        >>> extract_markdown("```markdown\\n# Hello\\n```")
        "# Hello"
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
        "Here is",
        "Here's",
    ]
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].lstrip()
            # 移除可能的冒号和换行
            if text.startswith(":"):
                text = text[1:].lstrip()
            break

    return text


def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """
    从 LLM 响应中提取 JSON 内容

    模型可能在 JSON 前后添加额外文本或将其包裹在代码块中。
    此方法尝试多种策略提取有效的 JSON。

    Args:
        text: 原始 LLM 响应

    Returns:
        解析后的 JSON 字典，如果解析失败则返回 None

    示例:
        >>> extract_json('JSON\\n{"name": "test"}')
        {"name": "test"}

        >>> extract_json('```json\\n{"key": "value"}\\n```')
        {"key": "value"}
    """
    text = text.strip()

    # 策略1：从 JSON 代码块中提取
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 策略2：移除已知前缀后解析
    prefixes = ["JSON", "json", "Output:", "output:", "Response:", "response:"]
    clean_text = text
    for prefix in prefixes:
        if clean_text.startswith(prefix):
            clean_text = clean_text[len(prefix):].lstrip()
            break

    # 策略3：查找第一个 { 和最后一个 }
    start = clean_text.find("{")
    end = clean_text.rfind("}")

    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(clean_text[start : end + 1])
        except json.JSONDecodeError:
            pass

    # 策略4：查找数组 [ ]
    start = clean_text.find("[")
    end = clean_text.rfind("]")

    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(clean_text[start : end + 1])
        except json.JSONDecodeError:
            pass

    # 策略5：直接尝试解析
    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        return None


def estimate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> float:
    """
    估算 API 调用成本

    根据模型类型和 token 数量估算费用。
    注意：这是基于公开定价的估算，AI SDK 可能有不同的计费方式。

    Args:
        model: 模型名称
        input_tokens: 输入 token 数
        output_tokens: 输出 token 数

    Returns:
        估算成本（美元）

    定价参考（2026年）:
        - DeepSeek: $0.14/1M input, $0.28/1M output
        - GPT-4o: $2.5/1M input, $10/1M output
        - Gemini Pro: $0.5/1M input, $1.5/1M output
        - 默认（yuanbao 等）: $0.1/1M input, $0.3/1M output
    """
    model_lower = model.lower()

    if "deepseek" in model_lower:
        input_cost = input_tokens * 0.14 / 1_000_000
        output_cost = output_tokens * 0.28 / 1_000_000
    elif "gpt" in model_lower:
        input_cost = input_tokens * 2.5 / 1_000_000
        output_cost = output_tokens * 10.0 / 1_000_000
    elif "gemini" in model_lower:
        input_cost = input_tokens * 0.5 / 1_000_000
        output_cost = output_tokens * 1.5 / 1_000_000
    else:
        # 默认定价（yuanbao 等自定义模型）
        input_cost = input_tokens * 0.1 / 1_000_000
        output_cost = output_tokens * 0.3 / 1_000_000

    return input_cost + output_cost


def count_tokens_approx(text: str) -> int:
    """
    粗略估算文本的 token 数

    使用简单的启发式方法：
    - 英文：约 4 字符 = 1 token
    - 中文：约 1.5 字符 = 1 token

    Args:
        text: 要估算的文本

    Returns:
        估算的 token 数

    注意：这只是粗略估算，实际 token 数取决于具体的 tokenizer。
    """
    # 统计中文字符
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    # 非中文字符
    other_chars = len(text) - chinese_chars

    # 估算 token 数
    chinese_tokens = chinese_chars / 1.5
    other_tokens = other_chars / 4

    return int(chinese_tokens + other_tokens)


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """
    截断文本到大约指定的 token 数

    Args:
        text: 要截断的文本
        max_tokens: 最大 token 数

    Returns:
        截断后的文本
    """
    current_tokens = count_tokens_approx(text)

    if current_tokens <= max_tokens:
        return text

    # 计算需要保留的字符比例
    ratio = max_tokens / current_tokens
    target_len = int(len(text) * ratio * 0.95)  # 留 5% 余量

    return text[:target_len] + "..."
