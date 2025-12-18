"""
SDK安装验证脚本
运行此脚本检查SDK是否正确安装
"""
import sys


def verify_imports():
    """验证所有模块是否可以正常导入"""
    print("=" * 60)
    print("AI SDK 安装验证")
    print("=" * 60)

    checks = []

    # 检查1: 导入主模块
    print("\n[1/7] 检查主模块导入...")
    try:
        import ai_sdk

        print(f"✅ ai_sdk 导入成功，版本: {ai_sdk.__version__}")
        checks.append(True)
    except ImportError as e:
        print(f"❌ ai_sdk 导入失败: {e}")
        checks.append(False)

    # 检查2: 导入客户端
    print("\n[2/7] 检查客户端类...")
    try:
        from ai_sdk import AIClient

        print("✅ AIClient 导入成功")
        checks.append(True)
    except ImportError as e:
        print(f"❌ AIClient 导入失败: {e}")
        checks.append(False)

    # 检查3: 导入异常类
    print("\n[3/7] 检查异常类...")
    try:
        from ai_sdk import (
            AIAPIError,
            AuthenticationError,
            InvalidRequestError,
            APIConnectionError,
            RateLimitError,
            TimeoutError,
        )

        print("✅ 所有异常类导入成功")
        checks.append(True)
    except ImportError as e:
        print(f"❌ 异常类导入失败: {e}")
        checks.append(False)

    # 检查4: 导入类型定义
    print("\n[4/7] 检查类型定义...")
    try:
        from ai_sdk import ChatMessage, ChatCompletion, Choice, Usage

        print("✅ 所有类型定义导入成功")
        checks.append(True)
    except ImportError as e:
        print(f"❌ 类型定义导入失败: {e}")
        checks.append(False)

    # 检查5: 检查依赖
    print("\n[5/7] 检查依赖包...")
    required_packages = ["requests", "dotenv", "pydantic"]
    missing_packages = []

    for package in required_packages:
        try:
            if package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} 未安装")
            missing_packages.append(package)

    if not missing_packages:
        print("✅ 所有依赖包已安装")
        checks.append(True)
    else:
        print(f"❌ 缺少依赖: {', '.join(missing_packages)}")
        print("   请运行: pip install -r requirements.txt")
        checks.append(False)

    # 检查6: 测试ChatMessage创建
    print("\n[6/7] 测试对象创建...")
    try:
        from ai_sdk import ChatMessage

        msg = ChatMessage(role="user", content="测试")
        assert msg.role == "user"
        assert msg.content == "测试"
        print("✅ ChatMessage 对象创建成功")
        checks.append(True)
    except Exception as e:
        print(f"❌ ChatMessage 对象创建失败: {e}")
        checks.append(False)

    # 检查7: 环境变量配置
    print("\n[7/7] 检查环境变量配置...")
    import os

    has_env_file = os.path.exists(".env")
    has_example = os.path.exists(".env.example")

    if has_env_file:
        print("✅ .env 文件存在")
        # 检查是否配置了必要的环境变量
        from dotenv import load_dotenv

        load_dotenv()
        token = os.getenv("AI_API_TOKEN")

        if token:
            print("✅ API Token 已配置")
            print("   (SDK 已内置默认服务地址，无需配置 base_url)")
            checks.append(True)
        else:
            print("⚠️  .env 文件存在但配置不完整")
            print("   请确保配置了 AI_API_TOKEN")
            checks.append(False)
    elif has_example:
        print("⚠️  .env 文件不存在")
        print("   请运行: cp .env.example .env")
        print("   然后编辑 .env 文件填入实际配置")
        checks.append(False)
    else:
        print("❌ .env.example 文件不存在")
        checks.append(False)

    # 总结
    print("\n" + "=" * 60)
    passed = sum(checks)
    total = len(checks)
    print(f"验证结果: {passed}/{total} 项通过")

    if passed == total:
        print("✅ SDK安装完整，可以开始使用！")
        print("\n下一步:")
        print("  1. 确保 .env 文件配置正确")
        print("  2. 运行示例: python examples/basic_chat.py")
        print("  3. 查看文档: README.md")
    else:
        print("⚠️  部分检查未通过，请按提示修复问题")
        if not all(checks[:4]):
            print("\n如果模块导入失败，请确保:")
            print("  1. 当前目录是项目根目录")
            print("  2. 已安装所有依赖: pip install -r requirements.txt")
        sys.exit(1)

    print("=" * 60)


if __name__ == "__main__":
    verify_imports()
