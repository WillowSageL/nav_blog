# GitHub Issues 创建指南

## 步骤 1: GitHub CLI 认证

### 方法 A: 使用 Personal Access Token（推荐）

1. **创建 GitHub Token**
   - 访问: https://github.com/settings/tokens/new
   - Token 名称: `gh-cli-nav-blog`
   - 过期时间: 选择合适的时间（如 90 天）
   - 勾选以下权限:
     - ✅ `repo` (完整仓库访问权限)
     - ✅ `workflow` (工作流权限)
     - ✅ `admin:org` (组织管理权限，如果需要)
   - 点击 "Generate token"
   - **复制生成的 token**（只显示一次！）

2. **使用 Token 登录**
   ```bash
   # 在终端运行
   echo "YOUR_TOKEN_HERE" | gh auth login --with-token
   ```

3. **验证认证**
   ```bash
   gh auth status
   ```

### 方法 B: 使用浏览器认证

```bash
# 运行此命令并按照提示操作
gh auth login

# 选择:
# ? What account do you want to log into? GitHub.com
# ? What is your preferred protocol for Git operations? HTTPS
# ? Authenticate Git with your GitHub credentials? Yes
# ? How would you like to authenticate GitHub CLI? Login with a web browser

# 复制显示的一次性代码，然后在浏览器中打开链接并输入代码
```

---

## 步骤 2: 运行 Issues 创建脚本

认证成功后，运行以下命令创建所有 Issues:

```bash
cd /Users/v_liangjiawei02/Desktop/导航页
./create_github_issues.sh
```

脚本将自动创建:
- ✅ 2 个 Milestones (Phase 1 和 Phase 2)
- ✅ 9 个 Issues (包含详细的验收标准和技术要点)
- ✅ 1 个 Epic Issue (总览)

---

## 步骤 3: 创建 GitHub Project（可选）

如果您想使用 GitHub Project 看板来可视化管理任务:

```bash
# 创建项目
gh project create --owner @me --title "nav_blog UI 升级"

# 获取项目编号（从上一步输出中）
PROJECT_NUMBER=<项目编号>

# 将所有 Issues 添加到项目
gh issue list --json number,url --jq '.[] | .url' | while read url; do
  gh project item-add $PROJECT_NUMBER --owner @me --url "$url"
done
```

---

## 步骤 4: 验证创建结果

### 查看 Milestones
```bash
gh milestone list
```

### 查看 Phase 1 Issues
```bash
gh issue list --milestone "Phase 1: 视觉风格重构（MVP 核心）"
```

### 查看 Phase 2 Issues
```bash
gh issue list --milestone "Phase 2: 交互增强与角色系统"
```

### 在浏览器中查看
```bash
gh repo view --web
```

---

## 创建的 Issues 概览

### Phase 1: 视觉风格重构（MVP 核心）

| # | Issue 标题 | 标签 | 优先级 |
|---|-----------|------|--------|
| 1 | 实现赛博朋克配色系统 | feature, ui, phase-1 | 高 |
| 2 | 实现动态粒子星空背景 | feature, ui, animation, phase-1 | 高 |
| 3 | 书签卡片赛博朋克风格重设计 | feature, ui, phase-1 | 高 |
| 4 | 实现 3D 卡片悬浮和倾斜效果 | feature, ui, animation, phase-1 | 中 |
| 5 | 实现页面和组件过渡动画 | feature, ui, animation, phase-1 | 中 |

### Phase 2: 交互增强与角色系统

| # | Issue 标题 | 标签 | 优先级 |
|---|-----------|------|--------|
| 6 | 设计和实现动漫风格图标和插画 | feature, ui, design, phase-2 | 中 |
| 7 | 实现看板娘角色助手（基础版） | feature, ui, animation, phase-2 | 高 |
| 8 | 看板娘高级功能（Live2D 动画） | feature, ui, animation, phase-2 | 低 |
| 9 | 添加更多赛博朋克装饰元素 | feature, ui, animation, phase-2 | 低 |

### Epic Issue

| # | Issue 标题 | 说明 |
|---|-----------|------|
| 10 | 🎨 赛博朋克风格 UI/UX 全面升级 | 总览 Issue，包含所有子任务链接 |

---

## 故障排除

### 问题: `gh auth login` 网络连接失败

**解决方案**: 使用 Personal Access Token 方式（方法 A）

### 问题: 脚本运行时提示 "Milestone already exists"

**解决方案**: 这是正常的，脚本会跳过已存在的 Milestone 并继续创建 Issues

### 问题: 某些 Issues 创建失败

**解决方案**:
1. 检查错误信息
2. 手动创建失败的 Issue
3. 或重新运行脚本（已存在的 Issues 不会重复创建）

---

## 下一步

创建完成后，您可以:

1. **开始开发**: 从 Phase 1 的高优先级 Issues 开始
2. **设置项目看板**: 使用 GitHub Project 可视化管理进度
3. **分配任务**: 如果是团队协作，可以分配 Issues 给不同成员
4. **追踪进度**: 完成后关闭 Issues，自动更新 Milestone 进度

---

## 相关文档

- 📄 PRD: `docs/ui-ux-upgrade-cyberpunk-prd.md`
- 🔧 创建脚本: `create_github_issues.sh`
- 📊 解析结果: `parsed_issues.json`

---

**祝开发顺利！🚀**
