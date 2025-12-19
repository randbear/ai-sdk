# OpenAI协议接口完整文档

## 📋 目录
- [概述](#概述)
- [基础配置](#基础配置)
- [接口详情](#接口详情)
  - [1. 提交任务接口](#1-提交任务接口)
  - [2. 查询结果接口](#2-查询结果接口)
- [响应格式说明](#响应格式说明)
- [代码实现](#代码实现)
- [使用示例](#使用示例)
- [错误处理](#错误处理)
- [注意事项](#注意事项)

---

## 概述

这是一个符合OpenAI协议的AI任务处理接口，支持提交AI任务并异步查询结果。主要用于：
- Gemini深度研究（deepResearch）
- 元宝分析（yuanbao）
- 图片生成（generateImage）

### 特性
- ✅ 异步任务处理
- ✅ 支持深度研究模式
- ✅ 支持图片生成
- ✅ 自动轮询查询结果
- ✅ 完善的错误处理

---

## 基础配置

### API服务器信息
- **基础URL**: `http://156.254.5.245:8088`
- **认证方式**: Token认证（x-custom-token）
- **Token**: `spsw.7464b7d51e71c92311bf76c528192413`

### 接口路径
- **提交任务**: `/api/v1/chatCompletion`
- **查询结果**: `/api/v1/chatResult`

---

## 接口详情

### 1. 提交任务接口

#### 基本信息
- **路径**: `/api/v1/chatCompletion`
- **方法**: `POST`
- **Content-Type**: `application/json`

#### 请求头（Headers）
```http
Content-Type: application/json
x-custom-token: spsw.7464b7d51e71c92311bf76c528192413
```

#### 请求参数（Body）
所有参数都是**必填**：

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| type | integer | 是 | 任务类型：1-元宝，2-gemini | 2 |
| question | string | 是 | 问题内容/提示词 | "请分析股票000001" |
| imageUrl | string | 是 | 图片网络地址（与imageData二选一） | "" |
| imageData | string | 是 | 图片数据（Base64字符串，与imageUrl二选一） | "" |
| deepResearch | integer | 是 | 深度研究标识：0-否，1-是 | 1 |
| generateImage | integer | 是 | 生成图片标识：0-否，1-是 | 0 |

#### 请求示例
```json
{
  "type": 2,
  "question": "请对股票平安银行(000001)进行深度研究分析，包括基本面、技术面、行业分析、投资建议等。",
  "imageUrl": "",
  "imageData": "",
  "deepResearch": 1,
  "generateImage": 0
}
```

#### 响应格式
**成功响应**（HTTP 200）：
```json
{
  "code": 0,
  "data": 1407075418509568,
  "message": "创建成功"
}
```

**响应字段说明**：
- `code`: 状态码，0表示成功
- `data`: 任务ID（数字类型），用于后续查询结果
- `message`: 响应消息

**失败响应**：
```json
{
  "code": 1,
  "message": "错误信息"
}
```

---

### 2. 查询结果接口

#### 基本信息
- **路径**: `/api/v1/chatResult`
- **方法**: `POST`
- **Content-Type**: `application/json`

#### 请求头（Headers）
```http
Content-Type: application/json
x-custom-token: spsw.7464b7d51e71c92311bf76c528192413
```

#### 请求参数（Body）

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| id | integer | 是 | 任务ID（从提交任务接口返回的data字段） | 1407075418509568 |

#### 请求示例
```json
{
  "id": 1407075418509568
}
```

#### 响应格式

**任务处理中**（HTTP 200）：
```json
{
  "code": 0,
  "answer": "",
  "message": "AI任务待处理"
}
```
或
```json
{
  "code": 0,
  "answer": "",
  "message": "AI任务处理中"
}
```

**任务完成**（HTTP 200）：
```json
{
  "code": 0,
  "answer": "完整的AI生成内容...",
  "message": "AI任务处理完成"
}
```

**任务失败**（HTTP 200）：
```json
{
  "code": 0,
  "answer": "错误信息",
  "message": "AI任务处理失败"
}
```

**响应字段说明**：
- `code`: 状态码，0表示请求成功
- `answer`: 任务结果内容（任务完成时包含完整内容）
- `message`: 任务状态消息
  - `"AI任务待处理"` - 任务已提交，等待处理
  - `"AI任务处理中"` - 任务正在处理中
  - `"AI任务处理完成"` - 任务已完成，answer包含结果
  - `"AI任务处理失败"` - 任务失败，answer包含错误信息

---

## 响应格式说明

### 任务状态判断

| message值 | 状态 | 说明 | 是否需要继续查询 |
|-----------|------|------|----------------|
| "AI任务待处理" | 等待中 | 任务已提交，等待处理 | ✅ 是 |
| "AI任务处理中" | 处理中 | 任务正在处理 | ✅ 是 |
| "AI任务处理完成" | 已完成 | 任务完成，answer有内容 | ❌ 否 |
| "AI任务处理失败" | 失败 | 任务失败 | ❌ 否 |

### 结果判断逻辑
```python
# 判断任务是否完成
success = message == "AI任务处理完成"
failed = message == "AI任务处理失败"
has_result = bool(answer and answer.strip() and len(answer.strip()) > 10)

if success and has_result:
    # 任务成功完成
    return answer
elif failed:
    # 任务失败
    return None
else:
    # 任务还在处理中，需要继续查询
    # 继续轮询...
```

---

## 代码实现

### Python客户端实现

#### 完整代码示例
```python
import requests
import time
from typing import Optional, Dict

class OpenAIProtocolClient:
    """OpenAI协议接口客户端"""
    
    def __init__(self, base_url: str = "http://156.254.5.245:8088", 
                 token: str = "spsw.7464b7d51e71c92311bf76c528192413"):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.chat_completion_url = f"{self.base_url}/api/v1/chatCompletion"
        self.chat_result_url = f"{self.base_url}/api/v1/chatResult"
    
    def submit_task(self, question: str, task_type: int = 2, 
                   deep_research: int = 1, generate_image: int = 0,
                   image_url: str = "", image_data: str = "") -> Optional[int]:
        """
        提交AI任务
        
        Args:
            question: 问题内容
            task_type: 任务类型（1-元宝，2-gemini）
            deep_research: 深度研究标识（0-否，1-是）
            generate_image: 生成图片标识（0-否，1-是）
            image_url: 图片URL
            image_data: 图片Base64数据
        
        Returns:
            任务ID，失败返回None
        """
        headers = {
            "Content-Type": "application/json",
            "x-custom-token": self.token
        }
        
        payload = {
            "type": task_type,
            "question": question,
            "imageUrl": image_url,
            "imageData": image_data,
            "deepResearch": deep_research,
            "generateImage": generate_image
        }
        
        try:
            response = requests.post(
                self.chat_completion_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0 and 'data' in data:
                    task_id = int(data['data'])
                    return task_id
            return None
        except Exception as e:
            print(f"提交任务失败: {e}")
            return None
    
    def get_task_result(self, task_id: int, max_wait: int = 300, 
                       check_interval: int = 5) -> Optional[Dict]:
        """
        查询任务结果（带轮询）
        
        Args:
            task_id: 任务ID
            max_wait: 最大等待时间（秒）
            check_interval: 检查间隔（秒）
        
        Returns:
            任务结果字典，失败返回None
        """
        headers = {
            "Content-Type": "application/json",
            "x-custom-token": self.token
        }
        
        payload = {"id": task_id}
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.post(
                    self.chat_result_url,
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('code') == 0 and 'answer' in data:
                        message = data.get("message", "")
                        answer = data['answer']
                        
                        # 判断任务状态
                        success = message == "AI任务处理完成"
                        failed = message == "AI任务处理失败"
                        has_result = bool(answer and answer.strip() and len(answer.strip()) > 10)
                        
                        if failed:
                            return None
                        
                        if success and has_result:
                            return {
                                'code': 0,
                                'answer': answer,
                                'message': message,
                                'task_id': task_id
                            }
                        elif has_result:
                            # 有结果但message不是"完成"，也认为完成了
                            return {
                                'code': 0,
                                'answer': answer,
                                'message': message,
                                'task_id': task_id
                            }
                        else:
                            # 任务还在处理中，等待后重试
                            time.sleep(check_interval)
            except Exception as e:
                print(f"查询任务结果失败: {e}")
                time.sleep(check_interval)
        
        return None  # 超时
```

---

## 使用示例

### 示例1：基础使用（分步调用）

```python
from openai_protocol_client import OpenAIProtocolClient

# 创建客户端
client = OpenAIProtocolClient()

# 步骤1：提交任务
task_id = client.submit_task(
    question="什么是股票？",
    task_type=2,  # gemini
    deep_research=0,
    generate_image=0
)

if task_id:
    print(f"任务提交成功，task_id: {task_id}")
    
    # 步骤2：查询结果（自动轮询）
    result = client.get_task_result(task_id)
    
    if result:
        print(f"任务完成！")
        print(f"结果: {result['answer']}")
    else:
        print("任务失败或超时")
else:
    print("提交任务失败")
```

### 示例2：深度研究股票

```python
from openai_protocol_client import OpenAIProtocolClient

client = OpenAIProtocolClient()

# 深度研究股票
task_id = client.submit_task(
    question="请对股票平安银行(000001)进行深度研究分析，包括基本面、技术面、行业分析、投资建议等。",
    task_type=2,  # gemini
    deep_research=1,  # 启用深度研究
    generate_image=0
)

if task_id:
    result = client.get_task_result(task_id, max_wait=600)  # 等待10分钟
    if result:
        print(result['answer'])
```

### 示例3：元宝分析

```python
from openai_protocol_client import OpenAIProtocolClient

client = OpenAIProtocolClient()

# 使用元宝进行分析
task_id = client.submit_task(
    question="分析当前市场趋势",
    task_type=1,  # 元宝
    deep_research=0,
    generate_image=0
)

if task_id:
    result = client.get_task_result(task_id)
    if result:
        print(result['answer'])
```

### 示例4：图片生成

```python
from openai_protocol_client import OpenAIProtocolClient

client = OpenAIProtocolClient()

# 生成图片
task_id = client.submit_task(
    question="生成一张股票走势图",
    task_type=2,  # gemini
    deep_research=0,
    generate_image=1  # 启用图片生成
)

if task_id:
    result = client.get_task_result(task_id)
    if result:
        # 图片URL或Base64数据在answer中
        print(result['answer'])
```

---

## 错误处理

### 常见错误及处理

#### 1. 连接错误
```python
try:
    task_id = client.submit_task(...)
except requests.exceptions.ConnectionError:
    print("无法连接到API服务器，请检查网络和服务器状态")
```

#### 2. 超时错误
```python
try:
    result = client.get_task_result(task_id, max_wait=300)
except requests.exceptions.Timeout:
    print("请求超时，请稍后重试")
```

#### 3. 任务失败
```python
result = client.get_task_result(task_id)
if not result:
    print("任务失败或超时")
    # 可以重试或记录错误
```

#### 4. 账号限制
```json
{
  "code": 0,
  "answer": "账号达到使用限制",
  "message": "AI任务处理失败"
}
```
处理：检查账号配额，等待或升级账号

---

## 注意事项

### ⚠️ 重要提示

1. **端口号**：API服务器端口是 `8088`，不是 `8089`
2. **Token认证**：必须在请求头中包含 `x-custom-token`
3. **任务ID类型**：task_id是数字类型，不是字符串
4. **轮询间隔**：建议查询间隔为3-5秒，避免过于频繁
5. **超时设置**：根据任务复杂度设置合理的超时时间
   - 简单任务：60-120秒
   - 深度研究：300-600秒
   - 图片生成：120-300秒

### 最佳实践

1. **错误重试**：对于网络错误，可以实现重试机制
2. **任务状态缓存**：可以缓存任务状态，避免重复查询
3. **批量处理**：对于多个任务，建议使用队列管理
4. **日志记录**：记录所有API调用和错误，便于排查问题

### 性能优化

1. **并发控制**：避免同时提交过多任务
2. **连接复用**：使用 `requests.Session()` 复用连接
3. **异步处理**：对于大量任务，考虑使用异步框架

---

## 参考实现

### 成功案例
参考 `article_gen/utils/api_client.py` 中的实现，该实现已成功对接并稳定运行。

### 相关文件
- `openai_protocol_client.py` - 客户端实现
- `config.py` - 配置信息
- `test_complete_flow.py` - 测试脚本

---

## 更新日志

- **2025-11-19**: 初始文档，基于成功对接的API实现
- 端口：8088
- Token：spsw.7464b7d51e71c92311bf76c528192413

---

## 联系方式

如有问题，请参考：
- API文档：https://openapi.apipost.net/swagger/v3/52c44bf47843000?locale=zh-cn
- 成功实现：`article_gen/utils/api_client.py`

