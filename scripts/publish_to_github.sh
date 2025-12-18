#!/bin/bash
# 发布到 GitHub 私有仓库的脚本

set -e  # 遇到错误立即退出

echo "=========================================="
echo "AI SDK - 发布到 GitHub 私有仓库"
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

# 获取用户输入
read -p "请输入仓库名称 (默认: ai-sdk): " REPO_NAME
REPO_NAME=${REPO_NAME:-ai-sdk}

read -p "请输入版本号 (默认: v0.1.0): " VERSION
VERSION=${VERSION:-v0.1.0}

echo ""
echo "配置信息:"
echo "  仓库名称: $REPO_NAME"
echo "  版本号: $VERSION"
echo "  类型: 私有仓库"
echo ""

read -p "确认发布？(y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
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
echo "🚀 创建 GitHub 私有仓库..."

# 创建仓库并推送
if gh repo create "$REPO_NAME" --private --source=. --push; then
    echo "✅ 仓库创建成功！"
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
echo "  版本: $VERSION"
echo ""

echo "📚 在其他项目中安装:"
echo ""
echo "  1. 创建 Personal Access Token:"
echo "     https://github.com/settings/tokens"
echo ""
echo "  2. 安装命令:"
echo "     export GITHUB_TOKEN=your_token_here"
echo "     pip install git+https://\${GITHUB_TOKEN}@github.com/$GITHUB_USER/$REPO_NAME.git"
echo ""
echo "  3. 安装特定版本:"
echo "     pip install git+https://\${GITHUB_TOKEN}@github.com/$GITHUB_USER/$REPO_NAME.git@$VERSION"
echo ""

echo "🌐 在浏览器中打开仓库？(y/n): "
read -p "" OPEN_BROWSER
if [ "$OPEN_BROWSER" == "y" ]; then
    gh repo view --web
fi

echo ""
echo "完成！"
