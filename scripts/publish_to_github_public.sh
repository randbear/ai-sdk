#!/bin/bash
# 发布到 GitHub Public 仓库的脚本

set -e  # 遇到错误立即退出

echo "=========================================="
echo "AI SDK - 发布到 GitHub Public 仓库"
echo "=========================================="
echo ""

# 检查是否安装了 gh
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) 未安装"
    echo "请先安装: brew install gh"
    echo "或访问: https://cli.github.com/"
    exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "❌ 未登录 GitHub"
    echo "请先运行: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI 已安装并登录"
echo ""

# 安全检查
echo "⚠️  重要提示："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Public 仓库意味着代码完全公开！"
echo ""
echo "  请确认："
echo "  ✅ .gitignore 已正确配置"
echo "  ✅ .env 文件不在版本控制中"
echo "  ✅ 代码中没有硬编码的密码、token等"
echo "  ✅ ai_api_info.txt 已在 .gitignore 中"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 运行安全检查
echo "🔍 运行安全检查..."
echo ""

# 检查 .gitignore
if [ ! -f .gitignore ]; then
    echo "❌ 缺少 .gitignore 文件"
    exit 1
fi

# 检查敏感文件是否被忽略
if grep -q "^\.env$" .gitignore; then
    echo "✅ .env 已在 .gitignore 中"
else
    echo "⚠️  .env 不在 .gitignore 中"
    read -p "是否添加 .env 到 .gitignore？(y/n): " ADD_ENV
    if [ "$ADD_ENV" == "y" ]; then
        echo ".env" >> .gitignore
        echo "✅ 已添加 .env 到 .gitignore"
    fi
fi

# 检查是否有 .env 文件被追踪
if git ls-files | grep -q "^\.env$"; then
    echo "❌ 警告：.env 文件已被 Git 追踪！"
    echo "请先运行: git rm --cached .env"
    exit 1
fi

# 检查可能的敏感信息
echo ""
echo "🔍 检查可能的敏感信息..."
SENSITIVE_PATTERNS="password|secret|private_key|api_key"
if git grep -i -E "$SENSITIVE_PATTERNS" -- ':!.env.example' ':!*.md' ':!.gitignore' &> /dev/null; then
    echo "⚠️  发现可能的敏感信息："
    git grep -i -n -E "$SENSITIVE_PATTERNS" -- ':!.env.example' ':!*.md' ':!.gitignore' || true
    echo ""
    read -p "确认这些不是真实的敏感信息？(y/n): " CONFIRM_SAFE
    if [ "$CONFIRM_SAFE" != "y" ]; then
        echo "请先清理敏感信息"
        exit 1
    fi
else
    echo "✅ 未发现明显的敏感信息"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 获取用户输入
read -p "请输入仓库名称 (默认: ai-sdk): " REPO_NAME
REPO_NAME=${REPO_NAME:-ai-sdk}

read -p "请输入版本号 (默认: v0.1.0): " VERSION
VERSION=${VERSION:-v0.1.0}

read -p "请输入仓库描述 (可选): " REPO_DESC
REPO_DESC=${REPO_DESC:-"兼容OpenAI SDK的AI API客户端"}

echo ""
echo "配置信息:"
echo "  仓库名称: $REPO_NAME"
echo "  版本号: $VERSION"
echo "  类型: Public 仓库 (公开)"
echo "  描述: $REPO_DESC"
echo ""

echo "⚠️  最后确认：将创建 PUBLIC 仓库，代码将完全公开！"
read -p "确认发布为 Public 仓库？(输入 'YES' 确认): " FINAL_CONFIRM
if [ "$FINAL_CONFIRM" != "YES" ]; then
    echo "取消发布"
    exit 0
fi

echo ""
echo "开始发布..."
echo ""

# 检查是否已经是 git 仓库
if [ ! -d .git ]; then
    echo "📦 初始化 Git 仓库..."
    git init

    echo "📝 添加文件..."
    git add .

    echo "💾 创建初始提交..."
    git commit -m "Initial commit: AI SDK $VERSION

- 兼容OpenAI SDK的接口设计
- 支持元宝和Gemini模型
- 支持图片分析和生成
- 完善的错误处理和日志
- 详细的文档和示例

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
else
    echo "✅ Git 仓库已存在"

    # 检查是否有未提交的更改
    if ! git diff-index --quiet HEAD --; then
        echo "⚠️  发现未提交的更改"
        read -p "是否提交这些更改？(y/n): " COMMIT_CHANGES
        if [ "$COMMIT_CHANGES" == "y" ]; then
            git add .
            read -p "请输入提交信息: " COMMIT_MSG
            git commit -m "$COMMIT_MSG"
        fi
    fi
fi

echo ""
echo "🚀 创建 GitHub Public 仓库..."

# 创建 public 仓库
if [ -n "$REPO_DESC" ]; then
    CREATE_CMD="gh repo create \"$REPO_NAME\" --public --description \"$REPO_DESC\" --source=. --push"
else
    CREATE_CMD="gh repo create \"$REPO_NAME\" --public --source=. --push"
fi

if eval $CREATE_CMD; then
    echo "✅ Public 仓库创建成功！"
else
    echo "⚠️  仓库可能已存在，尝试推送到现有仓库..."

    # 获取当前用户名
    GITHUB_USER=$(gh api user -q .login)

    # 添加远程仓库（如果不存在）
    if ! git remote get-url origin &> /dev/null; then
        git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
    fi

    # 推送代码
    git push -u origin main || git push -u origin master
fi

echo ""
echo "🏷️  创建版本标签..."
git tag -a "$VERSION" -m "Release $VERSION"
git push origin "$VERSION"

echo ""
echo "=========================================="
echo "✅ 发布完成！"
echo "=========================================="
echo ""

# 获取仓库 URL
GITHUB_USER=$(gh api user -q .login)
REPO_URL="https://github.com/$GITHUB_USER/$REPO_NAME"

echo "📦 仓库信息:"
echo "  URL: $REPO_URL"
echo "  类型: Public (公开)"
echo "  版本: $VERSION"
echo ""

echo "🎉 Public 仓库的优势："
echo "  ✅ 无需配置 token"
echo "  ✅ 安装超级简单"
echo "  ✅ 可以分享给任何人"
echo "  ✅ 支持协作开发"
echo ""

echo "📚 在其他项目中安装（超级简单）："
echo ""
echo "  安装命令（无需任何配置）:"
echo "  ┌────────────────────────────────────────────┐"
echo "  │ pip install git+$REPO_URL.git │"
echo "  └────────────────────────────────────────────┘"
echo ""
echo "  安装特定版本:"
echo "  pip install git+$REPO_URL.git@$VERSION"
echo ""

echo "📝 在 requirements.txt 中:"
echo "  git+$REPO_URL.git"
echo ""

echo "🌐 在浏览器中打开仓库？(y/n): "
read -p "" OPEN_BROWSER
if [ "$OPEN_BROWSER" == "y" ]; then
    gh repo view --web
fi

echo ""
echo "完成！你的 SDK 现在可以被任何人轻松安装和使用！🎊"
