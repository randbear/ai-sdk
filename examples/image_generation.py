"""
图片生成示例
演示如何使用AI SDK生成图片
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_sdk import AIClient
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    """图片生成示例"""

    client = AIClient()

    try:
        print("=" * 50)
        print("AI SDK 图片生成示例")
        print("=" * 50)

        # 示例1: 直接生成图片
        print("\n[示例1] 直接生成图片")
        print("-" * 50)

        response = client.chat.completions.create(
            model="yuanbao",
            messages=[
                {
                    "role": "user",
                    "content": "生成一张未来科技城市的图片，包含飞行汽车和高楼大厦",
                }
            ],
            generate_image=True,  # 启用图片生成
        )

        print(f"请求: 生成一张未来科技城市的图片")
        print(f"响应: {response.choices[0].message.content}")
        print(f"任务ID: {response.id}")

        # 示例2: 根据描述生成图片
        print("\n[示例2] 根据详细描述生成图片")
        print("-" * 50)

        prompt = """
        生成一张图片：
        - 主题：日落时分的海边
        - 风格：写实摄影风格
        - 元素：沙滩、海浪、晚霞、海鸥
        - 色调：温暖的橙红色调
        """

        response = client.chat.completions.create(
            model="yuanbao",
            messages=[{"role": "user", "content": prompt}],
            generate_image=True,
        )

        print(f"请求: {prompt.strip()}")
        print(f"响应: {response.choices[0].message.content}")

        # 示例3: 基于现有图片生成新图片
        print("\n[示例3] 基于现有图片生成类似风格的图片")
        print("-" * 50)

        image_url = "http://156.254.5.245:8089/img/generate_image/1395623752720640.png"

        response = client.chat.completions.create(
            model="yuanbao",
            messages=[
                {
                    "role": "user",
                    "content": "分析这张图片的风格，然后生成一张相似风格但主题不同的图片",
                }
            ],
            image_url=image_url,  # 提供参考图片
            generate_image=True,  # 启用图片生成
        )

        print(f"参考图片URL: {image_url}")
        print(f"响应: {response.choices[0].message.content}")

        # 示例4: 使用Gemini模型生成图片
        print("\n[示例4] 使用Gemini模型生成图片")
        print("-" * 50)

        response = client.chat.completions.create(
            model="gemini",  # 使用Gemini模型
            messages=[
                {
                    "role": "user",
                    "content": "生成一张可爱的卡通猫咪图片，要有大眼睛和蝴蝶结",
                }
            ],
            generate_image=True,
        )

        print(f"请求: 生成一张可爱的卡通猫咪图片")
        print(f"响应: {response.choices[0].message.content}")

        # 示例5: 生成图片 + 深度研究
        print("\n[示例5] 图片生成 + 深度研究模式")
        print("-" * 50)

        response = client.chat.completions.create(
            model="yuanbao",
            messages=[
                {
                    "role": "user",
                    "content": "研究文艺复兴时期的艺术风格，然后生成一张该风格的现代城市图片",
                }
            ],
            deep_research=True,  # 启用深度研究
            generate_image=True,  # 启用图片生成
        )

        print(f"请求: 研究文艺复兴风格并生成图片")
        print(f"响应: {response.choices[0].message.content}")

        # 示例6: 批量生成图片
        print("\n[示例6] 批量生成不同主题的图片")
        print("-" * 50)

        themes = [
            "春天的樱花树",
            "夏天的海滩",
            "秋天的枫叶林",
            "冬天的雪山",
        ]

        for i, theme in enumerate(themes, 1):
            print(f"\n生成图片 {i}/{len(themes)}: {theme}")
            try:
                response = client.chat.completions.create(
                    model="yuanbao",
                    messages=[{"role": "user", "content": f"生成一张{theme}的图片"}],
                    generate_image=True,
                )
                print(f"  ✓ 成功: {response.choices[0].message.content[:100]}...")
            except Exception as e:
                print(f"  ✗ 失败: {str(e)}")

        print("\n" + "=" * 50)
        print("提示：")
        print("1. 图片生成可能需要较长时间，请耐心等待")
        print("2. 可以结合image_url参数提供参考图片")
        print("3. 可以启用deep_research进行更深入的创作")
        print("4. 生成的图片URL会在响应内容中返回")
        print("=" * 50)

    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback

        traceback.print_exc()

    finally:
        # 关闭客户端
        client.close()


if __name__ == "__main__":
    main()
