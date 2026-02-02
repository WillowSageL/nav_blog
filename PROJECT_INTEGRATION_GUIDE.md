# gh-issue-create Skill 的 --project 参数使用指南

## ✅ 验证结果

经过检查，`/gh-issue-create` skill **已经支持** `--project` 参数，可以自动创建 GitHub Project 并关联 Issues！

### 检查项目
- ✅ `create_issues.sh` 脚本支持 `--project` 参数
- ✅ `create_project.sh` 脚本存在且功能完整
- ✅ GitHub CLI 已有 `project` 权限
- ✅ 所有依赖脚本都已更新

---

## 🚀 使用方法

### 方法 1: 使用 Skill 命令（推荐）

```bash
# 在项目目录中运行
/gh-issue-create docs/ui-ux-upgrade-cyberpunk-prd.md --project "nav_blog UI 升级"
```

这个命令会：
1. 解析 PRD 文档
2. 创建 Milestones
3. 创建 Labels
4. 创建 Issues
5. **创建 GitHub Project**
6. **将所有 Issues 添加到 Project**

### 方法 2: 直接使用脚本

如果您已经有 `parsed_issues.json` 文件：

```bash
bash ~/.claude/skills/gh-issue-create/scripts/create_issues.sh \
  parsed_issues.json \
  --project "nav_blog UI 升级"
```

---

## 📋 完整工作流程

### 步骤 1: 准备 PRD 文档
确保您的 PRD 文档包含：
- Phase 章节（会创建为 Milestones）
- User Stories 或功能需求（会创建为 Issues）
- 验收标准（会添加到 Issue body）

### 步骤 2: 运行 Skill
```bash
cd /Users/v_liangjiawei02/Desktop/导航页
/gh-issue-create docs/ui-ux-upgrade-cyberpunk-prd.md --project "nav_blog UI 升级"
```

### 步骤 3: 查看结果
脚本会输出：
- ✅ 创建的 Milestones 数量
- ✅ 创建的 Labels 列表
- ✅ 创建的 Issues 列表
- ✅ 创建的 Project 链接
- ✅ 添加到 Project 的 Issues 数量

---

## 🎯 Project 功能说明

### 自动创建的内容

**1. GitHub Project**
- 类型: Board（看板）
- 名称: 您指定的项目名称
- 位置: 用户级别的 Project

**2. Issues 关联**
- 所有创建的 Issues 会自动添加到 Project
- 默认添加到 "Todo" 列
- 可以手动拖拽到其他列（In Progress, Done 等）

### 手动配置（可选）

创建后，您可以在 Project 中：
1. **创建自定义列**
   - Backlog, Todo, In Progress, Review, Done

2. **设置分组**
   - 按 Milestone 分组（Phase 1 / Phase 2）
   - 按 Label 分组（priority-high, ui, animation 等）

3. **设置排序**
   - 按优先级排序
   - 按创建时间排序
   - 手动拖拽排序

---

## 🔧 故障排除

### 问题 1: "authentication token is missing required scopes"

**解决方案**:
```bash
gh auth refresh -h github.com -s project,read:project
```

然后在浏览器中完成授权。

### 问题 2: "Project already exists"

这是正常的！脚本会：
- 检测到已存在的 Project
- 使用现有 Project
- 将新 Issues 添加到该 Project

### 问题 3: "Failed to add issue to project"

可能原因：
- Issue 已经在 Project 中（会跳过）
- 权限不足（检查认证）

---

## 📊 示例输出

```bash
$ /gh-issue-create docs/ui-ux-upgrade-cyberpunk-prd.md --project "nav_blog UI 升级"

✅ Prerequisites check passed
📦 Repository: WillowSageL/nav_blog

📌 Creating Milestones...
✅ Created milestone: Phase 1: 视觉风格重构（MVP 核心） (#1)
✅ Created milestone: Phase 2: 交互增强与角色系统 (#2)

📌 Creating Labels...
✅ Created label: feature
✅ Created label: ui
✅ Created label: animation
...

📝 Creating Issues...
Creating issue 1/10: 实现赛博朋克配色系统
✅ Created: https://github.com/WillowSageL/nav_blog/issues/2
...

📋 Creating GitHub Project: nav_blog UI 升级
✅ Created project: nav_blog UI 升级 (Number: 1)
Project URL: https://github.com/users/WillowSageL/projects/1

➕ Adding issues to project...
Adding issue 1: https://github.com/WillowSageL/nav_blog/issues/2
✅ Added successfully
...

✅ Project setup complete!
Total issues processed: 10
Failed/Skipped: 0

View your project board:
https://github.com/users/WillowSageL/projects/1

Done! 🎉
```

---

## 🎨 Project 看板建议布局

创建 Project 后，建议设置以下布局：

```
┌─────────────────────────────────────────────────────────────┐
│  nav_blog UI 升级                                            │
├─────────────┬─────────────┬─────────────┬─────────────┬─────┤
│  📋 Backlog │  🚀 Todo    │  🔨 In Prog │  👀 Review  │ ✅ Done│
├─────────────┼─────────────┼─────────────┼─────────────┼─────┤
│             │ Phase 1     │             │             │     │
│             │ ─────────── │             │             │     │
│             │ #2 配色系统  │             │             │     │
│             │ #3 粒子背景  │             │             │     │
│             │ #4 卡片设计  │             │             │     │
│             │             │             │             │     │
│             │ Phase 2     │             │             │     │
│             │ ─────────── │             │             │     │
│             │ #7 图标插画  │             │             │     │
│             │ #8 看板娘    │             │             │     │
└─────────────┴─────────────┴─────────────┴─────────────┴─────┘
```

**设置步骤**:
1. 在 Project 中点击 **+ New column**
2. 创建: Backlog, In Progress, Review, Done
3. 点击 **View options** → **Group by** → **Milestone**
4. 拖拽 Issues 到相应的列

---

## 📚 相关文档

- Skill 文档: `~/.claude/skills/gh-issue-create/skill.md`
- 脚本位置: `~/.claude/skills/gh-issue-create/scripts/`
- 更新日志: `~/.claude/skills/gh-issue-create/CHANGELOG.md`

---

## ✨ 总结

**是的，skill 已经完全支持 `--project` 参数！**

只需在使用 `/gh-issue-create` 时添加 `--project "项目名称"` 参数，就会自动：
- ✅ 创建 GitHub Project
- ✅ 将所有 Issues 添加到 Project
- ✅ 提供 Project 链接

无需手动操作，一键完成！🎉
