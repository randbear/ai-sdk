# GitHub 私有仓库发布和安装指南

本指南将帮助你使用 GitHub CLI 将项目发布为私有仓库，并在其他项目中通过 pip 安装。

## 前置要求

1. **安装 GitHub CLI**

```bash
# macOS
brew install gh

# 或访问 https://cli.github.com/ 下载
```

2. **登录 GitHub**

```bash
gh auth login
```

按提示选择：
- GitHub.com
- HTTPS
- 使用浏览器登录或 token

---

## 步骤 1: 初始化 Git 仓库

```bash
# 进入项目目录
cd /Users/zhangxiatian/websites/my_ai_api

# 初始化 git 仓库
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: AI SDK v0.1.0

- 兼容OpenAI SDK的接口设计
- 支持元宝和Gemini模型
- 支持图片分析和生成
- 完善的错误处理和日志
- 详细的文档和示例

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 步骤 2: 创建 GitHub 私有仓库

使用 GitHub CLI 创建私有仓库：

```bash
# 创建私有仓库并推送
gh repo create ai-sdk --private --source=. --push

# 或者分步操作：
# 1. 只创建仓库（不推送）
gh repo create ai-sdk --private --source=.

# 2. 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/ai-sdk.git

# 3. 推送代码
git push -u origin main
```

**参数说明**:
- `ai-sdk` - 仓库名称（可自定义）
- `--private` - 创建私有仓库
- `--source=.` - 使用当前目录作为源
- `--push` - 立即推送代码

---

## 步骤 3: 验证仓库创建

```bash
# 查看仓库信息
gh repo view

# 在浏览器中打开仓库
gh repo view --web
```

---

## 步骤 4: 创建 Personal Access Token (PAT)

为了让 pip 能够访问私有仓库，需要创建一个 Personal Access Token。

### 方法 1: 使用 GitHub CLI（推荐）

```bash
gh auth refresh -h github.com -s read:packages
```

### 方法 2: 手动创建

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置：
   - **Note**: `AI SDK Access`
   - **Expiration**: 自定义（建议 No expiration 或 1 year）
   - **Scopes**: 勾选 `repo` (完整访问私有仓库)
4. 点击 "Generate token"
5. **复制并保存 token**（只显示一次！）

---

## 步骤 5: 在其他项目中安装

### 方法 1: 使用 HTTPS 和 Token（推荐）

在需要使用这个包的项目中：

```bash
# 方式 1: 直接安装（需要输入 token）
pip install git+https://github.com/YOUR_USERNAME/ai-sdk.git

# 方式 2: 在 URL 中包含 token（不推荐，会暴露在命令历史中）
pip install git+https://{TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git

# 方式 3: 使用环境变量
export GITHUB_TOKEN=ghp_your_token_here
pip install git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git
```

### 方法 2: 使用 requirements.txt

创建 `requirements.txt`:

```txt
# 方式 1: HTTPS (需要配置 token)
git+https://github.com/YOUR_USERNAME/ai-sdk.git

# 方式 2: 指定分支
git+https://github.com/YOUR_USERNAME/ai-sdk.git@main

# 方式 3: 指定版本标签
git+https://github.com/YOUR_USERNAME/ai-sdk.git@v0.1.0

# 方式 4: 指定提交
git+https://github.com/YOUR_USERNAME/ai-sdk.git@commit_hash
```

然后安装：

```bash
pip install -r requirements.txt
```

### 方法 3: 配置 Git 凭据

**一劳永逸的方法**（推荐用于开发环境）：

```bash
# 配置 Git 凭据助手
git config --global credential.helper store

# 第一次克隆时输入用户名和 token
# 用户名: YOUR_GITHUB_USERNAME
# 密码: YOUR_PERSONAL_ACCESS_TOKEN

# 之后 pip 安装就不需要再输入了
pip install git+https://github.com/YOUR_USERNAME/ai-sdk.git
```

---

## 步骤 6: 在项目中使用

安装完成后，就可以像普通包一样使用：

```python
# your_project/main.py
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "你好"}]
    )
    print(response.choices[0].message.content)
```

---

## 高级配置

### 1. 使用 pyproject.toml（现代方式）

如果你的项目使用 `pyproject.toml`：

```toml
[project]
dependencies = [
    "ai-sdk @ git+https://github.com/YOUR_USERNAME/ai-sdk.git",
]
```

### 2. 使用 pip.conf 配置文件

创建 `~/.pip/pip.conf` (Linux/macOS) 或 `%APPDATA%\pip\pip.ini` (Windows):

```ini
[global]
extra-index-url = https://{TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git
```

### 3. 使用 SSH（如果已配置 SSH key）

```bash
pip install git+ssh://git@github.com/YOUR_USERNAME/ai-sdk.git
```

---

## 版本管理

### 创建版本标签

```bash
# 创建版本标签
git tag -a v0.1.0 -m "Release version 0.1.0"

# 推送标签到 GitHub
git push origin v0.1.0

# 或推送所有标签
git push --tags
```

### 安装特定版本

```bash
# 安装特定版本
pip install git+https://github.com/YOUR_USERNAME/ai-sdk.git@v0.1.0

# 在 requirements.txt 中
git+https://github.com/YOUR_USERNAME/ai-sdk.git@v0.1.0
```

---

## CI/CD 环境配置

### GitHub Actions

在 CI/CD 中使用私有仓库：

```yaml
# .github/workflows/test.yml
- name: Install dependencies
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    pip install git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git
```

### Docker

在 Dockerfile 中：

```dockerfile
# 使用构建参数传递 token
ARG GITHUB_TOKEN

RUN pip install git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git
```

构建时：

```bash
docker build --build-arg GITHUB_TOKEN=${GITHUB_TOKEN} .
```

---

## 安全最佳实践

### ⚠️ 不要做的事情

❌ **不要将 token 直接写在代码或配置文件中**
❌ **不要将 token 提交到版本控制**
❌ **不要在公开的 URL 中包含 token**

### ✅ 应该做的事情

✅ **使用环境变量**
```bash
export GITHUB_TOKEN=ghp_xxx
pip install git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git
```

✅ **使用 .env 文件（但要加入 .gitignore）**
```bash
# .env
GITHUB_TOKEN=ghp_xxx

# .gitignore
.env
```

✅ **使用密钥管理工具**
- macOS: Keychain
- Linux: gnome-keyring
- Windows: Credential Manager

✅ **定期轮换 token**
- 设置过期时间
- 定期更新 token

---

## 故障排查

### 问题 1: 认证失败

```bash
ERROR: Repository not found or authentication failed
```

**解决方案**:
1. 检查 token 是否有效
2. 检查 token 是否有 `repo` 权限
3. 检查仓库名称是否正确
4. 使用 `gh auth status` 检查登录状态

### 问题 2: 权限被拒绝

```bash
Permission denied (publickey)
```

**解决方案**:
- 使用 HTTPS 而不是 SSH，或配置 SSH key

### 问题 3: 无法找到包

```bash
ERROR: Could not find a version that satisfies the requirement
```

**解决方案**:
1. 确保 `setup.py` 配置正确
2. 确保包名称正确
3. 尝试使用完整的 git URL

---

## 完整示例

### 1. 发布到 GitHub

```bash
# 项目根目录
cd /Users/zhangxiatian/websites/my_ai_api

# 初始化并提交
git init
git add .
git commit -m "Initial commit"

# 创建私有仓库并推送
gh repo create ai-sdk --private --source=. --push

# 创建版本标签
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

### 2. 在其他项目中使用

```bash
# 创建新项目
mkdir my-new-project
cd my-new-project

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 配置 token（环境变量）
export GITHUB_TOKEN=ghp_your_token_here

# 安装私有包
pip install git+https://${GITHUB_TOKEN}@github.com/YOUR_USERNAME/ai-sdk.git

# 创建测试文件
cat > test.py << 'EOF'
from ai_sdk import AIClient

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "你好"}]
    )
    print(response.choices[0].message.content)
EOF

# 运行测试
python test.py
```

---

## 总结

✅ **发布流程**:
1. `git init` → 初始化仓库
2. `gh repo create --private` → 创建私有仓库
3. `git push` → 推送代码
4. `git tag` → 创建版本标签（可选）

✅ **安装方法**:
1. 创建 Personal Access Token
2. 使用 `pip install git+https://...` 安装
3. 在代码中正常使用

✅ **最佳实践**:
- 使用环境变量存储 token
- 定期更新 token
- 使用版本标签管理版本
- 不要将敏感信息提交到版本控制

---

## 参考资源

- [GitHub CLI 文档](https://cli.github.com/manual/)
- [pip Git 安装文档](https://pip.pypa.io/en/stable/topics/vcs-support/)
- [Personal Access Token 创建](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub Packages 文档](https://docs.github.com/en/packages)

---

**创建时间**: 2025-12-18
**状态**: ✅ 完整可用
