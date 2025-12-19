# API差异分析 - 文档 vs 当前实现

## 一、提交任务接口差异

### 文档中的规范（✅ 正确）
```json
// 成功响应
{
  "code": 0,
  "data": 1407075418509568,  // 任务ID直接是数字
  "message": "创建成功"
}

// 失败响应
{
  "code": 1,  // 非0表示失败
  "message": "错误信息"
}
```

### 当前SDK实现
```python
# 检查响应码（成功时 code 为 0）
if code != 0:
    error_msg = f"API请求失败: {message}" if message else "API请求失败"
    raise InvalidRequestError(error_msg)

# 解析响应数据 - data 直接就是任务ID
task_id = response.get("data")
```

**✅ 这部分实现正确！**

---

## 二、查询结果接口差异（⚠️ 重要！）

### 文档中的规范

#### 1. 任务处理中
```json
{
  "code": 0,
  "answer": "",
  "message": "AI任务待处理"  // 或 "AI任务处理中"
}
```

#### 2. 任务完成
```json
{
  "code": 0,
  "answer": "完整的AI生成内容...",
  "message": "AI任务处理完成"
}
```

#### 3. 任务失败
```json
{
  "code": 0,
  "answer": "错误信息",
  "message": "AI任务处理失败"
}
```

### ⚠️ 关键发现：
**无论任务是否完成，code 都是 0！**

判断任务状态的**唯一依据**是 `message` 字段：
- `"AI任务待处理"` → 继续轮询
- `"AI任务处理中"` → 继续轮询
- `"AI任务处理完成"` → 任务完成
- `"AI任务处理失败"` → 任务失败

### 文档中的判断逻辑
```python
# 判断任务是否完成
success = message == "AI任务处理完成"
failed = message == "AI任务处理失败"
has_result = bool(answer and answer.strip() and len(answer.strip()) > 10)

if failed:
    # 任务失败
    return None

if success and has_result:
    # 任务成功完成
    return answer
elif has_result:
    # 有结果但message不是"完成"，也认为完成了
    return answer
else:
    # 任务还在处理中，需要继续查询
    time.sleep(check_interval)
```

---

## 三、当前SDK实现的问题

### 当前代码（❌ 错误）
```python
# 检查响应码
code = result_response.get("code")
message = result_response.get("message", "")

# code=0 表示成功/完成  ← ❌ 错误理解
if code == 0:
    # 任务完成，获取答案  ← ❌ code=0不代表完成
    content = result_response.get("answer")
    ...
    return ChatCompletion(...)

# code != 0 表示任务还在处理中或出错  ← ❌ 永远不会走到这里
else:
    ...
```

### 问题说明
1. **误解了 code 的含义**：code=0 只表示API请求成功，不代表任务完成
2. **没有判断 message**：应该根据 message 字段判断任务状态
3. **缺少轮询逻辑**：任务处理中时应该继续轮询，而不是直接返回

---

## 四、正确的实现逻辑

### 应该这样实现：

```python
for retry in range(max_retries):
    try:
        # 查询任务结果
        result_response = self._client._post(
            "/chatResult", json={"id": task_id}
        )

        # 获取响应字段
        code = result_response.get("code")
        message = result_response.get("message", "")
        answer = result_response.get("answer", "")

        # 检查API调用是否成功
        if code != 0:
            # code != 0 表示API调用失败（不是任务失败）
            logger.error(f"API call failed: {message}")
            time.sleep(interval)
            continue

        # code == 0，通过 message 判断任务状态

        # 1. 检查任务失败
        if message == "AI任务处理失败":
            error_msg = answer if answer else "任务执行失败"
            logger.error(f"Task {task_id} failed: {error_msg}")
            raise InvalidRequestError(f"任务执行失败: {error_msg}")

        # 2. 检查任务完成
        if message == "AI任务处理完成":
            # 验证是否有有效答案
            has_result = bool(answer and answer.strip() and len(answer.strip()) > 10)
            if has_result:
                logger.info(f"Task {task_id} completed successfully")
                return ChatCompletion(...)
            else:
                logger.warning(f"Task completed but answer is empty")
                # 可能需要继续等待
                time.sleep(interval)
                continue

        # 3. 任务处理中（"AI任务待处理" 或 "AI任务处理中"）
        if "处理中" in message or "待处理" in message:
            logger.debug(f"Task {task_id} is {message}, retry {retry + 1}/{max_retries}")
            time.sleep(interval)
            continue

        # 4. 兜底：有答案就返回（文档中提到的情况）
        has_result = bool(answer and answer.strip() and len(answer.strip()) > 10)
        if has_result:
            logger.info(f"Task {task_id} has result (message: {message})")
            return ChatCompletion(...)

        # 5. 未知状态，继续等待
        logger.warning(f"Unknown message: {message}, will retry")
        time.sleep(interval)

    except InvalidRequestError:
        raise
    except Exception as e:
        logger.warning(f"Error checking task status: {e}")
        time.sleep(interval)

# 超时
raise TimeoutError(f"任务 {task_id} 超时")
```

---

## 五、修复清单

### ✅ 需要修复的部分

1. **响应状态判断**
   - [ ] 修改：不要把 `code=0` 当作任务完成的标志
   - [ ] 添加：根据 `message` 字段判断任务状态
   - [ ] 添加：检查 `answer` 内容的有效性

2. **轮询逻辑**
   - [ ] 修改：处理中状态应该继续轮询，不是返回
   - [ ] 添加：明确识别 "AI任务待处理"、"AI任务处理中"、"AI任务处理完成"、"AI任务处理失败"

3. **错误处理**
   - [ ] 修改：区分API错误和任务失败
   - [ ] 添加：对 "AI任务处理失败" 的专门处理

### ✅ 保持不变的部分

1. **提交任务接口** - 实现正确
2. **base_url 配置** - 8088端口正确
3. **Token 认证** - x-custom-token 正确

---

## 六、测试验证

### 测试场景

1. **正常完成**
   ```python
   response = client.chat.completions.create(
       model="gemini",
       messages=[{"role": "user", "content": "1+1等于几？"}]
   )
   # 应该成功返回答案
   ```

2. **深度研究（长时间任务）**
   ```python
   response = client.chat.completions.create(
       model="gemini",
       messages=[{"role": "user", "content": "深度分析股票"}],
       deep_research=True
   )
   # 应该正确轮询并等待完成
   ```

3. **任务失败**
   ```python
   # 测试错误场景
   # 应该抛出 InvalidRequestError
   ```

---

## 七、总结

### 核心差异

| 方面 | 文档规范 | 当前实现 | 状态 |
|------|---------|---------|------|
| 提交任务响应 | code=0成功，data是任务ID | ✅ 正确 | ✅ |
| 查询结果 code | 始终为0 | ❌ 误认为0表示完成 | ❌ |
| 任务状态判断 | 根据message字段 | ❌ 根据code判断 | ❌ |
| 轮询逻辑 | 处理中继续轮询 | ❌ 直接返回 | ❌ |
| 答案验证 | 检查长度>10 | ❌ 没有验证 | ❌ |

### 关键问题
**当前实现误解了响应格式，把 `code=0` 当作任务完成，实际上应该通过 `message` 判断。**

---

## 八、修复优先级

1. **🔴 紧急**：修复查询结果的状态判断逻辑
2. **🔴 紧急**：添加基于 message 的任务状态识别
3. **🟡 重要**：添加 answer 内容验证
4. **🟢 一般**：优化日志输出

