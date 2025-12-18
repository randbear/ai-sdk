"""
图片分析示例
演示如何使用AI SDK进行图片内容分析
"""
import os
import sys
import base64

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_sdk import AIClient
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def encode_image_to_base64(image_path: str) -> str:
    """
    将图片文件编码为Base64字符串

    Args:
        image_path: 图片文件路径

    Returns:
        Base64编码的字符串
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def main():
    """图片分析示例"""

    # 初始化客户端
    client = AIClient()

    try:
        print("=" * 50)
        print("AI SDK 图片分析示例")
        print("=" * 50)

        # 示例1: 使用图片URL分析
        print("\n[示例1] 使用图片URL分析")
        print("-" * 50)

        image_url = "http://156.254.5.245:8089/img/generate_image/1395623752720640.png"

        response = client.chat.completions.create(
            model="yuanbao",
            messages=[{"role": "user", "content": "请详细描述这张图片的内容"}],
            image_url=image_url,
        )

        print(f"图片URL: {image_url}")
        print(f"问题: 请详细描述这张图片的内容")
        print(f"分析结果: {response.choices[0].message.content}")

        # 示例2: 使用Base64编码的图片数据
        print("\n[示例2] 使用Base64编码的图片数据")
        print("-" * 50)

        # 注意: 请替换为实际的图片路径
        # image_path = "path/to/your/image.png"
        # if os.path.exists(image_path):
        #     image_data = encode_image_to_base64(image_path)
        #
        #     response = client.chat.completions.create(
        #         model="yuanbao",
        #         messages=[
        #             {"role": "user", "content": "这张图片里有什么？"}
        #         ],
        #         image_data=image_data
        #     )
        #
        #     print(f"图片路径: {image_path}")
        #     print(f"分析结果: {response.choices[0].message.content}")
        # else:
        #     print("图片文件不存在，跳过此示例")

        print("提示: 请取消注释上面的代码并提供实际的图片路径来测试")

        # 示例3: 图片分析 + 生成图片
        print("\n[示例3] 图片分析 + 生成图片")
        print("-" * 50)

        response = client.chat.completions.create(
            model="yuanbao",
            messages=[
                {
                    "role": "user",
                    "content": "分析这张图片并生成一张类似风格的图片",
                }
            ],
            image_url=image_url,
            generate_image=True,  # 启用图片生成
        )

        print(f"分析和生成结果: {response.choices[0].message.content}")

        # 示例4: 使用Gemini模型分析图片
        print("\n[示例4] 使用Gemini模型分析图片")
        print("-" * 50)

        response = client.chat.completions.create(
            model="gemini",
            messages=[
                {
                    "role": "user",
                    "content": "请识别图片中的物体并分类",
                }
            ],
            image_url=image_url,
        )

        print(f"Gemini分析结果: {response.choices[0].message.content}")

    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback

        traceback.print_exc()

    finally:
        # 关闭客户端
        client.close()


if __name__ == "__main__":
    main()
