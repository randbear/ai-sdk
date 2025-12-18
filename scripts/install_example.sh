#!/bin/bash
# 在其他项目中安装 AI SDK 的示例脚本

set -e

echo "=========================================="
echo "AI SDK - 安装脚本"
echo "=========================================="
echo ""

# 检查是否设置了 GITHUB_TOKEN
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  未设置 GITHUB_TOKEN 环境变量"
    echo ""
    echo "请按以下步骤操作:"
    echo ""
    echo "1. 创建 Personal Access Token:"
    echo "   访问: https://github.com/settings/tokens"
    echo "   - 点击 'Generate new token (classic)'"
    echo "   - 勾选 'repo' 权限"
    echo "   - 生成并复制 token"
    echo ""
    echo "2. 设置环境变量:"
    echo "   export GITHUB_TOKEN=ghp_your_token_here"
    echo ""
    echo "3. 重新运行此脚本"
    echo ""
    exit 1
fi

echo "✅ GITHUB_TOKEN 已设置"
echo ""

# 获取用户输入
read -p "请输入 GitHub 用户名: " GITHUB_USER
read -p "请输入仓库名称 (默认: ai-sdk): " REPO_NAME
REPO_NAME=${REPO_NAME:-ai-sdk}

read -p "是否安装特定版本？(留空安装最新版): " VERSION

echo ""
echo "配置信息:"
echo "  用户名: $GITHUB_USER"
echo "  仓库: $REPO_NAME"
if [ -n "$VERSION" ]; then
    echo "  版本: $VERSION"
else
    echo "  版本: latest (main分支)"
fi
echo ""

# 构建安装 URL
if [ -n "$VERSION" ]; then
    INSTALL_URL="git+https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git@${VERSION}"
else
    INSTALL_URL="git+https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"
fi

echo "📦 开始安装..."
echo ""

# 安装包
pip install "$INSTALL_URL"

echo ""
echo "=========================================="
echo "✅ 安装完成！"
echo "=========================================="
echo ""

echo "🎯 测试安装:"
echo ""
python -c "from ai_sdk import AIClient; print('✅ AI SDK 导入成功！')"

echo ""
echo "📖 使用示例:"
echo ""
cat << 'EOF'
from ai_sdk import AIClient

# 确保配置了环境变量
# export AI_API_TOKEN=spsw.xxx
# export AI_API_BASE_URL=http://your_server/api/v1

with AIClient() as client:
    response = client.chat.completions.create(
        model="yuanbao",
        messages=[{"role": "user", "content": "你好"}]
    )
    print(response.choices[0].message.content)
EOF

echo ""
echo "完成！"
