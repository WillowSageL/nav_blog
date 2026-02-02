#!/bin/bash

# 将已创建的 Issues 添加到 GitHub Project
# 用法: ./add_issues_to_project.sh "项目名称"

set -e

PROJECT_TITLE="${1:-nav_blog UI 升级}"

echo "🚀 开始创建 GitHub Project 并添加 Issues..."

# 获取仓库信息
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
OWNER=$(echo $REPO | cut -d'/' -f1)

echo "📦 仓库: $REPO"
echo "📋 项目名称: $PROJECT_TITLE"
echo ""

# 检查 Project 是否已存在
echo "🔍 检查 Project 是否存在..."
EXISTING_PROJECT=$(gh project list --owner $OWNER --format json | jq -r ".projects[] | select(.title == \"$PROJECT_TITLE\") | .number" 2>/dev/null || echo "")

if [ -n "$EXISTING_PROJECT" ]; then
    PROJECT_NUMBER=$EXISTING_PROJECT
    echo "✓ Project 已存在: #$PROJECT_NUMBER"
else
    # 创建新 Project
    echo "📋 创建新 Project..."
    PROJECT_NUMBER=$(gh project create --owner $OWNER --title "$PROJECT_TITLE" --format json | jq -r '.number')
    echo "✅ 创建 Project: #$PROJECT_NUMBER"
fi

echo ""

# 获取所有 Issues（排除已关闭的）
echo "📝 获取所有 Issues..."
ISSUE_NUMBERS=$(gh issue list --limit 100 --state open --json number --jq '.[].number')

if [ -z "$ISSUE_NUMBERS" ]; then
    echo "⚠️  没有找到 Issues"
    exit 0
fi

# 将 Issues 添加到 Project
echo "➕ 添加 Issues 到 Project..."
ADDED_COUNT=0
SKIPPED_COUNT=0

for issue_num in $ISSUE_NUMBERS; do
    # 检查 Issue 是否已在 Project 中
    ISSUE_URL="https://github.com/$REPO/issues/$issue_num"

    # 尝试添加 Issue 到 Project
    if gh project item-add $PROJECT_NUMBER --owner $OWNER --url "$ISSUE_URL" 2>/dev/null; then
        echo "  ✅ 添加 Issue #$issue_num"
        ((ADDED_COUNT++))
    else
        echo "  ⏭️  Issue #$issue_num 已在 Project 中或添加失败"
        ((SKIPPED_COUNT++))
    fi
done

echo ""
echo "🎉 完成！"
echo "  - 添加: $ADDED_COUNT 个 Issues"
echo "  - 跳过: $SKIPPED_COUNT 个 Issues"
echo ""
echo "🔗 查看 Project:"
echo "   gh project view $PROJECT_NUMBER --owner $OWNER --web"
echo ""
echo "或访问: https://github.com/users/$OWNER/projects/$PROJECT_NUMBER"
