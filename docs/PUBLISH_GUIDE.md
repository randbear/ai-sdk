# 快速发布指南

## 💡 首先选择：Public 还是 Private？

### ✅ 推荐：Public Repo（公开仓库）

**优势**：
- 🚀 **安装超级简单** - 无需配置 token
- 📦 **一行命令安装** - `pip install git+https://github.com/YOUR_USERNAME/ai-sdk.git`
- 🤝 **易于分享** - 可以分享给任何人
- 🌟 **支持协作** - 方便接受 Pull Request

**安全性**：
- ✅ 代码本身不包含敏感信息
- ✅ API token 通过环境变量配置（.env）
- ✅ .gitignore 已正确配置

> 📖 详细对比请查看 [PUBLIC_VS_PRIVATE.md](PUBLIC_VS_PRIVATE.md)

### ⚠️ 可选：Private Repo（私有仓库）

**适用场景**：
- 🔒 包含商业机密
- 🏢 仅限内部使用
- 🔐 需要访问控制

**缺点**：
- 需要创建 GitHub token
- 安装时需要配置环境变量
- 每个环境都要配置

---

## 🚀 方法 1: 一键发布脚本（推荐）

### Public Repo（推荐）⭐

```bash
# 发布为 Public 仓库
./scripts/publish_to_github_public.sh
```

**特点**：
- 自动安全检查
- 检测敏感信息
- 创建 Public 仓库
- 安装超级简单

### Private Repo

```bash
# 发布为 Private 仓库
./scripts/publish_to_github.sh
```

按提示输入：
- 仓库名称（默认: ai-sdk）
- 版本号（默认: v0.1.0）

脚本会自动完成：
1. ✅ 初始化 Git 仓库
2. ✅ 创建 GitHub 仓库（Public 或 Private）
3. ✅ 推送代码
4. ✅ 创建版本标签

---

## 📦 方法 2: 手动发布

### 步骤 1: 初始化并提交

```bash
git init
git add .
git commit -m "Initial commit: AI SDK v0.1.0"
```

### 步骤 2: 创建 GitHub 仓库

**Public Repo（推荐）⭐**：
```bash
gh repo create ai-sdk --public --source=. --push
```

**Private Repo**：
```bash
gh repo create ai-sdk --private --source=. --push
```

### 步骤 3: 创建版本标签（可选）

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

---

## 💻 在其他项目中安装

### Public Repo - 超级简单！⭐

**无需任何配置，直接安装：**

```bash
# 安装最新版
pip install git+https://github.com/YOUR_USERNAME/ai-sdk.git

# 安装特定版本
pip install git+https://github.com/YOUR_USERNAME/ai-sdk.git@v0.1.0
```

**在 requirements.txt 中：**

```txt
git+https://github.com/YOUR_USERNAME/ai-sdk.git
```

就这么简单！🎉

---

### Private Repo - 需要配置 Token

#### 前置步骤：创建 Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制 token

### 方法 1: 环境变量方式（推荐）

```bash
# 设置 token
export GITHUB_TOKEN=ghp_your_token_here

# 安装最新版
pip install git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git

# 安装特定版本
pip install git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git@v0.1.0
```

### 方法 2: 使用 requirements.txt

创建 `requirements.txt`:

```txt
# 需要先设置 GITHUB_TOKEN 环境变量
git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git
```

安装:

```bash
export GITHUB_TOKEN=ghp_your_token_here
pip install -r requirements.txt
```

### 方法 3: 使用安装脚本

```bash
export GITHUB_TOKEN=ghp_your_token_here
./scripts/install_example.sh
```

---

## ✅ 验证安装

```python
# test.py
from ai_sdk import AIClient

# 测试导入
print("✅ AI SDK 安装成功！")

# 测试功能（需要配置 API token）
with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "你好"}]
    )
    print(response.choices[0].message.content)
```

---

## 📋 常用命令速查

```bash
# 发布新版本
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0

# 更新到最新版
pip install --upgrade git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git

# 卸载
pip uninstall ai-sdk

# 查看已安装版本
pip show ai-sdk
```

---

## 🔧 故障排查

### 问题: 认证失败

```bash
ERROR: Repository not found or authentication failed
```

**解决**: 检查 token 是否有效，是否有 `repo` 权限

### 问题: 找不到仓库

```bash
ERROR: Could not find a version that satisfies the requirement
```

**解决**: 确认仓库名称和用户名正确

---

## 📚 完整文档

- [GITHUB_SETUP.md](GITHUB_SETUP.md) - 详细的发布和安装指南
- [README.md](README.md) - 项目使用文档

---

**提示**: 第一次发布建议阅读 [GITHUB_SETUP.md](GITHUB_SETUP.md) 了解详细流程。
