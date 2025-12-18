# AI SDK - 兼容 OpenAI 的 Python SDK

<div align="center">

**一个完整的、生产级的 AI SDK，兼容 OpenAI SDK 接口风格**

[![GitHub](https://img.shields.io/badge/GitHub-randbear%2Fai--sdk-blue?logo=github)](https://github.com/randbear/ai-sdk)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

[快速开始](quickstart.md){ .md-button .md-button--primary }
[GitHub 仓库](https://github.com/randbear/ai-sdk){ .md-button }

</div>

---

## ✨ 特性

- ✅ **兼容 OpenAI SDK** - 熟悉的 API 接口，快速上手
- ✅ **类型提示完善** - 完整的类型注解，IDE 友好
- ✅ **错误处理健全** - 详细的异常类型和错误信息
- ✅ **环境变量管理** - 安全地管理 API Token 等敏感信息
- ✅ **多模型支持** - 支持元宝(Yuanbao)和 Gemini 模型
- ✅ **图片分析** - 支持图片 URL 和 Base64 数据
- ✅ **图片生成** - AI 生成各种风格的图片
- ✅ **深度研究** - 支持启用深度研究模式
- ✅ **任务管理** - 支持查询任务状态和结果

---

## 🚀 快速开始

### 安装

```bash
pip install git+https://github.com/randbear/ai-sdk.git
```

### 配置

创建 `.env` 文件：

```env
AI_API_TOKEN=your_token_here
```

> SDK 已内置默认服务地址，无需配置 base_url

### 使用

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

**查看 [快速开始指南](quickstart.md) 了解更多**

---

## 📚 功能演示

### 基础对话

```python
with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "什么是 SEO？"}]
    )
    print(response.choices[0].message.content)
```

### 图片生成 🎨

```python
with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "生成一张未来城市的图片"}],
        generate_image=True  # ← 启用图片生成
    )
    print(response.choices[0].message.content)
```

### 图片分析 🔍

```python
with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "描述这张图片"}],
        image_url="http://example.com/image.png"
    )
    print(response.choices[0].message.content)
```

### 深度研究 🔬

```python
with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "人工智能的发展历史"}],
        deep_research=True  # ← 启用深度研究
    )
    print(response.choices[0].message.content)
```

---

## 📖 文档导航

<div class="grid cards" markdown>

-   :material-rocket-launch: **快速开始**

    ---

    5 分钟快速上手指南

    [:octicons-arrow-right-24: 开始使用](quickstart.md)

-   :material-book-open-variant: **使用手册**

    ---

    完整的功能使用文档

    [:octicons-arrow-right-24: 查看手册](usage.md)

-   :material-image-plus: **图片生成**

    ---

    AI 图片生成专题指南

    [:octicons-arrow-right-24: 了解更多](image-generation.md)

-   :material-github: **发布指南**

    ---

    如何发布到 GitHub

    [:octicons-arrow-right-24: 发布文档](publish-guide.md)

-   :material-code-braces: **API 参考**

    ---

    详细的 API 文档

    [:octicons-arrow-right-24: API 文档](api-reference.md)

-   :material-file-code: **示例代码**

    ---

    丰富的示例程序

    [:octicons-arrow-right-24: 查看示例](examples/basic-chat.md)

</div>

---

## 🎯 核心优势

| 特性 | 说明 |
|-----|------|
| **简单易用** | 兼容 OpenAI SDK，无学习成本 |
| **类型安全** | 完整的类型提示，IDE 智能提示 |
| **健壮可靠** | 完善的错误处理，详细的日志 |
| **安全第一** | 环境变量管理，敏感信息保护 |
| **文档完善** | 10+ 份文档，覆盖所有场景 |

---

## 💻 在 requirements.txt 中使用

```txt
# 安装最新版
git+https://github.com/randbear/ai-sdk.git

# 或指定版本（推荐）
git+https://github.com/randbear/ai-sdk.git@v0.1.0
```

然后：

```bash
pip install -r requirements.txt
```

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

- [GitHub Issues](https://github.com/randbear/ai-sdk/issues)
- [Pull Requests](https://github.com/randbear/ai-sdk/pulls)

---

## 📄 许可证

MIT License - 查看 [LICENSE](https://github.com/randbear/ai-sdk/blob/master/LICENSE) 了解更多

---

## 🔗 相关链接

- [GitHub 仓库](https://github.com/randbear/ai-sdk)
- [问题反馈](https://github.com/randbear/ai-sdk/issues)
- [更新日志](https://github.com/randbear/ai-sdk/releases)

---

<div align="center">

**开始使用 AI SDK** 🚀

[查看文档](quickstart.md) · [GitHub](https://github.com/randbear/ai-sdk) · [报告问题](https://github.com/randbear/ai-sdk/issues)

</div>
