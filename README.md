# AI SDK - 兼容OpenAI的Python SDK

一个兼容OpenAI SDK接口风格的AI API客户端，支持元宝和Gemini模型，提供简洁易用的Python接口。

## 特性

- ✅ **兼容OpenAI SDK** - 熟悉的API接口，快速上手
- ✅ **类型提示完善** - 完整的类型注解，IDE友好
- ✅ **错误处理健全** - 详细的异常类型和错误信息
- ✅ **环境变量管理** - 安全地管理API Token等敏感信息
- ✅ **多模型支持** - 支持元宝(Yuanbao)和Gemini模型
- ✅ **图片分析** - 支持图片URL和Base64数据
- ✅ **图片生成** - AI生成各种风格的图片
- ✅ **深度研究** - 支持启用深度研究模式
- ✅ **任务管理** - 支持查询任务状态和结果

## 快速开始

### 安装方式

#### 方式 1: 从 GitHub 私有仓库安装（推荐）

```bash
# 设置 GitHub Token
export GITHUB_TOKEN=your_github_token

# 安装最新版
pip install git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git

# 或安装特定版本
pip install git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git@v0.1.0
```

> 📖 详细的发布和安装指南见 [PUBLISH_GUIDE.md](PUBLISH_GUIDE.md) 或 [GITHUB_SETUP.md](GITHUB_SETUP.md)

#### 方式 2: 本地开发安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/ai-sdk.git
cd ai-sdk

# 安装依赖
pip install -r requirements.txt

# 或以可编辑模式安装
pip install -e .
```

### 配置环境变量

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的配置：
```env
AI_API_TOKEN=spsw.your_token_here
AI_API_BASE_URL=http://your_server_ip/api/v1
AI_API_TIMEOUT=30
```

### 基础使用

```python
from ai_sdk import AIClient

# 初始化客户端（自动从环境变量读取配置）
client = AIClient()

# 发起对话请求
response = client.chat.completions.create(
    model="yuanbao",
    messages=[
        {"role": "user", "content": "什么是SEO？"}
    ]
)

# 获取回答
print(response.choices[0].message.content)

# 关闭客户端
client.close()
```

### 使用上下文管理器（推荐）

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "介绍一下Python"}
        ]
    )
    print(response.choices[0].message.content)
# 自动关闭客户端
```

## 使用示例

### 1. 简单对话

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "你好"}
        ]
    )
    print(response.choices[0].message.content)
```

### 2. 多轮对话

```python
from ai_sdk import AIClient, ChatMessage

with AIClient() as client:
    messages = [
        ChatMessage(role="system", content="你是一个Python编程助手"),
        ChatMessage(role="user", content="什么是装饰器？")
    ]

    response = client.chat.completions.create(
        model="yuanbao",
        messages=messages
    )
    print(response.choices[0].message.content)
```

### 3. 图片分析

```python
from ai_sdk import AIClient

with AIClient() as client:
    # 使用图片URL
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "请描述这张图片"}
        ],
        image_url="http://example.com/image.png"
    )
    print(response.choices[0].message.content)

    # 或使用Base64编码的图片数据
    import base64

    with open("image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "分析这张图片"}
        ],
        image_data=image_data
    )
```

### 4. 启用深度研究

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "人工智能的未来发展"}
        ],
        deep_research=True  # 启用深度研究
    )
    print(response.choices[0].message.content)
```

### 5. 切换模型

```python
from ai_sdk import AIClient

with AIClient() as client:
    # 使用元宝模型
    response1 = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "介绍武汉"}]
    )

    # 使用Gemini模型
    response2 = client.chat.completions.create(
        model="gemini",
        messages=[{"role": "user", "content": "介绍武汉"}]
    )
```

### 6. 错误处理

```python
from ai_sdk import (
    AIClient,
    AuthenticationError,
    InvalidRequestError,
    TimeoutError,
    AIAPIError
)

try:
    with AIClient() as client:
        response = client.chat.completions.create(
            model="yuanbao",
            messages=[{"role": "user", "content": "你好"}]
        )
except AuthenticationError as e:
    print(f"认证失败: {e}")
except InvalidRequestError as e:
    print(f"请求参数错误: {e}")
except TimeoutError as e:
    print(f"请求超时: {e}")
except AIAPIError as e:
    print(f"API错误: {e}")
```

### 7. 任务管理

```python
from ai_sdk import AIClient

with AIClient() as client:
    # 创建任务
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "介绍Python"}]
    )

    task_id = response.id
    print(f"任务ID: {task_id}")

    # 稍后查询任务结果
    task_result = client.tasks.retrieve(task_id)
    print(f"任务状态: {task_result['status']}")
    print(f"任务结果: {task_result['answer']}")
```

## 更多示例

查看 `examples/` 目录获取更多示例代码：

- `basic_chat.py` - 基础对话示例
- `image_analysis.py` - 图片分析示例
- `advanced_usage.py` - 高级用法示例

运行示例：

```bash
# 运行基础对话示例
python examples/basic_chat.py

# 运行图片分析示例
python examples/image_analysis.py

# 运行高级用法示例
python examples/advanced_usage.py
```

## API参考

### AIClient

主客户端类，用于与API交互。

**初始化参数：**

- `api_token` (str, optional): API Token，默认从环境变量 `AI_API_TOKEN` 读取
- `base_url` (str, optional): API基础URL，默认从环境变量 `AI_API_BASE_URL` 读取
- `timeout` (int, optional): 请求超时时间（秒），默认30秒

**方法：**

- `chat.completions.create()`: 创建chat completion
- `tasks.retrieve(task_id)`: 查询任务结果
- `close()`: 关闭客户端，释放资源

### chat.completions.create()

创建chat completion请求。

**参数：**

- `model` (str): 模型名称，可选 "yuanbao" 或 "gemini"
- `messages` (List[ChatMessage]): 对话消息列表
- `image_url` (str, optional): 图片URL
- `image_data` (str, optional): 图片Base64数据
- `deep_research` (bool, optional): 是否启用深度研究，默认False
- `generate_image` (bool, optional): 是否生成图片，默认False

**返回：**

- `ChatCompletion`: 包含生成结果的响应对象

### ChatMessage

对话消息对象。

**字段：**

- `role` (str): 消息角色，可选 "user", "assistant", "system"
- `content` (str): 消息内容

### ChatCompletion

Chat completion响应对象。

**字段：**

- `id` (str): 任务ID
- `object` (str): 对象类型，值为 "chat.completion"
- `created` (int): 创建时间戳
- `model` (str): 使用的模型
- `choices` (List[Choice]): 生成结果列表
- `usage` (Usage): Token使用统计

## 异常类型

- `AIAPIError`: 基础异常类
- `AuthenticationError`: 认证错误
- `InvalidRequestError`: 请求参数错误
- `APIConnectionError`: 网络连接错误
- `RateLimitError`: 请求频率限制错误
- `TimeoutError`: 请求超时错误

## 配置说明

### 环境变量

在项目根目录创建 `.env` 文件：

```env
# 必填：API Token
AI_API_TOKEN=spsw.your_token_here

# 必填：API基础URL
AI_API_BASE_URL=http://your_server_ip/api/v1

# 可选：请求超时时间（秒）
AI_API_TIMEOUT=30
```

### 代码配置

也可以在代码中直接传入配置：

```python
from ai_sdk import AIClient

client = AIClient(
    api_token="spsw.your_token",
    base_url="http://your_server/api/v1",
    timeout=60
)
```

## 项目结构

```
my_ai_api/
├── ai_sdk/                 # SDK核心代码
│   ├── __init__.py        # 包初始化，导出主要类
│   ├── client.py          # 核心客户端类
│   ├── exceptions.py      # 异常定义
│   ├── _utils.py          # 工具函数
│   ├── resources/         # 资源模块
│   │   ├── __init__.py
│   │   ├── chat.py        # Chat相关API
│   │   └── tasks.py       # 任务管理API
│   └── types/             # 类型定义
│       ├── __init__.py
│       └── chat.py        # Chat相关类型
├── examples/              # 使用示例
│   ├── basic_chat.py
│   ├── image_analysis.py
│   └── advanced_usage.py
├── tests/                 # 测试文件
├── .env.example           # 环境变量模板
├── .gitignore
├── README.md
└── requirements.txt
```

## 开发指南

### 安装开发依赖

```bash
pip install -r requirements.txt
```

### 运行测试

```bash
pytest tests/
```

### 代码风格

本项目遵循PEP 8代码风格规范，使用类型提示，注重代码可读性。

## 常见问题

### Q: 如何获取API Token？

A: 请参考API文档获取Token：https://docs.apipost.net/docs/detail/52c44bf47843000

### Q: 支持哪些模型？

A: 目前支持两种模型：
- `yuanbao` (元宝) - type=1
- `gemini` - type=2

### Q: 如何处理超时？

A: 可以在初始化客户端时设置timeout参数：

```python
client = AIClient(timeout=60)  # 60秒超时
```

### Q: 图片URL和图片数据可以同时使用吗？

A: 不建议同时使用。API会优先使用 `imageUrl`，如果为空才使用 `imageData`。

### Q: 如何启用日志？

A: 使用Python的logging模块：

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v0.1.0 (2025-12-18)

- 初始版本发布
- 实现基础chat.completions接口
- 支持元宝和Gemini模型
- 支持图片分析
- 支持深度研究模式
- 完善的错误处理和类型提示

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue: [GitHub Issues](https://github.com/your-repo/issues)
- 查看文档: [API文档](https://docs.apipost.net/docs/detail/52c44bf47843000)
