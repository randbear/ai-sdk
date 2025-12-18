"""
基础聊天示例
演示如何使用AI SDK进行简单的对话
"""
import os
import sys

# 添加父目录到路径，以便导入ai_sdk
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_sdk import AIClient, ChatMessage
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    """基础聊天示例"""

    # 初始化客户端
    # 确保已经设置了环境变量 AI_API_TOKEN 和 AI_API_BASE_URL
    # 或者在.env文件中配置
    client = AIClient()

    try:
        print("=" * 50)
        print("AI SDK 基础聊天示例")
        print("=" * 50)

        # 示例1: 简单问答
        print("\n[示例1] 简单问答")
        print("-" * 50)

        response = client.chat.completions.create(
            model="yuanbao",  # 使用元宝模型
            messages=[{"role": "user", "content": "什么是SEO？请简单解释一下"}],
        )

        print(f"问题: 什么是SEO？请简单解释一下")
        print(f"回答: {response.choices[0].message.content}")
        print(f"任务ID: {response.id}")

        # 示例2: 多轮对话
        print("\n[示例2] 多轮对话")
        print("-" * 50)

        messages = [
            ChatMessage(role="system", content="你是一个专业的Python编程助手"),
            ChatMessage(role="user", content="Python中的装饰器是什么？"),
        ]

        response = client.chat.completions.create(model="yuanbao", messages=messages)

        print("对话历史:")
        for msg in messages:
            print(f"  [{msg.role}]: {msg.content}")
        print(f"回答: {response.choices[0].message.content}")

        # 示例3: 使用gemini模型
        print("\n[示例3] 使用Gemini模型")
        print("-" * 50)

        response = client.chat.completions.create(
            model="gemini",
            messages=[{"role": "user", "content": "介绍一下武汉这座城市"}],
        )

        print(f"问题: 介绍一下武汉这座城市")
        print(f"回答: {response.choices[0].message.content}")

        # 示例4: 启用深度研究
        print("\n[示例4] 启用深度研究")
        print("-" * 50)

        response = client.chat.completions.create(
            model="yuanbao",
            messages=[{"role": "user", "content": "人工智能的发展趋势"}],
            deep_research=True,  # 启用深度研究
        )

        print(f"问题: 人工智能的发展趋势")
        print(f"回答: {response.choices[0].message.content}")

    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback

        traceback.print_exc()

    finally:
        # 关闭客户端
        client.close()


if __name__ == "__main__":
    main()
