# 图片生成功能指南

## 概述

AI SDK 支持强大的 **AI图片生成功能**，可以根据文本描述生成各种风格的图片。

## 快速开始

### 最简单的例子

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "生成一张未来城市的图片"}
        ],
        generate_image=True  # 启用图片生成
    )

    print(response.choices[0].message.content)
    # 响应中会包含生成的图片URL或描述
```

## 功能特性

### 1. 纯文本生成图片

根据文本描述直接生成图片：

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {
                "role": "user",
                "content": "生成一张日落时分的海边，有沙滩、海浪和晚霞"
            }
        ],
        generate_image=True
    )

    print(response.choices[0].message.content)
```

### 2. 基于参考图片生成

提供参考图片，生成相似风格的新图片：

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {
                "role": "user",
                "content": "参考这张图片的风格，生成一张不同主题的图片"
            }
        ],
        image_url="http://example.com/reference.png",
        generate_image=True
    )

    print(response.choices[0].message.content)
```

### 3. 详细描述生成

提供详细的风格和元素描述：

```python
from ai_sdk import AIClient

prompt = """
生成一张图片，要求：
- 主题：科幻太空站
- 风格：赛博朋克
- 元素：霓虹灯、飞船、宇航员
- 色调：蓝紫色调
- 氛围：神秘、未来感
"""

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": prompt}],
        generate_image=True
    )

    print(response.choices[0].message.content)
```

### 4. 结合深度研究

先研究特定风格，再生成图片：

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {
                "role": "user",
                "content": "研究印象派绘画风格，然后生成一张该风格的现代城市图片"
            }
        ],
        deep_research=True,   # 启用深度研究
        generate_image=True   # 启用图片生成
    )

    print(response.choices[0].message.content)
```

### 5. 使用不同模型

元宝和Gemini模型都支持图片生成：

```python
from ai_sdk import AIClient

with AIClient() as client:
    # 使用元宝模型
    response1 = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "生成一只可爱的猫"}],
        generate_image=True
    )

    # 使用Gemini模型
    response2 = client.chat.completions.create(
        model="gemini",
        messages=[{"role": "user", "content": "生成一只可爱的猫"}],
        generate_image=True
    )

    print("元宝:", response1.choices[0].message.content)
    print("Gemini:", response2.choices[0].message.content)
```

## 批量生成

生成多张不同主题的图片：

```python
from ai_sdk import AIClient

themes = [
    "春天的樱花",
    "夏天的海滩",
    "秋天的枫叶",
    "冬天的雪山"
]

with AIClient() as client:
    for theme in themes:
        response = client.chat.completions.create(
            model="yuanbao",
            messages=[{"role": "user", "content": f"生成一张{theme}的图片"}],
            generate_image=True
        )
        print(f"{theme}: {response.choices[0].message.content}")
```

## 完整参数说明

```python
client.chat.completions.create(
    model="yuanbao",           # 或 "gemini"
    messages=[...],            # 文本描述
    image_url="...",           # 可选：参考图片URL
    image_data="...",          # 可选：参考图片Base64
    generate_image=True,       # 必需：启用图片生成
    deep_research=False        # 可选：启用深度研究
)
```

## 参数组合

### 组合1: 纯文本生成
```python
messages=[{"role": "user", "content": "描述"}]
generate_image=True
```

### 组合2: 参考图片 + 文本
```python
messages=[{"role": "user", "content": "基于这张图片..."}]
image_url="http://..."
generate_image=True
```

### 组合3: 深度研究 + 生成
```python
messages=[{"role": "user", "content": "研究...然后生成..."}]
deep_research=True
generate_image=True
```

### 组合4: 全功能
```python
messages=[{"role": "user", "content": "分析这张图..."}]
image_url="http://..."
deep_research=True
generate_image=True
```

## 最佳实践

### 1. 清晰的描述

✅ **好的描述**：
```python
"生成一张赛博朋克风格的城市夜景，包含霓虹灯、飞行汽车和高楼大厦，色调为蓝紫色"
```

❌ **模糊的描述**：
```python
"生成一张图片"
```

### 2. 指定风格

明确指定艺术风格：
- 写实摄影
- 卡通动漫
- 油画风格
- 水彩画
- 赛博朋克
- 蒸汽朋克
- 极简主义
- 超现实主义

### 3. 描述元素

具体说明需要包含的元素：
- 主体对象
- 背景环境
- 光线效果
- 色调氛围
- 构图方式

### 4. 合理使用参数

```python
# 简单场景 - 只用generate_image
generate_image=True

# 需要研究特定风格 - 加上deep_research
deep_research=True
generate_image=True

# 需要参考现有图片 - 提供image_url
image_url="..."
generate_image=True
```

## 注意事项

1. **等待时间**
   - 图片生成需要较长时间（通常30-120秒）
   - 可以适当增加timeout设置
   ```python
   client = AIClient(timeout=120)
   ```

2. **响应内容**
   - 生成的图片URL会在响应的message.content中返回
   - 也可能包含图片描述和相关说明

3. **错误处理**
   ```python
   from ai_sdk import AIClient, TimeoutError

   try:
       with AIClient(timeout=120) as client:
           response = client.chat.completions.create(
               model="yuanbao",
               messages=[{"role": "user", "content": "生成图片"}],
               generate_image=True
           )
   except TimeoutError:
       print("生成超时，请重试")
   ```

4. **资源管理**
   - 使用with语句自动管理资源
   - 批量生成时注意API调用频率

## 运行示例

项目提供了完整的图片生成示例：

```bash
python examples/image_generation.py
```

该示例包含：
- ✅ 直接生成图片
- ✅ 根据详细描述生成
- ✅ 基于现有图片生成
- ✅ 使用不同模型生成
- ✅ 深度研究 + 生成
- ✅ 批量生成

## 常见问题

### Q: 支持哪些图片格式？
A: 生成的图片格式由API决定，通常为PNG或JPEG。

### Q: 生成的图片尺寸是多少？
A: 图片尺寸由API决定，可以在prompt中描述所需尺寸。

### Q: 可以生成多张图片吗？
A: 可以通过多次调用API生成多张图片，参考批量生成示例。

### Q: 生成失败怎么办？
A:
1. 检查prompt描述是否清晰
2. 确认timeout设置足够长
3. 查看错误日志了解具体原因

### Q: 如何获取生成的图片？
A: 图片URL会在响应的message.content中返回，可以直接下载。

## 进阶技巧

### 1. 风格迁移

```python
response = client.chat.completions.create(
    model="yuanbao",
    messages=[
        {"role": "user", "content": "将这张照片转换为梵高的星空风格"}
    ],
    image_url="http://example.com/photo.jpg",
    generate_image=True
)
```

### 2. 概念设计

```python
response = client.chat.completions.create(
    model="yuanbao",
    messages=[
        {"role": "user", "content": "设计一个未来智能手机的概念图"}
    ],
    generate_image=True
)
```

### 3. 场景重建

```python
response = client.chat.completions.create(
    model="yuanbao",
    messages=[
        {"role": "user", "content": "重建唐朝长安城的街景"}
    ],
    deep_research=True,
    generate_image=True
)
```

---

**开始创作吧！** 🎨

查看 `examples/image_generation.py` 获取完整示例代码。
