#!/usr/bin/env python3
"""
Complete GitHub Issues Generator for UI/UX Cyberpunk Upgrade Project
Generates all Epics, Tasks, Milestones, and Labels from PRD

Usage:
    python create_all_issues.py
"""

import subprocess
import json
import time
import sys
import os
from typing import Dict, List, Optional, Tuple

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_info(text: str):
    print(f"{Colors.CYAN}→ {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def run_gh_command(args: List[str], retry: int = 3) -> Optional[str]:
    """Execute gh CLI command with retry logic"""
    env = dict(os.environ)
    env['GH_PROMPT_DISABLED'] = '1'
    env['GH_NO_UPDATE_NOTIFIER'] = '1'

    for attempt in range(retry):
        try:
            result = subprocess.run(
                ['gh'] + args,
                capture_output=True,
                text=True,
                check=True,
                env=env,
                timeout=30
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            print_error(f"Command timed out: {' '.join(args)}")
            return None
        except subprocess.CalledProcessError as e:
            if attempt < retry - 1:
                time.sleep(2)
                continue
            print_error(f"Command failed: {' '.join(args)}")
            print_error(f"Error: {e.stderr}")
            return None
    return None

def find_issue_by_title(title: str) -> Optional[int]:
    """Find existing issue by exact title and return issue number if found"""
    search_query = f'"{title}" in:title'
    result = run_gh_command([
        'issue', 'list',
        '--search', search_query,
        '--state', 'all',
        '--json', 'number,title',
        '--limit', '100'
    ])

    if not result:
        return None

    try:
        issues = json.loads(result)
    except json.JSONDecodeError:
        return None

    for issue in issues:
        if issue.get('title', '').strip() == title.strip():
            return int(issue['number'])

    return None

def create_labels():
    """Create all necessary labels"""
    print_header("Step 1: Creating Labels")

    labels = [
        # Type labels
        ("epic", "7057ff", "Epic issue containing multiple tasks"),
        ("feature", "a2eeef", "New feature or request"),
        ("enhancement", "84b6eb", "Enhancement to existing feature"),
        ("testing", "d4c5f9", "Testing related tasks"),
        ("documentation", "0075ca", "Documentation improvements"),
        # Phase labels
        ("phase-1", "fbca04", "Phase 1: Visual Style Refactoring"),
        ("phase-2", "d93f0b", "Phase 2: Interaction Enhancement"),
        # Domain labels
        ("ui", "e99695", "UI/Frontend related"),
        ("backend", "c2e0c6", "Backend related"),
        ("animation", "f9d0c4", "Animation and effects"),
        ("design", "fef2c0", "Design assets and styling"),
        ("performance", "bfd4f2", "Performance optimization"),
        # Priority labels
        ("priority-p0", "b60205", "Critical priority"),
        ("priority-p1", "d93f0b", "High priority"),
        ("priority-p2", "fbca04", "Medium priority"),
        ("priority-p3", "0e8a16", "Low priority"),
        # Size labels
        ("size-small", "c5def5", "1-2 hours"),
        ("size-medium", "bfdadc", "2-3 hours"),
        ("size-large", "d4c5f9", "3-4 hours"),
    ]

    for name, color, description in labels:
        result = run_gh_command([
            'label', 'create', name,
            '--color', color,
            '--description', description,
            '--force'
        ])
        if result is not None:
            print_success(f"Label: {name}")

def create_milestones() -> Tuple[str, str]:
    """Create project milestones and return their titles"""
    print_header("Step 2: Creating Milestones")

    milestones = [
        {
            "title": "Phase 1: Visual Style Refactoring",
            "description": "Establish cyberpunk visual foundation with core visual upgrades. Includes Epic 1 (Cyberpunk Visual Style), Epic 2 (Particle Background), Epic 3 (3D Card Effects).",
        },
        {
            "title": "Phase 2: Interaction Enhancement & Character System",
            "description": "Add anime elements and interactive features. Includes Epic 4 (Anime Icons), Epic 5 (Kanban Musume Character).",
        }
    ]

    milestone_titles = []

    for milestone in milestones:
        result = run_gh_command([
            'api', 'repos/{owner}/{repo}/milestones',
            '-f', f'title={milestone["title"]}',
            '-f', f'description={milestone["description"]}',
            '-f', 'state=open'
        ])

        if result:
            try:
                data = json.loads(result)
                milestone_num = str(data['number'])
                milestone_titles.append(milestone["title"])
                print_success(f"Milestone: {milestone['title']} (#{milestone_num})")
            except (json.JSONDecodeError, KeyError):
                milestone_titles.append(milestone["title"])
                print_info(f"Milestone may already exist: {milestone['title']}")

    return tuple(milestone_titles) if len(milestone_titles) == 2 else (milestones[0]["title"], milestones[1]["title"])

def create_epic_issue(title: str, body: str, labels: List[str], milestone: str) -> Optional[int]:
    """Create an Epic issue and return its number"""
    existing_issue = find_issue_by_title(title)
    if existing_issue:
        print_info(f"Epic exists: {title} (#{existing_issue})")
        return existing_issue

    result = run_gh_command([
        'issue', 'create',
        '--title', title,
        '--body', body,
        '--label', ','.join(labels),
        '--milestone', milestone
    ])

    if result:
        issue_number = int(result.split('/')[-1])
        print_success(f"Epic: {title} (#{issue_number})")
        return issue_number
    return None

def create_task_issue(title: str, body: str, labels: List[str], milestone: str) -> Optional[int]:
    """Create a Task issue and return its number"""
    existing_issue = find_issue_by_title(title)
    if existing_issue:
        print_info(f"  Task exists: {title} (#{existing_issue})")
        return existing_issue

    result = run_gh_command([
        'issue', 'create',
        '--title', title,
        '--body', body,
        '--label', ','.join(labels),
        '--milestone', milestone
    ])

    if result:
        issue_number = int(result.split('/')[-1])
        print_success(f"  Task: {title} (#{issue_number})")
        return issue_number
    return None

def generate_epic1_body() -> str:
    """Generate Epic 1 body content"""
    return """## Epic Overview

实现完整的赛博朋克配色方案，包括深色基调、霓虹色强调、渐变效果和发光元素。

## User Story

**作为** 二次元爱好者
**我想要** 看到深蓝、紫色、霓虹色调的赛博朋克配色方案
**以便** 界面能反映我的审美偏好，而不是千篇一律的商务风格

## Acceptance Criteria

- [ ] 主色调采用深蓝（#0a0e27）、紫色（#6366f1）、霓虹粉（#ec4899）、霓虹青（#06b6d4）
- [ ] 背景使用深色基调，避免刺眼的亮色
- [ ] 文字和图标使用高对比度的霓虹色，确保可读性
- [ ] 支持暗色模式（默认）和亮色模式切换
- [ ] 移动端保持相同的配色方案

## Tasks Breakdown

This epic contains 10 tasks (24 hours total):

1. Setup Tailwind CSS cyberpunk color palette (2h)
2. Create dark theme base styles (2h)
3. Implement neon color scheme for text/icons (2h)
4. Add glow effects to interactive elements (3h)
5. Create light mode variant (3h)
6. Update all existing components (4h)
7. Add theme toggle functionality (2h)
8. Implement responsive color adjustments (2h)
9. Add high contrast mode for accessibility (3h)
10. Create color system documentation (1h)

## Success Metrics

- All pages use new cyberpunk color scheme
- Theme toggle works smoothly
- Accessibility contrast ratios meet WCAG AA standards
- Mobile and desktop have consistent styling

## Dependencies

None - This is a foundational epic

---
*This is an Epic issue. Individual tasks will be created as separate issues and linked to this epic.*"""

def generate_epic2_body() -> str:
    """Generate Epic 2 body content"""
    return """## Epic Overview

实现动态粒子星空背景，包含性能监控、设备降级与移动端策略，确保沉浸感与流畅度兼顾。

## User Story

**作为** 用户
**我想要** 看到动态的粒子星空背景效果
**以便** 界面更有科幻感和沉浸感

## Acceptance Criteria

- [ ] 背景包含缓慢移动的粒子效果（模拟星空）
- [ ] 粒子具有渐变透明度与轻微发光
- [ ] 鼠标/触控存在轻量交互（可配置关闭）
- [ ] 移动端可自动降级为静态渐变或低粒子配置
- [ ] 动画帧率保持在 30fps 以上

## Tasks Breakdown

This epic contains 10 tasks (23 hours total):

1. Create Canvas-based particle system component (3h)
2. Implement particle movement algorithm (2h)
3. Add gradient transparency and glow effects (2h)
4. Implement mouse interaction with particles (3h)
5. Add performance monitoring and FPS counter (2h)
6. Implement device detection and auto-degradation (3h)
7. Create static gradient fallback (2h)
8. Add user preference toggle (2h)
9. Optimize particle count based on screen size (2h)
10. Add mobile-specific particle configuration (2h)

## Success Metrics

- Particle background renders without blocking interactions
- FPS ≥ 30 on mainstream devices
- Mobile devices auto-apply simplified configuration

## Dependencies

None - This epic can be developed in parallel

---
*This is an Epic issue. Individual tasks will be created as separate issues and linked to this epic.*"""

def generate_epic3_body() -> str:
    """Generate Epic 3 body content"""
    return """## Epic Overview

为书签卡片提供 3D 悬浮、倾斜与交互动效，提升立体感与可玩性，并兼顾移动端体验。

## User Story

**作为** 用户
**我想要** 书签卡片具有 3D 悬浮和倾斜效果
**以便** 交互更有趣，视觉更立体

## Acceptance Criteria

- [ ] 鼠标悬停时卡片有 3D 倾斜与悬浮阴影
- [ ] 过渡动画平滑，使用统一的动画框架
- [ ] 点击反馈清晰（缩放或高亮）
- [ ] 移动端简化动画，避免重负载
- [ ] 文字与图标在动画下仍清晰可读

## Tasks Breakdown

This epic contains 10 tasks (21 hours total):

1. Install and configure Framer Motion (1h)
2. Create 3D tilt effect component (3h)
3. Implement hover shadow and glow border (2h)
4. Add smooth transition animations (2h)
5. Implement click feedback with scale animation (2h)
6. Create mobile-friendly simplified animations (3h)
7. Add card content readability optimization (2h)
8. Implement animation performance optimization (3h)
9. Add accessibility support for reduced motion (2h)
10. Create card animation documentation (1h)

## Success Metrics

- Hover/tilt effect feels natural without jitter
- Mobile animation stays under performance budget
- Reduced-motion users can opt out

## Dependencies

None - This epic can be developed independently

---
*This is an Epic issue. Individual tasks will be created as separate issues and linked to this epic.*"""

def generate_epic4_body() -> str:
    """Generate Epic 4 body content"""
    return """## Epic Overview

引入手绘风格的图标与插画，建立二次元视觉语言，并形成可复用的图标系统与样式规范。

## User Story

**作为** 用户
**我想要** 看到手绘风格的图标和装饰性插画元素
**以便** 界面更有二次元氛围

## Acceptance Criteria

- [ ] 核心分类图标具备统一的手绘风格
- [ ] 空状态与加载状态拥有插画支持
- [ ] 图标组件化可复用，并具备悬停动效
- [ ] SVG 体积可控，加载性能可接受
- [ ] 插画尺寸在不同屏幕上保持比例一致

## Tasks Breakdown

This epic contains 10 tasks (23 hours total):

1. Design hand-drawn style category icons (4h)
2. Create decorative geometric elements (3h)
3. Design empty state illustrations (3h)
4. Implement icon component system (2h)
5. Add decorative line art elements (2h)
6. Create loading state illustrations (2h)
7. Implement icon animation on hover (2h)
8. Optimize SVG files for performance (2h)
9. Add responsive scaling for illustrations (2h)
10. Create illustration style guide (1h)

## Success Metrics

- Icons/illustrations appear consistent across pages
- SVG sizes are optimized and load quickly
- Style guide can onboard new contributors

## Dependencies

None - Can proceed after Phase 1 or in parallel

---
*This is an Epic issue. Individual tasks will be created as separate issues and linked to this epic.*"""

def generate_epic5_body() -> str:
    """Generate Epic 5 body content"""
    return """## Epic Overview

构建可交互的看板娘角色助手，具备对话、快捷操作、状态变化与移动端适配。

## User Story

**作为** 用户
**我想要** 一个可交互的看板娘角色
**以便** 界面更有趣，并能快速访问常用功能

## Acceptance Criteria

- [ ] 看板娘固定在页面角落，可与用户交互
- [ ] 点击或悬停触发对话与状态变化
- [ ] 提供快捷入口，提升常用操作效率
- [ ] 移动端布局友好，可收起或缩小
- [ ] 动画与状态切换顺畅

## Tasks Breakdown

This epic contains 10 tasks (27 hours total):

1. Design or source kanban musume character assets (4h)
2. Create kanban musume component with fixed positioning (2h)
3. Implement click interaction and dialog system (3h)
4. Add dynamic expressions and state changes (3h)
5. Create quick action menu (3h)
6. Implement time-based greeting messages (2h)
7. Add minimize/hide functionality (2h)
8. Create mobile-responsive layout (3h)
9. Implement drag-and-drop position adjustment (3h)
10. Add entrance/exit animations (2h)

## Success Metrics

- Character interactions feel responsive and non-intrusive
- Quick actions reduce clicks for common tasks
- Mobile layout remains usable without occlusion

## Dependencies

None - Can proceed after Phase 2 starts

---
*This is an Epic issue. Individual tasks will be created as separate issues and linked to this epic.*"""

def generate_task_body(task_num: int, epic_num: int, epic_title: str, task_data: Dict) -> str:
    """Generate task issue body"""
    return f"""## Background

{task_data['background']}

## Acceptance Criteria

{task_data['acceptance_criteria']}

## Implementation Plan

**Files to Modify:**
{task_data['files']}

**Implementation Steps:**
{task_data['steps']}

**Estimated Time:** {task_data['time']}

## Core Logic

```typescript
{task_data.get('code', '// Implementation details')}
```

## Testing Requirements

{task_data['testing']}

## Dependencies

- **Priority:** {task_data['priority']}
- **Size:** {task_data['size']}
- **Blocked by:** {task_data.get('blocked_by', 'None')}
- **Blocks:** {task_data.get('blocks', 'None')}

## Git Worktree

```bash
# Create worktree for this task
git worktree add ../nav_blog-{task_data['branch']} -b {task_data['branch']}
cd ../nav_blog-{task_data['branch']}

# After completion
git add .
git commit -m "{task_data['commit']}"
git push -u origin {task_data['branch']}

# Create PR
gh pr create --title "{task_data['title']}" --body "Closes #{epic_num}"
```

## Related

- Epic: #{epic_num} {epic_title}
"""

def create_epic1_tasks(epic_num: int, milestone: str):
    """Create all tasks for Epic 1"""
    print_info("Creating tasks for Epic 1...")

    tasks = [
        {
            'title': '[Epic 1-Task 1] Setup Tailwind CSS cyberpunk color palette',
            'background': '需要在 Tailwind 配置中定义赛博朋克风格的颜色系统，包括深蓝、紫色、霓虹粉、霓虹青等主题色。',
            'acceptance_criteria': '''- [ ] 在 tailwind.config.js 中添加自定义颜色
- [ ] 定义 CSS 变量用于动态主题切换
- [ ] 颜色命名清晰且语义化
- [ ] 包含所有必需的色调变体（50-950）''',
            'files': '- `tailwind.config.js`\n- `src/app/globals.css`',
            'steps': '''1. 在 tailwind.config.js 的 theme.extend.colors 中添加颜色定义
2. 在 globals.css 中定义 CSS 变量
3. 测试颜色在不同组件中的显示效果''',
            'time': '2 hours',
            'code': '''// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        cyber: {
          dark: '#0a0e27',
          purple: '#6366f1',
          pink: '#ec4899',
          cyan: '#06b6d4'
        }
      }
    }
  }
}''',
            'testing': '- 验证所有颜色在浏览器中正确显示\n- 检查颜色对比度是否符合可访问性标准',
            'priority': 'P0',
            'size': 'size-small',
            'branch': 'feat/epic1-task1-tailwind-colors',
            'commit': 'feat: Add cyberpunk color palette to Tailwind config',
            'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p0', 'size-small']
        },
        {
            'title': '[Epic 1-Task 2] Create dark theme base styles',
            'background': '创建深色主题的基础样式，包括深蓝色背景和基础布局样式。',
            'acceptance_criteria': '''- [ ] 页面背景使用深蓝色（#0a0e27）
- [ ] 文字颜色具有足够的对比度
- [ ] 所有基础组件应用深色主题
- [ ] 避免刺眼的亮色''',
            'files': '- `src/app/globals.css`\n- `src/app/layout.tsx`',
            'steps': '''1. 在 globals.css 中定义 dark theme 基础样式
2. 更新 body 背景色
3. 设置默认文字颜色和链接颜色''',
            'time': '2 hours',
            'code': '''/* globals.css */
:root {
  --bg-primary: #0a0e27;
  --text-primary: #e2e8f0;
}

body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
}''',
            'testing': '- 检查所有页面的背景色和文字色\n- 验证可读性',
            'priority': 'P0',
            'size': 'size-small',
            'blocked_by': 'Task 1',
            'branch': 'feat/epic1-task2-dark-theme-base',
            'commit': 'feat: Implement dark theme base styles',
            'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p0', 'size-small']
        },
        {
            'title': '[Epic 1-Task 3] Implement neon color scheme for text and icons',
            'background': '为文本、图标与强调信息加入霓虹色方案，统一视觉语言并提升识别度。',
            'acceptance_criteria': '''- [ ] 文本与图标使用霓虹色调
- [ ] 重点信息具备明确的强调色
- [ ] 保持可读性与对比度
- [ ] 组件样式可复用''',
            'files': '- `src/app/globals.css`\n- `src/components/ui/*.tsx`',
            'steps': '''1. 在 globals.css 中定义霓虹文本与图标的基础类
2. 替换关键组件的文字与图标色值
3. 校验在不同背景下的对比度与可读性''',
            'time': '2 hours',
            'code': '''.text-neon-pink {
  color: var(--cyber-pink);
  text-shadow: 0 0 8px rgba(236, 72, 153, 0.6);
}

.icon-neon-cyan {
  color: var(--cyber-cyan);
}''',
            'testing': '- 目视检查重要页面文本与图标的对比度\n- 验证色彩在暗/亮主题中的一致性',
            'priority': 'P0',
            'size': 'size-small',
            'blocked_by': 'Task 1',
            'branch': 'feat/epic1-task3-neon-colors',
            'commit': 'feat: Apply neon color scheme for text and icons',
            'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p0', 'size-small']
        },
        {
            'title': '[Epic 1-Task 4] Add glow effects to interactive elements',
            'background': '为按钮、输入框等交互组件增加发光效果，强化赛博朋克氛围。',
            'acceptance_criteria': '''- [ ] Hover/Focus 状态具备柔和发光
- [ ] 发光效果可配置且不影响可读性
- [ ] 不影响主要交互性能''',
            'files': '- `src/components/ui/button.tsx`\n- `src/app/globals.css`',
            'steps': '''1. 在 globals.css 中定义通用 glow 样式
2. 为 Button/Inputs 等交互组件添加发光样式
3. 验证交互状态下的视觉一致性''',
            'time': '3 hours',
            'code': '''.glow-hover:hover {
  box-shadow: 0 0 12px rgba(6, 182, 212, 0.5);
}

.glow-focus:focus-visible {
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.5);
}''',
            'testing': '- 检查 hover/focus 时发光效果是否稳定\n- 确认不会遮挡文字或影响可读性',
            'priority': 'P1',
            'size': 'size-medium',
            'blocked_by': 'Task 1',
            'branch': 'feat/epic1-task4-glow-effects',
            'commit': 'feat: Add glow effects to interactive elements',
            'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p1', 'size-medium']
        },
        {
            'title': '[Epic 1-Task 5] Create light mode variant',
            'background': '提供亮色主题方案，满足不同用户偏好并保持一致的赛博朋克调性。',
            'acceptance_criteria': '''- [ ] 亮色主题有可用的主色与背景
- [ ] 亮色模式下仍保持霓虹对比度
- [ ] 主题切换后样式无明显闪烁''',
            'files': '- `src/app/globals.css`\n- `tailwind.config.js`',
            'steps': '''1. 定义 light theme 的 CSS 变量
2. 补充 Tailwind 主题扩展
3. 验证亮色模式下组件显示''',
            'time': '3 hours',
            'code': ''':root[data-theme='light'] {
  --bg-primary: #f8fafc;
  --text-primary: #0f172a;
  --accent-neon: #6366f1;
}''',
            'testing': '- 切换主题后检查背景与文字颜色\n- 检查亮色模式下的可读性',
            'priority': 'P1',
            'size': 'size-medium',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic1-task5-light-mode',
            'commit': 'feat: Add light theme variant',
            'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p1', 'size-medium']
        },
        {
            'title': '[Epic 1-Task 6] Update all existing components',
            'background': '将现有组件全部接入新的赛博朋克配色与主题变量，避免风格断层。',
            'acceptance_criteria': '''- [ ] 所有组件使用新颜色变量
- [ ] 旧色值全部替换或移除
- [ ] 页面风格保持一致''',
            'files': '- `src/components/**/*.tsx`\n- `src/app/**/*.tsx`',
            'steps': '''1. 盘点现有组件中使用的颜色
2. 替换为新的主题变量或 Tailwind 颜色
3. 逐页检查视觉一致性''',
            'time': '4 hours',
            'code': '''const buttonClass = 'bg-cyber-purple text-cyber-cyan glow-hover'
// Replace legacy color tokens with new cyber tokens''',
            'testing': '- 全站巡检组件样式一致性\n- 验证关键页面无样式断裂',
            'priority': 'P0',
            'size': 'size-large',
            'blocked_by': 'Tasks 1, 2, 3',
            'branch': 'feat/epic1-task6-update-components',
            'commit': 'feat: Update all components to cyberpunk theme',
            'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p0', 'size-large']
        },
        {
            'title': '[Epic 1-Task 7] Add theme toggle functionality',
            'background': '提供主题切换功能，允许用户在暗色与亮色模式间切换。',
            'acceptance_criteria': '''- [ ] UI 上提供主题切换入口
- [ ] 主题切换持久化
- [ ] 切换后页面无明显闪烁''',
            'files': '- `src/components/ThemeToggle.tsx`\n- `src/app/layout.tsx`',
            'steps': '''1. 实现 ThemeToggle 组件
2. 在 layout 中引入并持久化主题偏好
3. 验证刷新后主题保持''',
            'time': '2 hours',
            'code': '''const toggleTheme = () => {
  const next = theme === 'dark' ? 'light' : 'dark'
  document.documentElement.dataset.theme = next
  localStorage.setItem('theme', next)
}''',
            'testing': '- 切换主题时检查样式变化\n- 刷新后验证主题持久化',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 5',
            'branch': 'feat/epic1-task7-theme-toggle',
            'commit': 'feat: Add theme toggle functionality',
            'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 1-Task 8] Implement responsive color adjustments',
            'background': '针对不同屏幕与亮度环境调整颜色显示，确保移动端视觉一致。',
            'acceptance_criteria': '''- [ ] 小屏设备使用更高对比度颜色
- [ ] 文字与背景在移动端仍清晰可读
- [ ] 不影响桌面端样式''',
            'files': '- `src/app/globals.css`\n- `tailwind.config.js`',
            'steps': '''1. 定义响应式颜色变量或 Tailwind 断点覆盖
2. 在移动端提高对比度与字号
3. 验证不同尺寸设备显示''',
            'time': '2 hours',
            'code': '''@media (max-width: 640px) {
  :root {
    --text-primary: #f1f5f9;
  }
}''',
            'testing': '- 在移动设备模拟器上检查对比度\n- 验证桌面端无回归',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 6',
            'branch': 'feat/epic1-task8-responsive-colors',
            'commit': 'feat: Add responsive color adjustments',
            'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 1-Task 9] Add high contrast mode for accessibility',
            'background': '提供高对比度模式以提升可访问性，满足 WCAG AA 的可读性要求。',
            'acceptance_criteria': '''- [ ] 高对比度模式可开启/关闭
- [ ] 对比度符合 WCAG AA 标准
- [ ] 不破坏现有组件布局''',
            'files': '- `src/app/globals.css`\n- `src/components/Settings.tsx`',
            'steps': '''1. 新增 high-contrast 主题变量
2. 在设置中加入切换入口
3. 验证组件样式可读性''',
            'time': '3 hours',
            'code': '''[data-contrast='high'] {
  --text-primary: #ffffff;
  --bg-primary: #000000;
  --accent-neon: #00ffff;
}''',
            'testing': '- 目视检查高对比度模式\n- 使用对比度检测工具验证',
            'priority': 'P2',
            'size': 'size-medium',
            'blocked_by': 'Task 6',
            'branch': 'feat/epic1-task9-high-contrast',
            'commit': 'feat: Add high contrast mode for accessibility',
            'labels': ['enhancement', 'phase-1', 'ui', 'design', 'priority-p2', 'size-medium']
        },
        {
            'title': '[Epic 1-Task 10] Create color system documentation',
            'background': '整理颜色系统的使用规范与示例，方便团队后续迭代与统一。',
            'acceptance_criteria': '''- [ ] 文档包含颜色命名与用途说明
- [ ] 示例涵盖按钮、文本、背景
- [ ] 文档可作为新成员参考''',
            'files': '- `docs/color-system.md`',
            'steps': '''1. 总结颜色变量与命名规范
2. 输出常见组件的颜色使用示例
3. 添加注意事项与可访问性提示''',
            'time': '1 hour',
            'code': '''# Color System
- cyber-dark: Primary background
- cyber-purple: Primary accent
- cyber-pink: Highlight
- cyber-cyan: Secondary accent''',
            'testing': '- 检查文档格式与示例是否清晰',
            'priority': 'P3',
            'size': 'size-small',
            'blocked_by': 'Task 6',
            'branch': 'docs/epic1-task10-color-docs',
            'commit': 'docs: Add cyberpunk color system documentation',
            'labels': ['documentation', 'phase-1', 'design', 'priority-p3', 'size-small']
        }
    ]

    epic_title = '[Epic 1] 赛博朋克视觉风格 (Cyberpunk Visual Style)'

    for index, task in enumerate(tasks, start=1):
        body = generate_task_body(index, epic_num, epic_title, task)
        create_task_issue(task['title'], body, task['labels'], milestone)
        time.sleep(1)

def create_epic2_tasks(epic_num: int, milestone: str):
    """Create all tasks for Epic 2"""
    print_info("Creating tasks for Epic 2...")

    tasks = [
        {
            'title': '[Epic 2-Task 1] Create Canvas-based particle system component',
            'background': '建立基于 Canvas 的粒子背景组件，提供完整的渲染生命周期与自适应布局。',
            'acceptance_criteria': '''- [ ] 组件支持全屏/容器渲染
- [ ] 使用 requestAnimationFrame 驱动动画
- [ ] 自动监听窗口尺寸变化
- [ ] 支持开启/关闭渲染''',
            'files': '- `src/components/ParticleBackground.tsx`',
            'steps': '''1. 创建 Canvas 与容器布局
2. 实现渲染循环与清屏逻辑
3. 监听 resize 并更新 canvas 大小''',
            'time': '3 hours',
            'code': '''const canvas = canvasRef.current
const ctx = canvas.getContext('2d')
const render = () => {
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  drawParticles(ctx)
  requestAnimationFrame(render)
}''',
            'testing': '- 在不同分辨率下验证渲染尺寸\n- 检查动画是否持续运行',
            'priority': 'P0',
            'size': 'size-medium',
            'branch': 'feat/epic2-task1-particle-component',
            'commit': 'feat: Add canvas particle background component',
            'labels': ['feature', 'phase-1', 'ui', 'animation', 'priority-p0', 'size-medium']
        },
        {
            'title': '[Epic 2-Task 2] Implement particle movement algorithm',
            'background': '为粒子添加基础移动算法（速度、方向、边界回绕），形成稳定的星空动态。',
            'acceptance_criteria': '''- [ ] 粒子具有速度与方向
- [ ] 离开边界后可回绕或重置
- [ ] 动画稳定无明显跳帧''',
            'files': '- `src/components/ParticleBackground.tsx`',
            'steps': '''1. 定义粒子数据结构（位置、速度、半径）
2. 在每一帧更新位置
3. 超出边界时回绕或重置''',
            'time': '2 hours',
            'code': '''particles.forEach(p => {
  p.x += p.vx
  p.y += p.vy
  if (p.x > width) p.x = 0
  if (p.y > height) p.y = 0
})''',
            'testing': '- 观察粒子运动是否连续\n- 确认粒子不会永久消失',
            'priority': 'P0',
            'size': 'size-small',
            'blocked_by': 'Task 1',
            'branch': 'feat/epic2-task2-particle-movement',
            'commit': 'feat: Implement particle movement algorithm',
            'labels': ['feature', 'phase-1', 'ui', 'animation', 'priority-p0', 'size-small']
        },
        {
            'title': '[Epic 2-Task 3] Add gradient transparency and glow effects',
            'background': '为粒子添加渐变透明与微弱发光效果，提升视觉层次。',
            'acceptance_criteria': '''- [ ] 粒子具有径向渐变
- [ ] 发光效果可调节强度
- [ ] 不明显影响帧率''',
            'files': '- `src/components/ParticleBackground.tsx`',
            'steps': '''1. 使用 radial gradient 绘制粒子
2. 添加 glow 颜色与阴影
3. 验证视觉效果与性能''',
            'time': '2 hours',
            'code': '''const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius)
gradient.addColorStop(0, 'rgba(6,182,212,0.9)')
gradient.addColorStop(1, 'rgba(6,182,212,0)')''',
            'testing': '- 检查发光效果是否明显\n- 对比开启/关闭时的性能差异',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 1',
            'branch': 'feat/epic2-task3-particle-glow',
            'commit': 'feat: Add gradient and glow effects for particles',
            'labels': ['feature', 'phase-1', 'ui', 'animation', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 2-Task 4] Implement mouse interaction with particles',
            'background': '增加鼠标/触控互动，让粒子对指针位置产生吸引或排斥反应。',
            'acceptance_criteria': '''- [ ] 鼠标移动时粒子出现响应
- [ ] 交互半径与强度可配置
- [ ] 可在设置中关闭交互''',
            'files': '- `src/components/ParticleBackground.tsx`',
            'steps': '''1. 监听鼠标位置
2. 计算粒子与指针距离
3. 根据距离调整速度向量''',
            'time': '3 hours',
            'code': '''const dx = p.x - mouse.x
const dy = p.y - mouse.y
const dist = Math.sqrt(dx * dx + dy * dy)
if (dist < radius) {
  p.vx += dx / dist * force
  p.vy += dy / dist * force
}''',
            'testing': '- 检查鼠标交互是否自然\n- 确认交互关闭后无性能损耗',
            'priority': 'P2',
            'size': 'size-medium',
            'blocked_by': 'Task 1',
            'branch': 'feat/epic2-task4-mouse-interaction',
            'commit': 'feat: Add mouse interaction to particles',
            'labels': ['feature', 'phase-1', 'ui', 'animation', 'priority-p2', 'size-medium']
        },
        {
            'title': '[Epic 2-Task 5] Add performance monitoring and FPS counter',
            'background': '引入性能监控与 FPS 统计，便于调优和自动降级。',
            'acceptance_criteria': '''- [ ] 实时统计 FPS
- [ ] 支持开发模式显示指标
- [ ] 指标逻辑不影响渲染性能''',
            'files': '- `src/components/ParticleBackground.tsx`\n- `src/lib/performance.ts`',
            'steps': '''1. 创建 FPS 计算工具函数
2. 在粒子渲染循环中采样
3. 在开发模式下展示或输出日志''',
            'time': '2 hours',
            'code': '''export const createFpsTracker = () => {
  let last = performance.now()
  let frames = 0
  return () => {
    frames += 1
    const now = performance.now()
    const fps = (frames * 1000) / (now - last)
    if (now - last > 1000) { frames = 0; last = now }
    return Math.round(fps)
  }
}''',
            'testing': '- 验证 FPS 输出是否合理\n- 确认指标关闭时无额外开销',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic2-task5-performance-monitor',
            'commit': 'feat: Add FPS monitor for particle system',
            'labels': ['feature', 'phase-1', 'ui', 'performance', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 2-Task 6] Implement device detection and auto-degradation',
            'background': '根据设备性能自动降级粒子数量与效果，避免低端设备掉帧。',
            'acceptance_criteria': '''- [ ] 基于设备信息评估性能等级
- [ ] 低端设备自动减少粒子数量
- [ ] 可被用户设置覆盖''',
            'files': '- `src/lib/device-detection.ts`\n- `src/components/ParticleBackground.tsx`',
            'steps': '''1. 实现设备检测（内存、CPU、UA）
2. 根据等级调整粒子配置
3. 与用户偏好设置合并''',
            'time': '3 hours',
            'code': '''export const getDeviceTier = () => {
  const memory = (navigator as any).deviceMemory || 4
  if (memory <= 2) return 'low'
  if (memory <= 4) return 'medium'
  return 'high'
}''',
            'testing': '- 模拟不同设备等级配置\n- 确认降级策略生效',
            'priority': 'P0',
            'size': 'size-medium',
            'blocked_by': 'Task 5',
            'branch': 'feat/epic2-task6-device-detection',
            'commit': 'feat: Add device detection and auto-degradation',
            'labels': ['feature', 'phase-1', 'ui', 'performance', 'priority-p0', 'size-medium']
        },
        {
            'title': '[Epic 2-Task 7] Create static gradient fallback',
            'background': '为不支持 Canvas 或性能过低的环境提供静态渐变背景。',
            'acceptance_criteria': '''- [ ] 静态背景使用赛博朋克渐变
- [ ] 可在性能不足时自动切换
- [ ] 组件可复用''',
            'files': '- `src/components/StaticBackground.tsx`',
            'steps': '''1. 创建静态背景组件
2. 配置渐变色与透明度
3. 与粒子组件的降级逻辑对接''',
            'time': '2 hours',
            'code': '''export const StaticBackground = () => (
  <div className="fixed inset-0 bg-gradient-to-b from-cyber-dark to-cyber-purple" />
)''',
            'testing': '- 关闭粒子后检查背景显示\n- 验证层级不会遮挡内容',
            'priority': 'P0',
            'size': 'size-small',
            'branch': 'feat/epic2-task7-static-fallback',
            'commit': 'feat: Add static gradient fallback background',
            'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p0', 'size-small']
        },
        {
            'title': '[Epic 2-Task 8] Add user preference toggle',
            'background': '允许用户通过设置开关控制粒子背景是否开启。',
            'acceptance_criteria': '''- [ ] 设置中提供粒子背景开关
- [ ] 用户选择可持久化
- [ ] 关闭后不加载粒子逻辑''',
            'files': '- `src/components/Settings.tsx`\n- `src/app/layout.tsx`',
            'steps': '''1. 在设置中加入粒子开关
2. 持久化用户选择
3. 在 layout 中根据设置加载组件''',
            'time': '2 hours',
            'code': '''const [enableParticles, setEnableParticles] = useState(true)
if (!enableParticles) return <StaticBackground />''',
            'testing': '- 切换开关时观察背景变化\n- 刷新后检查设置是否保留',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 6',
            'branch': 'feat/epic2-task8-particle-toggle',
            'commit': 'feat: Add particle background toggle',
            'labels': ['feature', 'phase-1', 'ui', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 2-Task 9] Optimize particle count based on screen size',
            'background': '根据屏幕尺寸动态调整粒子数量，减少小屏渲染负担。',
            'acceptance_criteria': '''- [ ] 粒子数量与屏幕面积相关
- [ ] 超大屏限制最大粒子数量
- [ ] 小屏避免过密粒子''',
            'files': '- `src/components/ParticleBackground.tsx`',
            'steps': '''1. 计算屏幕面积
2. 基于面积设置粒子数量
3. 限制最大与最小值''',
            'time': '2 hours',
            'code': '''const area = width * height
const count = Math.min(120, Math.max(40, Math.floor(area / 12000)))''',
            'testing': '- 在不同分辨率下观察粒子数量\n- 确保数量变化不造成卡顿',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 6',
            'branch': 'feat/epic2-task9-particle-optimization',
            'commit': 'feat: Optimize particle count by screen size',
            'labels': ['enhancement', 'phase-1', 'ui', 'performance', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 2-Task 10] Add mobile-specific particle configuration',
            'background': '为移动端定义独立的粒子配置，降低复杂度与能耗。',
            'acceptance_criteria': '''- [ ] 移动端使用更少粒子与更低速率
- [ ] 触控设备默认弱交互
- [ ] 配置可与用户偏好结合''',
            'files': '- `src/components/ParticleBackground.tsx`',
            'steps': '''1. 识别移动端或触控设备
2. 载入移动端粒子配置
3. 与通用配置合并''',
            'time': '2 hours',
            'code': '''const isMobile = /Mobi|Android/i.test(navigator.userAgent)
const config = isMobile ? mobileConfig : desktopConfig''',
            'testing': '- 在移动设备模拟器验证粒子数量与速度\n- 检查交互是否符合预期',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 9',
            'branch': 'feat/epic2-task10-mobile-particles',
            'commit': 'feat: Add mobile-specific particle configuration',
            'labels': ['enhancement', 'phase-1', 'ui', 'performance', 'priority-p1', 'size-small']
        }
    ]

    epic_title = '[Epic 2] 动态粒子星空背景 (Dynamic Particle Background)'

    for index, task in enumerate(tasks, start=1):
        body = generate_task_body(index, epic_num, epic_title, task)
        create_task_issue(task['title'], body, task['labels'], milestone)
        time.sleep(1)

def create_epic3_tasks(epic_num: int, milestone: str):
    """Create all tasks for Epic 3"""
    print_info("Creating tasks for Epic 3...")

    tasks = [
        {
            'title': '[Epic 3-Task 1] Install and configure Framer Motion',
            'background': '引入 Framer Motion 作为统一动画框架，保证后续 3D 动效实现一致。',
            'acceptance_criteria': '''- [ ] 安装 framer-motion 依赖
- [ ] Next.js 配置兼容
- [ ] 基础 motion 组件可用''',
            'files': '- `package.json`\n- `next.config.js`',
            'steps': '''1. 安装 framer-motion
2. 检查 Next.js 配置兼容性
3. 验证基础 motion 组件渲染''',
            'time': '1 hour',
            'code': '''import { motion } from 'framer-motion'
const MotionDiv = motion.div''',
            'testing': '- 运行本地项目并验证 motion 组件渲染',
            'priority': 'P0',
            'size': 'size-small',
            'branch': 'feat/epic3-task1-framer-motion-setup',
            'commit': 'feat: Setup Framer Motion for animations',
            'labels': ['feature', 'phase-1', 'ui', 'animation', 'priority-p0', 'size-small']
        },
        {
            'title': '[Epic 3-Task 2] Create 3D tilt effect component',
            'background': '创建 Card3D 组件，实现基于鼠标位置的倾斜效果与透视。',
            'acceptance_criteria': '''- [ ] 卡片悬停时产生 3D 倾斜
- [ ] 倾斜幅度可配置
- [ ] 组件可复用''',
            'files': '- `src/components/Card3D.tsx`',
            'steps': '''1. 创建 Card3D 组件
2. 监听鼠标位置计算倾斜角度
3. 使用 motion 或 CSS transform 应用透视''',
            'time': '3 hours',
            'code': '''const rotateX = ((mouseY / height) - 0.5) * 10
const rotateY = ((mouseX / width) - 0.5) * -10
return <motion.div style={{ rotateX, rotateY }} />''',
            'testing': '- 观察悬停时倾斜是否平滑\n- 验证卡片内容布局稳定',
            'priority': 'P0',
            'size': 'size-medium',
            'blocked_by': 'Task 1',
            'branch': 'feat/epic3-task2-3d-tilt',
            'commit': 'feat: Add 3D tilt effect component',
            'labels': ['feature', 'phase-1', 'ui', 'animation', 'priority-p0', 'size-medium']
        },
        {
            'title': '[Epic 3-Task 3] Implement hover shadow and glow border',
            'background': '为 3D 卡片添加悬浮阴影与发光边框，提升立体感。',
            'acceptance_criteria': '''- [ ] Hover 时出现阴影与边框发光
- [ ] 效果统一且可复用
- [ ] 不遮挡内容''',
            'files': '- `src/components/Card3D.tsx`\n- `src/app/globals.css`',
            'steps': '''1. 定义 hover shadow 与 glow 样式
2. 应用到 Card3D 组件
3. 校验光效与可读性''',
            'time': '2 hours',
            'code': '''.card-3d-hover:hover {
  box-shadow: 0 12px 30px rgba(0,0,0,0.35), 0 0 12px rgba(6,182,212,0.4);
}''',
            'testing': '- 目视检查 hover 时阴影与边框\n- 确认滚动时无闪烁',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic3-task3-hover-effects',
            'commit': 'feat: Add hover shadow and glow border for cards',
            'labels': ['feature', 'phase-1', 'ui', 'animation', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 3-Task 4] Add smooth transition animations',
            'background': '为 3D 卡片提供更顺滑的过渡动画，减少突兀感。',
            'acceptance_criteria': '''- [ ] 进入/离开 hover 状态平滑
- [ ] 动画时长一致
- [ ] 不影响交互响应''',
            'files': '- `src/components/Card3D.tsx`',
            'steps': '''1. 使用 motion transition 配置过渡
2. 调整 duration 与 easing
3. 测试 hover 进入/退出效果''',
            'time': '2 hours',
            'code': '''const transition = { type: 'spring', stiffness: 180, damping: 20 }
return <motion.div transition={transition} />''',
            'testing': '- 检查动画是否过度抖动\n- 验证多次 hover 的稳定性',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic3-task4-transitions',
            'commit': 'feat: Add smooth transitions to 3D card',
            'labels': ['feature', 'phase-1', 'ui', 'animation', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 3-Task 5] Implement click feedback with scale animation',
            'background': '在点击卡片时加入缩放反馈，强化交互感。',
            'acceptance_criteria': '''- [ ] 点击时卡片轻微缩放
- [ ] 反馈动画短且不影响跳转
- [ ] 与 hover 动画兼容''',
            'files': '- `src/components/Card3D.tsx`',
            'steps': '''1. 增加 tap/press 动画配置
2. 与 hover 状态共存
3. 验证点击反馈触发及时''',
            'time': '2 hours',
            'code': '''<motion.div whileTap={{ scale: 0.98 }} />''',
            'testing': '- 点击卡片时观察缩放效果\n- 确认不会阻碍点击事件',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic3-task5-click-feedback',
            'commit': 'feat: Add click feedback animation for cards',
            'labels': ['feature', 'phase-1', 'ui', 'animation', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 3-Task 6] Create mobile-friendly simplified animations',
            'background': '在移动端提供简化动画，避免 3D 倾斜造成性能或体验问题。',
            'acceptance_criteria': '''- [ ] 移动端禁用复杂 3D 倾斜
- [ ] 仍保留轻量缩放或阴影
- [ ] 桌面端不受影响''',
            'files': '- `src/components/Card3D.tsx`',
            'steps': '''1. 检测移动端或触控设备
2. 切换为简化动画配置
3. 确保视觉风格一致''',
            'time': '3 hours',
            'code': '''const isTouch = 'ontouchstart' in window
const hoverConfig = isTouch ? { scale: 1.02 } : { rotateX, rotateY }''',
            'testing': '- 在移动端检查动画是否简化\n- 桌面端效果保持原样',
            'priority': 'P0',
            'size': 'size-medium',
            'blocked_by': 'Tasks 2, 3, 4, 5',
            'branch': 'feat/epic3-task6-mobile-animations',
            'commit': 'feat: Add mobile-friendly card animations',
            'labels': ['feature', 'phase-1', 'ui', 'animation', 'priority-p0', 'size-medium']
        },
        {
            'title': '[Epic 3-Task 7] Add card content readability optimization',
            'background': '确保 3D 动画下卡片内容仍清晰可读，避免过多发光或阴影干扰。',
            'acceptance_criteria': '''- [ ] 文字在 hover 状态依然清晰
- [ ] 发光/阴影不遮挡内容
- [ ] 适配暗色与亮色主题''',
            'files': '- `src/components/Card3D.tsx`',
            'steps': '''1. 调整内容层级与背景透明度
2. 增加文字对比度
3. 测试多种主题与状态''',
            'time': '2 hours',
            'code': '''.card-content {
  position: relative;
  z-index: 2;
  text-shadow: 0 1px 2px rgba(0,0,0,0.4);
}''',
            'testing': '- 观察不同背景下文字可读性\n- 验证 hover 时内容不模糊',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 6',
            'branch': 'feat/epic3-task7-readability',
            'commit': 'feat: Improve 3D card content readability',
            'labels': ['enhancement', 'phase-1', 'ui', 'animation', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 3-Task 8] Implement animation performance optimization',
            'background': '优化动画渲染性能，减少 GPU 压力与重绘开销。',
            'acceptance_criteria': '''- [ ] 使用 will-change 与 transform 优化
- [ ] 限制阴影与模糊开销
- [ ] 保持 30fps 以上''',
            'files': '- `src/components/Card3D.tsx`\n- `src/lib/animation-utils.ts`',
            'steps': '''1. 提取动画工具函数
2. 优化 transform 与阴影参数
3. 结合性能指标调整''',
            'time': '3 hours',
            'code': '''export const applyPerfHints = () => ({
  style: { willChange: 'transform' }
})''',
            'testing': '- 通过性能面板观察 FPS\n- 比较优化前后 GPU 占用',
            'priority': 'P1',
            'size': 'size-medium',
            'blocked_by': 'Task 6',
            'branch': 'feat/epic3-task8-animation-perf',
            'commit': 'perf: Optimize 3D card animation performance',
            'labels': ['enhancement', 'phase-1', 'ui', 'performance', 'priority-p1', 'size-medium']
        },
        {
            'title': '[Epic 3-Task 9] Add accessibility support for reduced motion',
            'background': '遵守用户的 reduced motion 偏好，提供动画降级方案。',
            'acceptance_criteria': '''- [ ] 支持 prefers-reduced-motion
- [ ] 动效可被关闭或简化
- [ ] 不影响布局稳定''',
            'files': '- `src/components/Card3D.tsx`',
            'steps': '''1. 读取 prefers-reduced-motion 媒体查询
2. 禁用复杂动画或降低幅度
3. 验证可读性与交互反馈''',
            'time': '2 hours',
            'code': '''const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
const enableMotion = !prefersReduced''',
            'testing': '- 启用系统 reduced motion 后验证效果\n- 检查卡片是否仍可交互',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 8',
            'branch': 'feat/epic3-task9-reduced-motion',
            'commit': 'feat: Add reduced motion support for cards',
            'labels': ['enhancement', 'phase-1', 'ui', 'animation', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 3-Task 10] Create card animation documentation',
            'background': '编写 3D 卡片动效的使用说明与配置指南。',
            'acceptance_criteria': '''- [ ] 文档包含动画参数说明
- [ ] 示例覆盖 hover 与点击反馈
- [ ] 提供性能与可访问性注意事项''',
            'files': '- `docs/card-animations.md`',
            'steps': '''1. 描述动画组件结构
2. 列出关键参数与默认值
3. 添加性能与可访问性说明''',
            'time': '1 hour',
            'code': '''# Card Animation Guide
- hover: tilt + shadow
- tap: scale feedback
- reduced motion: disabled tilt''',
            'testing': '- 检查文档内容完整性与可读性',
            'priority': 'P3',
            'size': 'size-small',
            'blocked_by': 'Task 9',
            'branch': 'docs/epic3-task10-animation-docs',
            'commit': 'docs: Add card animation documentation',
            'labels': ['documentation', 'phase-1', 'animation', 'priority-p3', 'size-small']
        }
    ]

    epic_title = '[Epic 3] 3D 卡片悬浮效果 (3D Card Hover Effects)'

    for index, task in enumerate(tasks, start=1):
        body = generate_task_body(index, epic_num, epic_title, task)
        create_task_issue(task['title'], body, task['labels'], milestone)
        time.sleep(1)

def create_epic4_tasks(epic_num: int, milestone: str):
    """Create all tasks for Epic 4"""
    print_info("Creating tasks for Epic 4...")

    tasks = [
        {
            'title': '[Epic 4-Task 1] Design hand-drawn style category icons',
            'background': '设计一套手绘风格分类图标，作为二次元视觉体系的核心元素。',
            'acceptance_criteria': '''- [ ] 图标风格统一、可识别
- [ ] 支持多分类扩展
- [ ] SVG 兼容与可压缩''',
            'files': '- `public/icons/*.svg`',
            'steps': '''1. 定义手绘风格视觉基准
2. 设计并导出分类图标 SVG
3. 验证在页面中的清晰度与一致性''',
            'time': '4 hours',
            'code': '''// SVG export checklist
// - ViewBox set
// - Stroke width consistent
// - No embedded raster images''',
            'testing': '- 在不同尺寸下检查图标清晰度\n- 验证 SVG 文件大小',
            'priority': 'P0',
            'size': 'size-large',
            'branch': 'design/epic4-task1-category-icons',
            'commit': 'design: Add hand-drawn category icons',
            'labels': ['feature', 'phase-2', 'design', 'priority-p0', 'size-large']
        },
        {
            'title': '[Epic 4-Task 2] Create decorative geometric elements',
            'background': '制作装饰性几何图形素材，用于背景与布局点缀。',
            'acceptance_criteria': '''- [ ] 几何元素可复用
- [ ] 风格与图标一致
- [ ] 支持透明背景''',
            'files': '- `public/decorations/*.svg`\n- `src/components/Decorations.tsx`',
            'steps': '''1. 设计几何装饰 SVG
2. 创建 Decorations 组件封装
3. 验证多页面复用效果''',
            'time': '3 hours',
            'code': '''export const Decorations = () => (
  <img src="/decorations/triangle.svg" alt="" aria-hidden />
)''',
            'testing': '- 检查装饰元素在不同背景下效果\n- 验证不会干扰内容阅读',
            'priority': 'P1',
            'size': 'size-medium',
            'branch': 'design/epic4-task2-geometric-elements',
            'commit': 'design: Add decorative geometric elements',
            'labels': ['feature', 'phase-2', 'design', 'ui', 'priority-p1', 'size-medium']
        },
        {
            'title': '[Epic 4-Task 3] Design empty state illustrations',
            'background': '为空状态设计插画，提升空白页面的情绪表达。',
            'acceptance_criteria': '''- [ ] 空状态插画与整体风格统一
- [ ] 支持不同尺寸渲染
- [ ] SVG 体积可控''',
            'files': '- `public/illustrations/*.svg`',
            'steps': '''1. 设计空状态插画
2. 输出可缩放 SVG
3. 在页面中预览效果''',
            'time': '3 hours',
            'code': '''// Empty state illustration guidelines
// - Simple lines
// - Limited color palette
// - Transparent background''',
            'testing': '- 在空状态页面预览插画效果\n- 检查缩放清晰度',
            'priority': 'P1',
            'size': 'size-medium',
            'branch': 'design/epic4-task3-empty-states',
            'commit': 'design: Add empty state illustrations',
            'labels': ['feature', 'phase-2', 'design', 'priority-p1', 'size-medium']
        },
        {
            'title': '[Epic 4-Task 4] Implement icon component system',
            'background': '将图标抽象为组件系统，统一尺寸、颜色与交互。',
            'acceptance_criteria': '''- [ ] Icon 组件支持 name/size/color
- [ ] 统一默认尺寸与对齐方式
- [ ] 适配手绘风格 SVG''',
            'files': '- `src/components/Icon.tsx`',
            'steps': '''1. 创建 Icon 组件并支持传参
2. 统一图标尺寸与填充规则
3. 应用到现有页面''',
            'time': '2 hours',
            'code': '''type IconProps = { name: string; size?: number; className?: string }
const Icon = ({ name, size = 24 }: IconProps) => (
  <img src={`/icons/${name}.svg`} width={size} height={size} alt="" />
)''',
            'testing': '- 检查所有图标渲染是否一致\n- 验证尺寸与颜色传参',
            'priority': 'P0',
            'size': 'size-small',
            'blocked_by': 'Task 1',
            'branch': 'feat/epic4-task4-icon-system',
            'commit': 'feat: Add icon component system',
            'labels': ['feature', 'phase-2', 'ui', 'design', 'priority-p0', 'size-small']
        },
        {
            'title': '[Epic 4-Task 5] Add decorative line art elements',
            'background': '增加线稿风格装饰元素，增强二次元氛围。',
            'acceptance_criteria': '''- [ ] 线稿元素可复用
- [ ] 与几何元素风格一致
- [ ] 支持透明背景''',
            'files': '- `src/components/LineArt.tsx`',
            'steps': '''1. 设计线稿素材或复用 SVG
2. 创建 LineArt 组件
3. 验证在页面中的布局效果''',
            'time': '2 hours',
            'code': '''export const LineArt = () => (
  <svg aria-hidden className="line-art" />
)''',
            'testing': '- 检查线稿元素在不同背景下对比度\n- 确认不会干扰布局',
            'priority': 'P2',
            'size': 'size-small',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic4-task5-line-art',
            'commit': 'feat: Add decorative line art elements',
            'labels': ['feature', 'phase-2', 'ui', 'design', 'priority-p2', 'size-small']
        },
        {
            'title': '[Epic 4-Task 6] Create loading state illustrations',
            'background': '为加载状态设计插画，提升等待体验。',
            'acceptance_criteria': '''- [ ] 加载插画风格统一
- [ ] 适配小尺寸显示
- [ ] 可在加载组件中复用''',
            'files': '- `public/illustrations/loading.svg`\n- `src/components/Loading.tsx`',
            'steps': '''1. 设计 loading 插画并导出 SVG
2. 在 Loading 组件中引用
3. 验证加载状态展示''',
            'time': '2 hours',
            'code': '''const Loading = () => (
  <img src="/illustrations/loading.svg" alt="Loading" />
)''',
            'testing': '- 检查加载状态插画显示是否清晰\n- 验证不同尺寸下可读性',
            'priority': 'P1',
            'size': 'size-small',
            'branch': 'design/epic4-task6-loading-states',
            'commit': 'design: Add loading state illustrations',
            'labels': ['feature', 'phase-2', 'design', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 4-Task 7] Implement icon animation on hover',
            'background': '为图标添加轻量 hover 动效，提升交互反馈。',
            'acceptance_criteria': '''- [ ] Hover 时图标有轻微动画
- [ ] 动效不影响性能
- [ ] 支持全局禁用''',
            'files': '- `src/components/Icon.tsx`',
            'steps': '''1. 为 Icon 组件添加 hover 动画样式
2. 控制动效强度与时长
3. 验证低性能设备效果''',
            'time': '2 hours',
            'code': '''.icon-hover:hover {
  transform: translateY(-2px) scale(1.03);
  transition: transform 120ms ease;
}''',
            'testing': '- 检查 hover 动画的流畅度\n- 验证是否影响点击响应',
            'priority': 'P2',
            'size': 'size-small',
            'blocked_by': 'Task 4',
            'branch': 'feat/epic4-task7-icon-animations',
            'commit': 'feat: Add hover animation to icons',
            'labels': ['feature', 'phase-2', 'ui', 'animation', 'priority-p2', 'size-small']
        },
        {
            'title': '[Epic 4-Task 8] Optimize SVG files for performance',
            'background': '优化 SVG 体积与渲染性能，提升首屏加载速度。',
            'acceptance_criteria': '''- [ ] SVG 文件体积可控
- [ ] 移除冗余路径与 metadata
- [ ] 视觉效果保持一致''',
            'files': '- `public/icons/*.svg`\n- `public/illustrations/*.svg`',
            'steps': '''1. 使用 SVGO 清理 SVG
2. 统一 viewBox 与尺寸
3. 检查优化后显示效果''',
            'time': '2 hours',
            'code': '''// SVGO config snippet
// removeMetadata: true
// convertPathData: true''',
            'testing': '- 比较优化前后文件大小\n- 检查 SVG 渲染是否异常',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Tasks 1, 3, 6',
            'branch': 'perf/epic4-task8-svg-optimization',
            'commit': 'perf: Optimize SVG assets',
            'labels': ['enhancement', 'phase-2', 'design', 'performance', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 4-Task 9] Add responsive scaling for illustrations',
            'background': '为插画与装饰元素添加响应式缩放策略，确保多端一致。',
            'acceptance_criteria': '''- [ ] 插画随屏幕尺寸比例缩放
- [ ] 避免遮挡核心内容
- [ ] 桌面端保持原比例''',
            'files': '- `src/components/Decorations.tsx`\n- `src/app/globals.css`',
            'steps': '''1. 为装饰元素添加响应式样式
2. 使用 CSS clamp 控制大小
3. 在多端验证布局''',
            'time': '2 hours',
            'code': '''.illustration {
  width: clamp(120px, 18vw, 240px);
  height: auto;
}''',
            'testing': '- 在不同分辨率下检查插画比例\n- 确认不遮挡正文',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Tasks 2, 5',
            'branch': 'feat/epic4-task9-responsive-illustrations',
            'commit': 'feat: Add responsive scaling for illustrations',
            'labels': ['feature', 'phase-2', 'ui', 'design', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 4-Task 10] Create illustration style guide',
            'background': '输出插画风格指南，统一后续设计与实现规范。',
            'acceptance_criteria': '''- [ ] 描述颜色、线条与阴影规范
- [ ] 提供插画应用示例
- [ ] 便于新成员快速上手''',
            'files': '- `docs/illustration-guide.md`',
            'steps': '''1. 整理插画风格规则
2. 提供示例与注意事项
3. 说明输出与优化流程''',
            'time': '1 hour',
            'code': '''# Illustration Guide
- Line width: 2px
- Palette: cyber purple + cyan
- Use transparent background''',
            'testing': '- 检查文档是否完整易读',
            'priority': 'P3',
            'size': 'size-small',
            'blocked_by': 'Tasks 1, 2, 3',
            'branch': 'docs/epic4-task10-style-guide',
            'commit': 'docs: Add illustration style guide',
            'labels': ['documentation', 'phase-2', 'design', 'priority-p3', 'size-small']
        }
    ]

    epic_title = '[Epic 4] 动漫风格图标和插画 (Anime-style Icons and Illustrations)'

    for index, task in enumerate(tasks, start=1):
        body = generate_task_body(index, epic_num, epic_title, task)
        create_task_issue(task['title'], body, task['labels'], milestone)
        time.sleep(1)

def create_epic5_tasks(epic_num: int, milestone: str):
    """Create all tasks for Epic 5"""
    print_info("Creating tasks for Epic 5...")

    tasks = [
        {
            'title': '[Epic 5-Task 1] Design or source kanban musume character assets',
            'background': '准备看板娘角色素材，包含基本表情与姿态版本。',
            'acceptance_criteria': '''- [ ] 素材风格与整体 UI 一致
- [ ] 至少提供基础表情集
- [ ] 资源尺寸与格式规范''',
            'files': '- `public/kanban-musume/*.png`',
            'steps': '''1. 确定角色风格与尺寸标准
2. 设计或采购角色素材
3. 导出并归档资源''',
            'time': '4 hours',
            'code': '''// Asset checklist
// - PNG with transparency
// - 2x size for retina
// - naming: pose-expression.png''',
            'testing': '- 检查素材清晰度\n- 确保资源体积合理',
            'priority': 'P0',
            'size': 'size-large',
            'branch': 'design/epic5-task1-character-assets',
            'commit': 'design: Add kanban musume character assets',
            'labels': ['feature', 'phase-2', 'design', 'priority-p0', 'size-large']
        },
        {
            'title': '[Epic 5-Task 2] Create kanban musume component with fixed positioning',
            'background': '实现看板娘组件并固定在页面角落，作为可交互 UI 元素。',
            'acceptance_criteria': '''- [ ] 看板娘固定在页面右下角
- [ ] 可配置显示/隐藏
- [ ] 不遮挡核心操作区域''',
            'files': '- `src/components/KanbanMusume.tsx`',
            'steps': '''1. 创建 KanbanMusume 组件
2. 设置固定定位与层级
3. 添加可配置 props''',
            'time': '2 hours',
            'code': '''const KanbanMusume = () => (
  <div className="fixed bottom-6 right-6 z-40">
    <img src="/kanban-musume/base.png" alt="Kanban Musume" />
  </div>
)''',
            'testing': '- 检查不同页面的定位\n- 确认不会遮挡主要内容',
            'priority': 'P0',
            'size': 'size-small',
            'blocked_by': 'Task 1',
            'branch': 'feat/epic5-task2-character-component',
            'commit': 'feat: Add kanban musume component',
            'labels': ['feature', 'phase-2', 'ui', 'priority-p0', 'size-small']
        },
        {
            'title': '[Epic 5-Task 3] Implement click interaction and dialog system',
            'background': '为看板娘添加点击交互与对话系统，提供基础互动。',
            'acceptance_criteria': '''- [ ] 点击触发对话框
- [ ] 对话内容可配置
- [ ] 对话框可关闭''',
            'files': '- `src/components/KanbanMusume.tsx`\n- `src/components/CharacterDialog.tsx`',
            'steps': '''1. 创建 CharacterDialog 组件
2. 看板娘点击触发对话
3. 提供关闭与切换逻辑''',
            'time': '3 hours',
            'code': '''const [open, setOpen] = useState(false)
const handleClick = () => setOpen(true)''',
            'testing': '- 点击看板娘时验证对话框弹出\n- 测试关闭按钮与状态切换',
            'priority': 'P0',
            'size': 'size-medium',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic5-task3-dialog-system',
            'commit': 'feat: Add character dialog system',
            'labels': ['feature', 'phase-2', 'ui', 'priority-p0', 'size-medium']
        },
        {
            'title': '[Epic 5-Task 4] Add dynamic expressions and state changes',
            'background': '根据交互状态切换看板娘表情与姿态，提升情感反馈。',
            'acceptance_criteria': '''- [ ] 至少支持 3 种表情
- [ ] 状态切换平滑
- [ ] 表情与事件绑定''',
            'files': '- `src/components/KanbanMusume.tsx`',
            'steps': '''1. 定义表情状态与资源映射
2. 在交互事件中切换状态
3. 添加默认状态与回退''',
            'time': '3 hours',
            'code': '''const expressionMap = {
  idle: '/kanban-musume/idle.png',
  happy: '/kanban-musume/happy.png',
  surprise: '/kanban-musume/surprise.png'
}''',
            'testing': '- 触发不同事件验证表情切换\n- 检查状态回退逻辑',
            'priority': 'P1',
            'size': 'size-medium',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic5-task4-expressions',
            'commit': 'feat: Add dynamic expressions to character',
            'labels': ['feature', 'phase-2', 'ui', 'animation', 'priority-p1', 'size-medium']
        },
        {
            'title': '[Epic 5-Task 5] Create quick action menu',
            'background': '提供快捷操作菜单，提升常用功能访问效率。',
            'acceptance_criteria': '''- [ ] 菜单包含 3-5 个快捷入口
- [ ] 与看板娘交互触发
- [ ] 支持扩展''',
            'files': '- `src/components/QuickActionMenu.tsx`',
            'steps': '''1. 设计 QuickActionMenu 结构
2. 与看板娘交互触发显示
3. 提供配置化入口列表''',
            'time': '3 hours',
            'code': '''const actions = [
  { id: 'search', label: 'Search', onClick: openSearch },
  { id: 'settings', label: 'Settings', onClick: openSettings }
]''',
            'testing': '- 点击菜单项验证功能触发\n- 检查菜单定位与遮挡',
            'priority': 'P0',
            'size': 'size-medium',
            'blocked_by': 'Task 3',
            'branch': 'feat/epic5-task5-action-menu',
            'commit': 'feat: Add quick action menu for character',
            'labels': ['feature', 'phase-2', 'ui', 'priority-p0', 'size-medium']
        },
        {
            'title': '[Epic 5-Task 6] Implement time-based greeting messages',
            'background': '基于时间段展示不同的问候语，提高角色互动感。',
            'acceptance_criteria': '''- [ ] 早/午/晚问候语不同
- [ ] 支持可配置文案
- [ ] 与对话系统集成''',
            'files': '- `src/components/KanbanMusume.tsx`\n- `src/lib/greetings.ts`',
            'steps': '''1. 设计问候语配置表
2. 根据当前时间选择文案
3. 与对话系统联动展示''',
            'time': '2 hours',
            'code': '''export const getGreeting = (hour: number) => {
  if (hour < 12) return 'Good morning'
  if (hour < 18) return 'Good afternoon'
  return 'Good evening'
}''',
            'testing': '- 模拟不同时间验证文案\n- 检查对话触发逻辑',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 3',
            'branch': 'feat/epic5-task6-greetings',
            'commit': 'feat: Add time-based greetings for character',
            'labels': ['feature', 'phase-2', 'ui', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 5-Task 7] Add minimize/hide functionality',
            'background': '提供最小化/隐藏功能，避免看板娘遮挡内容。',
            'acceptance_criteria': '''- [ ] 用户可隐藏/展开看板娘
- [ ] 状态可持久化
- [ ] 与设置面板联动''',
            'files': '- `src/components/KanbanMusume.tsx`\n- `src/components/Settings.tsx`',
            'steps': '''1. 添加最小化按钮与状态
2. 将状态持久化
3. 在设置中加入控制开关''',
            'time': '2 hours',
            'code': '''const [collapsed, setCollapsed] = useState(false)
if (collapsed) return <MiniButton />''',
            'testing': '- 切换最小化状态验证 UI\n- 刷新后确认状态保留',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic5-task7-minimize',
            'commit': 'feat: Add minimize/hide functionality',
            'labels': ['feature', 'phase-2', 'ui', 'priority-p1', 'size-small']
        },
        {
            'title': '[Epic 5-Task 8] Create mobile-responsive layout',
            'background': '为移动端重新布局看板娘组件，防止遮挡内容与交互冲突。',
            'acceptance_criteria': '''- [ ] 移动端位置与尺寸适配
- [ ] 不遮挡主要交互区域
- [ ] 可与快捷菜单协同''',
            'files': '- `src/components/KanbanMusume.tsx`',
            'steps': '''1. 添加移动端响应式样式
2. 调整位置与缩放比例
3. 验证与菜单组合的布局''',
            'time': '3 hours',
            'code': '''@media (max-width: 640px) {
  .kanban-musume { width: 120px; right: 12px; bottom: 12px; }
}''',
            'testing': '- 在移动端模拟器验证布局\n- 检查交互区域是否被遮挡',
            'priority': 'P0',
            'size': 'size-medium',
            'blocked_by': 'Tasks 2, 3, 5',
            'branch': 'feat/epic5-task8-mobile-responsive',
            'commit': 'feat: Add mobile responsive layout for character',
            'labels': ['feature', 'phase-2', 'ui', 'priority-p0', 'size-medium']
        },
        {
            'title': '[Epic 5-Task 9] Implement drag-and-drop position adjustment',
            'background': '允许用户拖拽看板娘调整位置，提高个性化体验。',
            'acceptance_criteria': '''- [ ] 支持拖拽移动位置
- [ ] 位置可持久化
- [ ] 移动端行为合理''',
            'files': '- `src/components/KanbanMusume.tsx`',
            'steps': '''1. 实现拖拽事件与位置更新
2. 保存位置到 localStorage
3. 限制拖拽范围避免出屏''',
            'time': '3 hours',
            'code': '''const handleDrag = (event) => {
  setPosition({ x: event.clientX, y: event.clientY })
}''',
            'testing': '- 拖拽后检查位置是否正确\n- 刷新后验证位置保存',
            'priority': 'P2',
            'size': 'size-medium',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic5-task9-draggable',
            'commit': 'feat: Add draggable position for character',
            'labels': ['feature', 'phase-2', 'ui', 'priority-p2', 'size-medium']
        },
        {
            'title': '[Epic 5-Task 10] Add entrance/exit animations',
            'background': '为看板娘组件添加进入/退出动画，提升视觉体验。',
            'acceptance_criteria': '''- [ ] 出现/消失时有过渡动画
- [ ] 动画时长不影响交互
- [ ] 可与缩放/移动兼容''',
            'files': '- `src/components/KanbanMusume.tsx`',
            'steps': '''1. 添加进入与退出动画
2. 控制动画时长与缓动
3. 验证动画与交互共存''',
            'time': '2 hours',
            'code': '''<motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} />''',
            'testing': '- 观察动画是否顺滑\n- 确认动画不阻断点击',
            'priority': 'P1',
            'size': 'size-small',
            'blocked_by': 'Task 2',
            'branch': 'feat/epic5-task10-animations',
            'commit': 'feat: Add entrance/exit animations for character',
            'labels': ['feature', 'phase-2', 'ui', 'animation', 'priority-p1', 'size-small']
        }
    ]

    epic_title = '[Epic 5] 看板娘角色助手 (Kanban Musume Character Assistant)'

    for index, task in enumerate(tasks, start=1):
        body = generate_task_body(index, epic_num, epic_title, task)
        create_task_issue(task['title'], body, task['labels'], milestone)
        time.sleep(1)

def main():
    """Main execution function"""
    print_header("GitHub Issues Generator for UI/UX Cyberpunk Upgrade")
    print_info("Project: nav_blog UI 升级")
    print_info("Repository: WillowSageL/nav_blog")

    # Step 1: Create labels
    create_labels()
    time.sleep(1)

    # Step 2: Create milestones
    milestone1, milestone2 = create_milestones()
    time.sleep(1)

    # Step 3: Create Epic Issues
    print_header("Step 3: Creating Epic Issues")
    epic1_body = generate_epic1_body()
    epic1_num = create_epic_issue(
        title="[Epic 1] 赛博朋克视觉风格 (Cyberpunk Visual Style)",
        body=epic1_body,
        labels=['epic', 'phase-1', 'ui', 'design', 'priority-p0'],
        milestone=milestone1
    )

    epic2_body = generate_epic2_body()
    epic2_num = create_epic_issue(
        title="[Epic 2] 动态粒子星空背景 (Dynamic Particle Background)",
        body=epic2_body,
        labels=['epic', 'phase-1', 'ui', 'animation', 'priority-p0'],
        milestone=milestone1
    )

    epic3_body = generate_epic3_body()
    epic3_num = create_epic_issue(
        title="[Epic 3] 3D 卡片悬浮效果 (3D Card Hover Effects)",
        body=epic3_body,
        labels=['epic', 'phase-1', 'ui', 'animation', 'priority-p1'],
        milestone=milestone1
    )

    epic4_body = generate_epic4_body()
    epic4_num = create_epic_issue(
        title="[Epic 4] 动漫风格图标和插画 (Anime-style Icons and Illustrations)",
        body=epic4_body,
        labels=['epic', 'phase-2', 'ui', 'design', 'priority-p1'],
        milestone=milestone2
    )

    epic5_body = generate_epic5_body()
    epic5_num = create_epic_issue(
        title="[Epic 5] 看板娘角色助手 (Kanban Musume Character Assistant)",
        body=epic5_body,
        labels=['epic', 'phase-2', 'ui', 'priority-p1'],
        milestone=milestone2
    )

    # Step 4: Create Task Issues
    print_header("Step 4: Creating Task Issues")
    if epic1_num:
        create_epic1_tasks(epic1_num, milestone1)
    if epic2_num:
        create_epic2_tasks(epic2_num, milestone1)
    if epic3_num:
        create_epic3_tasks(epic3_num, milestone1)
    if epic4_num:
        create_epic4_tasks(epic4_num, milestone2)
    if epic5_num:
        create_epic5_tasks(epic5_num, milestone2)

    print_header("Summary")
    print_success(f"Epic 1: #{epic1_num}")
    print_success(f"Epic 2: #{epic2_num}")
    print_success(f"Epic 3: #{epic3_num}")
    print_success(f"Epic 4: #{epic4_num}")
    print_success(f"Epic 5: #{epic5_num}")
    print_info("All epics and tasks processed. Existing issues were skipped by title.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nScript interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
