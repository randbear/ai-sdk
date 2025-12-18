"""
高级用法示例
演示上下文管理器、任务管理、错误处理等高级功能
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_sdk import AIClient, AIAPIError, AuthenticationError, TimeoutError
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def example_context_manager():
    """示例1: 使用上下文管理器"""
    print("\n[示例1] 使用上下文管理器")
    print("-" * 50)

    # 使用with语句，自动管理客户端资源
    with AIClient() as client:
        response = client.chat.completions.create(
            model="yuanbao",
            messages=[{"role": "user", "content": "你好"}],
        )
        print(f"回答: {response.choices[0].message.content}")
    # 退出with块时自动调用client.close()


def example_task_management():
    """示例2: 任务管理"""
    print("\n[示例2] 任务管理 - 直接查询任务")
    print("-" * 50)

    with AIClient() as client:
        # 首先创建一个任务
        response = client.chat.completions.create(
            model="yuanbao",
            messages=[{"role": "user", "content": "介绍Python语言"}],
        )

        task_id = response.id
        print(f"任务创建成功，ID: {task_id}")

        # 稍后可以通过任务ID查询结果
        task_result = client.tasks.retrieve(task_id)
        print(f"任务状态: {task_result.get('status')}")
        print(f"任务结果: {task_result.get('answer', 'N/A')}")


def example_error_handling():
    """示例3: 错误处理"""
    print("\n[示例3] 错误处理")
    print("-" * 50)

    # 错误1: Token错误
    print("\n测试1: 无效Token")
    try:
        client = AIClient(
            api_token="invalid_token", base_url="http://localhost/api/v1"
        )
        response = client.chat.completions.create(
            model="yuanbao", messages=[{"role": "user", "content": "测试"}]
        )
    except AuthenticationError as e:
        print(f"捕获认证错误: {e}")
    except Exception as e:
        print(f"捕获其他错误: {type(e).__name__}: {e}")

    # 错误2: 参数错误
    print("\n测试2: 空消息列表")
    try:
        with AIClient() as client:
            response = client.chat.completions.create(
                model="yuanbao",
                messages=[],  # 空消息列表
            )
    except AIAPIError as e:
        print(f"捕获API错误: {e}")

    # 错误3: 网络超时
    print("\n测试3: 超时设置")
    try:
        # 设置很短的超时时间
        client = AIClient(timeout=1)
        # 如果API响应较慢，会触发超时
        # response = client.chat.completions.create(
        #     model="yuanbao",
        #     messages=[{"role": "user", "content": "测试"}]
        # )
        print("超时测试（已注释，取消注释测试实际超时）")
    except TimeoutError as e:
        print(f"捕获超时错误: {e}")
    finally:
        client.close()


def example_custom_configuration():
    """示例4: 自定义配置"""
    print("\n[示例4] 自定义配置")
    print("-" * 50)

    # 方式1: 通过参数传入（SDK 已内置默认服务地址）
    client = AIClient(
        api_token="spsw.your_token_here",
        timeout=60,  # 60秒超时
    )

    # 方式2: 通过环境变量（推荐）
    # 在.env文件中设置：
    # AI_API_TOKEN=spsw.your_token
    # 可选：自定义服务地址
    # AI_API_BASE_URL=http://your_custom_server/api/v1

    # client = AIClient()  # 自动从环境变量读取

    print(f"客户端配置:")
    print(f"  Base URL: {client.base_url}")
    print(f"  Timeout: {client.timeout}秒")

    client.close()


def example_batch_requests():
    """示例5: 批量请求"""
    print("\n[示例5] 批量请求")
    print("-" * 50)

    questions = [
        "什么是Python?",
        "什么是JavaScript?",
        "什么是Go语言?",
    ]

    with AIClient() as client:
        responses = []

        for i, question in enumerate(questions, 1):
            print(f"\n处理问题 {i}/{len(questions)}: {question}")
            try:
                response = client.chat.completions.create(
                    model="yuanbao",
                    messages=[{"role": "user", "content": question}],
                )
                responses.append(
                    {
                        "question": question,
                        "answer": response.choices[0].message.content,
                        "task_id": response.id,
                    }
                )
                print(f"回答: {response.choices[0].message.content[:100]}...")
            except Exception as e:
                print(f"错误: {e}")
                responses.append({"question": question, "error": str(e)})

        print(f"\n批量处理完成，共{len(responses)}个请求")


def main():
    """运行所有示例"""
    print("=" * 50)
    print("AI SDK 高级用法示例")
    print("=" * 50)

    try:
        # 注意: 某些示例需要有效的API Token和Base URL
        # example_context_manager()
        # example_task_management()
        example_error_handling()
        example_custom_configuration()
        # example_batch_requests()

        print("\n提示: 某些示例已被注释，取消注释并配置正确的API Token后运行")

    except Exception as e:
        print(f"\n未捕获的错误: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
