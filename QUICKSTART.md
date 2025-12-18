# 快速开始指南

这个指南将帮助你在5分钟内开始使用AI SDK。

## 步骤1: 安装依赖

```bash
pip install -r requirements.txt
```

## 步骤2: 配置环境变量

复制环境变量模板并填入你的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
AI_API_TOKEN=spsw.7464b7d51e71c92311bf76c528192413
AI_API_BASE_URL=http://your_server_ip/api/v1
AI_API_TIMEOUT=30
```

> **注意**: 请将 `your_server_ip` 替换为实际的服务器地址。Token可以从 `ai_api_info.txt` 中获取。

## 步骤3: 运行你的第一个请求

创建一个新文件 `test.py`：

```python
from ai_sdk import AIClient

# 初始化客户端
with AIClient() as client:
    # 发起对话
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "什么是Python？"}
        ]
    )

    # 打印回答
    print(response.choices[0].message.content)
```

运行：

```bash
python test.py
```

## 步骤4: 尝试更多功能

### 多轮对话

```python
from ai_sdk import AIClient, ChatMessage

with AIClient() as client:
    messages = [
        ChatMessage(role="system", content="你是一个编程助手"),
        ChatMessage(role="user", content="如何学习Python？")
    ]

    response = client.chat.completions.create(
        model="yuanbao",
        messages=messages
    )

    print(response.choices[0].message.content)
```

### 图片分析

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "请描述这张图片"}
        ],
        image_url="http://example.com/image.png"
    )

    print(response.choices[0].message.content)
```

### 深度研究模式

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "人工智能的发展历史"}
        ],
        deep_research=True  # 启用深度研究
    )

    print(response.choices[0].message.content)
```

## 步骤5: 运行示例代码

项目提供了完整的示例代码：

```bash
# 基础对话示例
python examples/basic_chat.py

# 图片分析示例
python examples/image_analysis.py

# 高级用法示例
python examples/advanced_usage.py
```

## 常见问题

### 1. 认证失败怎么办？

检查 `.env` 文件中的 `AI_API_TOKEN` 是否正确。

### 2. 连接超时怎么办？

可以增加超时时间：

```python
client = AIClient(timeout=60)  # 60秒超时
```

### 3. 如何启用调试日志？

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 4. 支持哪些模型？

- `yuanbao` (元宝模型)
- `gemini` (Gemini模型)

## 下一步

- 阅读完整的 [README.md](README.md)
- 查看 [API参考文档](README.md#api参考)
- 查看更多 [示例代码](examples/)
- 了解 [错误处理](README.md#错误处理)

## 需要帮助？

- 查看 [常见问题](README.md#常见问题)
- 查看 [API文档](https://docs.apipost.net/docs/detail/52c44bf47843000)
- 提交 [Issue](https://github.com/your-repo/issues)

祝你使用愉快！ 🎉
