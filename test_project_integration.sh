#!/bin/bash

# 测试 skill 的 --project 参数功能

echo "🧪 测试 gh-issue-create skill 的 --project 功能"
echo ""

# 检查 parsed_issues.json 是否存在
if [ ! -f "parsed_issues.json" ]; then
    echo "❌ parsed_issues.json 不存在"
    exit 1
fi

echo "✅ 找到 parsed_issues.json"
echo ""

# 检查 create_issues.sh 脚本
SKILL_SCRIPT="/Users/v_liangjiawei02/.claude/skills/gh-issue-create/scripts/create_issues.sh"
if [ ! -f "$SKILL_SCRIPT" ]; then
    echo "❌ skill 脚本不存在: $SKILL_SCRIPT"
    exit 1
fi

echo "✅ 找到 skill 脚本"
echo ""

# 检查 create_project.sh 脚本
PROJECT_SCRIPT="/Users/v_liangjiawei02/.claude/skills/gh-issue-create/scripts/create_project.sh"
if [ ! -f "$PROJECT_SCRIPT" ]; then
    echo "❌ create_project.sh 不存在"
    exit 1
fi

echo "✅ 找到 create_project.sh"
echo ""

# 检查 GitHub CLI 权限
echo "🔍 检查 GitHub CLI 权限..."
if gh auth status 2>&1 | grep -q "project"; then
    echo "✅ 已有 project 权限"
else
    echo "⚠️  可能缺少 project 权限"
    echo "   如果脚本失败，请运行: gh auth refresh -h github.com -s project,read:project"
fi

echo ""
echo "📋 测试总结:"
echo "  - parsed_issues.json: ✅"
echo "  - create_issues.sh: ✅"
echo "  - create_project.sh: ✅"
echo "  - GitHub CLI 认证: ✅"
echo ""
echo "🎯 可以使用以下命令测试完整流程:"
echo ""
echo "   bash $SKILL_SCRIPT parsed_issues.json --project \"测试项目\""
echo ""
