# AI SDK 快速参考

## 基础对话

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",  # 或 "gemini"
        messages=[{"role": "user", "content": "你好"}]
    )
    print(response.choices[0].message.content)
```

## 图片生成 🎨

```python
with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "生成一张未来城市的图片"}],
        generate_image=True  # ← 关键参数
    )
    print(response.choices[0].message.content)
```

## 图片分析 🔍

```python
with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "描述这张图片"}],
        image_url="http://example.com/image.png"
    )
    print(response.choices[0].message.content)
```

## 深度研究 🔬

```python
with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "人工智能的发展历史"}],
        deep_research=True  # ← 关键参数
    )
    print(response.choices[0].message.content)
```

## 组合功能 🚀

### 参考图片 + 生成新图

```python
response = client.chat.completions.create(
    model="yuanbao",
    messages=[{"role": "user", "content": "参考这张图的风格生成新图"}],
    image_url="http://example.com/ref.png",
    generate_image=True
)
```

### 深度研究 + 图片生成

```python
response = client.chat.completions.create(
    model="yuanbao",
    messages=[{"role": "user", "content": "研究印象派风格，生成一张现代城市"}],
    deep_research=True,
    generate_image=True
)
```

## 参数速查表

| 参数 | 类型 | 说明 | 默认值 |
|-----|------|------|--------|
| `model` | str | 模型：`yuanbao` 或 `gemini` | `yuanbao` |
| `messages` | List | 对话消息列表 | **必填** |
| `image_url` | str | 图片URL | `None` |
| `image_data` | str | 图片Base64 | `None` |
| `generate_image` | bool | 生成图片 | `False` |
| `deep_research` | bool | 深度研究 | `False` |

## 错误处理

```python
from ai_sdk import AIClient, AIAPIError, TimeoutError

try:
    with AIClient() as client:
        response = client.chat.completions.create(...)
except TimeoutError:
    print("请求超时")
except AIAPIError as e:
    print(f"API错误: {e}")
```

## 配置

### 环境变量 (.env)

```env
AI_API_TOKEN=spsw.your_token
AI_API_BASE_URL=http://your_server/api/v1
AI_API_TIMEOUT=30
```

### 代码配置

```python
client = AIClient(
    api_token="spsw.your_token",
    base_url="http://your_server/api/v1",
    timeout=60
)
```

## 示例代码

```bash
# 基础对话
python examples/basic_chat.py

# 图片分析
python examples/image_analysis.py

# 图片生成 ⭐NEW
python examples/image_generation.py

# 高级用法
python examples/advanced_usage.py
```

## 文档

- 📖 [README.md](README.md) - 完整文档
- 🚀 [QUICKSTART.md](QUICKSTART.md) - 快速开始
- 📘 [USAGE.md](USAGE.md) - 使用手册
- 🎨 [IMAGE_GENERATION_GUIDE.md](IMAGE_GENERATION_GUIDE.md) - 图片生成指南
- 📋 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目总结

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 验证安装
python verify_installation.py

# 配置环境
cp .env.example .env
# 然后编辑 .env 文件

# 运行测试
pytest tests/ -v
```

---

**提示**: 图片生成功能已完全集成，只需设置 `generate_image=True` 即可！
