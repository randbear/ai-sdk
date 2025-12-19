#!/usr/bin/env python3
"""
SDK 快速测试脚本
测试 SDK 是否正常工作
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_import():
    """测试导入"""
    print("=" * 60)
    print("测试 1: 检查模块导入")
    print("=" * 60)
    try:
        from ai_sdk import AIClient, ChatMessage
        print("✅ 模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_client_init():
    """测试客户端初始化"""
    print("\n" + "=" * 60)
    print("测试 2: 检查客户端初始化")
    print("=" * 60)

    from ai_sdk import AIClient

    token = os.getenv("AI_API_TOKEN")
    if not token:
        print("⚠️  未找到 AI_API_TOKEN 环境变量")
        print("   请在 .env 文件中配置")
        return False

    try:
        client = AIClient()
        print(f"✅ 客户端初始化成功")
        print(f"   Base URL: {client.base_url}")
        print(f"   Timeout: {client.timeout}秒")
        client.close()
        return True
    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")
        return False

def test_simple_chat():
    """测试简单对话"""
    print("\n" + "=" * 60)
    print("测试 3: 测试简单对话功能")
    print("=" * 60)

    from ai_sdk import AIClient

    token = os.getenv("AI_API_TOKEN")
    if not token:
        print("⚠️  跳过测试（未配置 Token）")
        return False

    try:
        with AIClient() as client:
            print("发送测试消息: '你好'")
            response = client.chat.completions.create(
                model="yuanbao",
                messages=[
                    {"role": "user", "content": "你好"}
                ]
            )

            answer = response.choices[0].message.content
            print(f"\n✅ 收到回复:")
            print(f"   {answer[:100]}..." if len(answer) > 100 else f"   {answer}")
            print(f"\n   任务ID: {response.id}")
            print(f"   模型: {response.model}")
            return True

    except Exception as e:
        print(f"❌ 对话测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_default_base_url():
    """测试默认 base_url"""
    print("\n" + "=" * 60)
    print("测试 4: 验证默认 base_url 配置")
    print("=" * 60)

    from ai_sdk import AIClient

    # 临时移除环境变量中的 base_url
    original_base_url = os.environ.pop("AI_API_BASE_URL", None)

    try:
        # 不提供 token 会失败，但我们可以看到 base_url
        try:
            client = AIClient(api_token="test_token")
            print(f"✅ 默认 base_url 已生效: {client.base_url}")
            expected = "http://156.254.5.245:8089/api/v1"
            if client.base_url == expected:
                print(f"   ✅ 地址正确: {expected}")
            else:
                print(f"   ⚠️  地址不匹配，期望: {expected}")
            client.close()
            return True
        except Exception as e:
            print(f"   初始化客户端时出错: {e}")
            return False
    finally:
        # 恢复环境变量
        if original_base_url:
            os.environ["AI_API_BASE_URL"] = original_base_url

def main():
    """运行所有测试"""
    print("\n🚀 开始测试 AI SDK\n")

    results = []

    # 测试 1: 导入
    results.append(("模块导入", test_import()))

    # 测试 2: 客户端初始化
    results.append(("客户端初始化", test_client_init()))

    # 测试 3: 默认 base_url
    results.append(("默认 base_url", test_default_base_url()))

    # 测试 4: 简单对话（需要有效的 Token）
    if os.getenv("AI_API_TOKEN"):
        results.append(("简单对话", test_simple_chat()))
    else:
        print("\n" + "=" * 60)
        print("⚠️  跳过对话测试（未配置 AI_API_TOKEN）")
        print("=" * 60)

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\n总计: {passed}/{total} 项测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！SDK 工作正常！")
    else:
        print("\n⚠️  部分测试失败，请检查配置")

    print("=" * 60)

if __name__ == "__main__":
    main()
