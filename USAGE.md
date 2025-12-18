# 使用手册

## 目录

1. [开始使用](#开始使用)
2. [基础功能](#基础功能)
3. [高级功能](#高级功能)
4. [最佳实践](#最佳实践)
5. [故障排查](#故障排查)

## 开始使用

### 第一步：安装依赖

```bash
pip install -r requirements.txt
```

### 第二步：配置API

根据 `ai_api_info.txt` 中的信息配置环境变量：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
AI_API_TOKEN=spsw.7464b7d51e71c92311bf76c528192413
AI_API_BASE_URL=http://156.254.5.245:8089/api/v1
AI_API_TIMEOUT=30
```

### 第三步：验证安装

```bash
python verify_installation.py
```

看到 "SDK安装完整，可以开始使用！" 即表示安装成功。

## 基础功能

### 1. 简单对话

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "什么是SEO？"}
        ]
    )
    print(response.choices[0].message.content)
```

### 2. 多轮对话

```python
from ai_sdk import AIClient, ChatMessage

with AIClient() as client:
    # 构建对话历史
    messages = [
        ChatMessage(role="system", content="你是一个编程助手"),
        ChatMessage(role="user", content="Python有什么优点？"),
    ]

    response = client.chat.completions.create(
        model="yuanbao",
        messages=messages
    )

    # 继续对话
    messages.append(ChatMessage(
        role="assistant",
        content=response.choices[0].message.content
    ))
    messages.append(ChatMessage(
        role="user",
        content="那它有什么缺点吗？"
    ))

    response2 = client.chat.completions.create(
        model="yuanbao",
        messages=messages
    )
    print(response2.choices[0].message.content)
```

### 3. 切换模型

```python
from ai_sdk import AIClient

with AIClient() as client:
    # 使用元宝模型
    response1 = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "介绍Python"}]
    )

    # 使用Gemini模型
    response2 = client.chat.completions.create(
        model="gemini",
        messages=[{"role": "user", "content": "介绍Python"}]
    )

    # 比较两个模型的回答
    print("元宝:", response1.choices[0].message.content)
    print("\nGemini:", response2.choices[0].message.content)
```

## 高级功能

### 1. 图片分析（使用URL）

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "请详细描述这张图片的内容"}
        ],
        image_url="http://156.254.5.245:8089/img/generate_image/1395623752720640.png"
    )
    print(response.choices[0].message.content)
```

### 2. 图片分析（使用Base64）

```python
import base64
from ai_sdk import AIClient

# 读取本地图片并转为Base64
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

with AIClient() as client:
    image_data = encode_image("path/to/your/image.png")

    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "这张图片里有什么？"}
        ],
        image_data=image_data
    )
    print(response.choices[0].message.content)
```

### 3. 深度研究模式

```python
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[
            {"role": "user", "content": "人工智能的发展历史和未来趋势"}
        ],
        deep_research=True  # 启用深度研究
    )
    print(response.choices[0].message.content)
```

### 4. 生成图片

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
```

### 5. 任务管理

```python
from ai_sdk import AIClient

with AIClient() as client:
    # 创建任务
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "介绍机器学习"}]
    )

    # 获取任务ID
    task_id = response.id
    print(f"任务ID: {task_id}")

    # 稍后查询任务结果
    import time
    time.sleep(5)

    task_result = client.tasks.retrieve(task_id)
    print(f"状态: {task_result['status']}")
    print(f"结果: {task_result['answer']}")
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
import logging

# 启用日志
logging.basicConfig(level=logging.INFO)

try:
    with AIClient() as client:
        response = client.chat.completions.create(
            model="yuanbao",
            messages=[{"role": "user", "content": "你好"}]
        )
        print(response.choices[0].message.content)

except AuthenticationError as e:
    print(f"认证失败: {e}")
    print("请检查 AI_API_TOKEN 是否正确")

except InvalidRequestError as e:
    print(f"请求参数错误: {e}")
    print("请检查请求参数是否正确")

except TimeoutError as e:
    print(f"请求超时: {e}")
    print("请尝试增加超时时间或稍后重试")

except AIAPIError as e:
    print(f"API错误: {e}")
    print(f"状态码: {e.status_code}")
    print(f"响应: {e.response}")
```

### 7. 批量处理

```python
from ai_sdk import AIClient
import concurrent.futures

def process_question(client, question):
    """处理单个问题"""
    try:
        response = client.chat.completions.create(
            model="yuanbao",
            messages=[{"role": "user", "content": question}]
        )
        return {
            "question": question,
            "answer": response.choices[0].message.content,
            "success": True
        }
    except Exception as e:
        return {
            "question": question,
            "error": str(e),
            "success": False
        }

# 批量问题列表
questions = [
    "什么是Python？",
    "什么是JavaScript？",
    "什么是Go语言？",
    "什么是Rust？"
]

with AIClient() as client:
    # 串行处理
    results = []
    for q in questions:
        result = process_question(client, q)
        results.append(result)

    # 输出结果
    for r in results:
        if r["success"]:
            print(f"Q: {r['question']}")
            print(f"A: {r['answer'][:100]}...")
            print()
```

## 最佳实践

### 1. 使用上下文管理器

推荐使用 `with` 语句，自动管理资源：

```python
# ✅ 推荐
with AIClient() as client:
    response = client.chat.completions.create(...)

# ❌ 不推荐
client = AIClient()
response = client.chat.completions.create(...)
# 容易忘记调用 client.close()
```

### 2. 合理设置超时

根据任务复杂度设置合适的超时时间：

```python
# 简单查询 - 短超时
client = AIClient(timeout=30)

# 深度研究 - 长超时
client = AIClient(timeout=120)
```

### 3. 启用日志调试

开发时启用详细日志：

```python
import logging

# 开发环境
logging.basicConfig(level=logging.DEBUG)

# 生产环境
logging.basicConfig(level=logging.INFO)
```

### 4. 妥善处理异常

始终捕获和处理可能的异常：

```python
from ai_sdk import AIClient, AIAPIError

try:
    with AIClient() as client:
        response = client.chat.completions.create(...)
except AIAPIError as e:
    logging.error(f"API调用失败: {e}")
    # 实施降级方案或重试逻辑
```

### 5. 保护敏感信息

永远不要在代码中硬编码Token：

```python
# ❌ 危险
client = AIClient(api_token="spsw.your_token")

# ✅ 安全
client = AIClient()  # 从环境变量读取
```

## 故障排查

### 问题1: 导入失败

**错误**: `ModuleNotFoundError: No module named 'ai_sdk'`

**解决方案**:
```bash
# 确保在项目根目录
cd /path/to/my_ai_api

# 确保依赖已安装
pip install -r requirements.txt

# 验证安装
python verify_installation.py
```

### 问题2: 认证失败

**错误**: `AuthenticationError: 认证失败，请检查API Token是否正确`

**解决方案**:
1. 检查 `.env` 文件是否存在
2. 检查 `AI_API_TOKEN` 是否正确
3. 确认Token格式：`spsw.xxxxxxxxxx`

### 问题3: 连接失败

**错误**: `APIConnectionError: 网络连接错误`

**解决方案**:
1. 检查 `AI_API_BASE_URL` 是否正确
2. 确认服务器是否可访问
3. 检查网络连接

### 问题4: 请求超时

**错误**: `TimeoutError: 请求超时`

**解决方案**:
```python
# 增加超时时间
client = AIClient(timeout=60)

# 或在环境变量中设置
# AI_API_TIMEOUT=60
```

### 问题5: 参数错误

**错误**: `InvalidRequestError: messages参数不能为空`

**解决方案**:
确保提供了必要的参数：
```python
# ❌ 错误
client.chat.completions.create(model="yuanbao")

# ✅ 正确
client.chat.completions.create(
    model="yuanbao",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 启用调试模式

遇到问题时，启用调试日志查看详细信息：

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 然后运行你的代码
from ai_sdk import AIClient
# ...
```

## 获取帮助

- 查看 [README.md](README.md) - 完整文档
- 查看 [QUICKSTART.md](QUICKSTART.md) - 快速开始
- 查看 [examples/](examples/) - 示例代码
- 运行 `python verify_installation.py` - 检查安装
- 查看 [API文档](https://docs.apipost.net/docs/detail/52c44bf47843000) - 官方文档

---

祝你使用愉快！如有问题欢迎反馈。
