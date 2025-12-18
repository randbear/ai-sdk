# API 参考文档

完整的 API 接口文档。

## AIClient

核心客户端类，用于与 API 交互。

### 初始化

```python
AIClient(
    api_token: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: int = 30
)
```

**参数**:

- `api_token` (str, optional): API Token，默认从环境变量 `AI_API_TOKEN` 读取
- `base_url` (str, optional): API 基础 URL（可选），SDK 已内置默认服务地址
- `timeout` (int, optional): 请求超时时间（秒），默认 30 秒

**示例**:

```python
# 使用环境变量
client = AIClient()

# 或直接传入参数
client = AIClient(api_token="spsw.your_token")

# 自定义超时时间
client = AIClient(api_token="spsw.your_token", timeout=60)

# 使用自定义服务地址（可选）
client = AIClient(
    api_token="spsw.your_token",
    base_url="http://your_custom_server/api/v1"
)
```

---

## chat.completions.create()

创建 chat completion 请求。

### 方法签名

```python
client.chat.completions.create(
    model: str = "yuanbao",
    messages: List[ChatMessage],
    image_url: Optional[str] = None,
    image_data: Optional[str] = None,
    deep_research: bool = False,
    generate_image: bool = False
) -> ChatCompletion
```

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|--------|------|
| `model` | str | `"yuanbao"` | 模型名称：`"yuanbao"` 或 `"gemini"` |
| `messages` | List[ChatMessage] | **必填** | 对话消息列表 |
| `image_url` | str | `None` | 图片 URL（可选） |
| `image_data` | str | `None` | 图片 Base64 数据（可选） |
| `deep_research` | bool | `False` | 是否启用深度研究 |
| `generate_image` | bool | `False` | 是否生成图片 |

### 返回值

返回 `ChatCompletion` 对象，包含：

- `id` (str): 任务 ID
- `object` (str): 对象类型，值为 `"chat.completion"`
- `created` (int): 创建时间戳
- `model` (str): 使用的模型
- `choices` (List[Choice]): 生成结果列表
- `usage` (Usage): Token 使用统计

### 示例

#### 基础对话

```python
response = client.chat.completions.create(
    model="yuanbao",
    messages=[
        {"role": "user", "content": "你好"}
    ]
)
print(response.choices[0].message.content)
```

#### 多轮对话

```python
from ai_sdk import ChatMessage

messages = [
    ChatMessage(role="system", content="你是一个编程助手"),
    ChatMessage(role="user", "content": "什么是装饰器？")
]

response = client.chat.completions.create(
    model="yuanbao",
    messages=messages
)
```

#### 图片分析

```python
response = client.chat.completions.create(
    model="yuanbao",
    messages=[{"role": "user", "content": "描述这张图片"}],
    image_url="http://example.com/image.png"
)
```

#### 图片生成

```python
response = client.chat.completions.create(
    model="yuanbao",
    messages=[{"role": "user", "content": "生成一张未来城市的图片"}],
    generate_image=True
)
```

#### 深度研究

```python
response = client.chat.completions.create(
    model="yuanbao",
    messages=[{"role": "user", "content": "人工智能的发展历史"}],
    deep_research=True
)
```

---

## tasks.retrieve()

查询任务结果。

### 方法签名

```python
client.tasks.retrieve(task_id: str) -> Dict[str, Any]
```

### 参数

- `task_id` (str): 任务 ID

### 返回值

返回任务结果字典，包含：

- `status`: 任务状态
- `answer`: 任务结果
- 其他字段...

### 示例

```python
# 获取任务 ID
response = client.chat.completions.create(...)
task_id = response.id

# 查询任务结果
result = client.tasks.retrieve(task_id)
print(result['status'])
print(result['answer'])
```

---

## 数据类型

### ChatMessage

对话消息对象。

```python
class ChatMessage:
    role: Literal["user", "assistant", "system"]
    content: str
```

**示例**:

```python
from ai_sdk import ChatMessage

msg = ChatMessage(role="user", content="你好")
```

### ChatCompletion

Chat completion 响应对象。

```python
class ChatCompletion:
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Optional[Usage]
```

### Choice

单个选择结果。

```python
class Choice:
    index: int
    message: ChatMessage
    finish_reason: Optional[str]
```

### Usage

Token 使用统计。

```python
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
```

---

## 异常类型

### AIAPIError

基础异常类。

```python
class AIAPIError(Exception):
    message: str
    status_code: Optional[int]
    response: Optional[dict]
```

### AuthenticationError

认证错误 - Token 无效或缺失。

```python
class AuthenticationError(AIAPIError):
    pass
```

### InvalidRequestError

请求参数错误。

```python
class InvalidRequestError(AIAPIError):
    pass
```

### APIConnectionError

API 连接错误。

```python
class APIConnectionError(AIAPIError):
    pass
```

### RateLimitError

请求频率限制错误。

```python
class RateLimitError(AIAPIError):
    pass
```

### TimeoutError

请求超时错误。

```python
class TimeoutError(AIAPIError):
    pass
```

---

## 上下文管理器

AIClient 支持上下文管理器，自动管理资源。

```python
with AIClient() as client:
    response = client.chat.completions.create(...)
    # 退出时自动调用 client.close()
```

---

## 完整示例

```python
from ai_sdk import (
    AIClient,
    ChatMessage,
    AIAPIError,
    AuthenticationError,
    InvalidRequestError
)
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

try:
    # 使用上下文管理器
    with AIClient() as client:
        # 创建对话
        response = client.chat.completions.create(
            model="yuanbao",
            messages=[
                ChatMessage(role="system", content="你是一个编程助手"),
                ChatMessage(role="user", content="什么是 Python？")
            ],
            deep_research=True
        )

        # 获取结果
        answer = response.choices[0].message.content
        print(f"回答: {answer}")

        # 查询任务详情
        task_result = client.tasks.retrieve(response.id)
        print(f"任务状态: {task_result['status']}")

except AuthenticationError as e:
    print(f"认证失败: {e}")
except InvalidRequestError as e:
    print(f"参数错误: {e}")
except AIAPIError as e:
    print(f"API 错误: {e}")
```

---

## 环境变量

| 变量名 | 说明 | 必需 | 示例 |
|-------|------|------|------|
| `AI_API_TOKEN` | API Token | 是 | `spsw.xxxxx` |
| `AI_API_BASE_URL` | API 基础 URL | 否 | `http://server/api/v1` |
| `AI_API_TIMEOUT` | 请求超时时间（秒） | 否 | `30` |

> **提示**: SDK 已内置默认服务地址，`AI_API_BASE_URL` 为可选配置

配置方式：

```bash
# 方式 1: 环境变量
export AI_API_TOKEN=spsw.your_token

# 方式 2: .env 文件
# 创建 .env 文件并添加：
AI_API_TOKEN=spsw.your_token

# 可选：使用自定义服务地址
# AI_API_BASE_URL=http://your_custom_server/api/v1
```

---

## 更多信息

- [完整使用手册](usage.md)
- [图片生成指南](image-generation.md)
- [示例代码](examples/basic-chat.md)
- [GitHub 仓库](https://github.com/randbear/ai-sdk)
