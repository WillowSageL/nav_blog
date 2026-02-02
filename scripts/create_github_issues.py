#!/usr/bin/env python3
"""
GitHub Issues Generator for UI/UX Upgrade Project
Creates Epics, Tasks, Milestones, and Labels based on PRD
"""

import subprocess
import json
import time
from typing import Dict, List, Optional

class GitHubIssueCreator:
    def __init__(self, project_name: str = "nav_blog UI 升级"):
        self.project_name = project_name
        self.epic_numbers = {}
        self.milestone_numbers = {}

    def run_gh_command(self, args: List[str], retry: int = 3) -> Optional[str]:
        """Execute gh CLI command with retry logic"""
        for attempt in range(retry):
            try:
                result = subprocess.run(
                    ['gh'] + args,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout.strip()
            except subprocess.CalledProcessError as e:
                if attempt < retry - 1:
                    time.sleep(2)
                    continue
                print(f"Error executing command: {' '.join(args)}")
                print(f"Error: {e.stderr}")
                return None
        return None

    def create_labels(self):
        """Create all necessary labels"""
        print("Creating labels...")
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
            result = self.run_gh_command([
                'label', 'create', name,
                '--color', color,
                '--description', description,
                '--force'
            ])
            if result is not None:
                print(f"  ✓ Created label: {name}")

    def create_milestones(self):
        """Create project milestones"""
        print("\nCreating milestones...")
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

        for milestone in milestones:
            result = self.run_gh_command([
                'api', 'repos/{owner}/{repo}/milestones',
                '-f', f'title={milestone["title"]}',
                '-f', f'description={milestone["description"]}',
                '-f', 'state=open'
            ])
            if result:
                data = json.loads(result)
                self.milestone_numbers[milestone["title"]] = data['number']
                print(f"  ✓ Created milestone: {milestone['title']} (#{data['number']})")

    def create_epic_issue(self, epic_data: Dict) -> Optional[int]:
        """Create an Epic issue"""
        body = f"""## Epic Overview

{epic_data['description']}

## User Story

**作为** {epic_data['as_a']}
**我想要** {epic_data['i_want']}
**以便** {epic_data['so_that']}

## Acceptance Criteria

{epic_data['acceptance_criteria']}

## Tasks Breakdown

This epic will be broken down into {epic_data['task_count']} tasks:

{epic_data['tasks_list']}

## Success Metrics

{epic_data['success_metrics']}

## Dependencies

{epic_data['dependencies']}

---
*This is an Epic issue. Individual tasks will be created as separate issues and linked to this epic.*
"""

        labels = ['epic'] + epic_data.get('labels', [])

        result = self.run_gh_command([
            'issue', 'create',
            '--title', epic_data['title'],
            '--body', body,
            '--label', ','.join(labels),
            '--milestone', str(self.milestone_numbers.get(epic_data['milestone'], ''))
        ])

        if result:
            issue_url = result
            issue_number = int(issue_url.split('/')[-1])
            print(f"  ✓ Created Epic: {epic_data['title']} (#{issue_number})")
            return issue_number
        return None

    def create_task_issue(self, task_data: Dict) -> Optional[int]:
        """Create a Task issue"""
        body = f"""## Background

{task_data['background']}

## Acceptance Criteria

{task_data['acceptance_criteria']}

## Implementation Plan

**Files to Modify:**
{task_data['files_to_modify']}

**Implementation Steps:**
{task_data['implementation_steps']}

**Estimated Time:** {task_data['estimated_time']}

## Core Logic

```typescript
{task_data['core_logic']}
```

## Testing Requirements

{task_data['testing_requirements']}

## Dependencies

- **Priority:** {task_data['priority']}
- **Size:** {task_data['size']}
- **Blocked by:** {task_data.get('blocked_by', 'None')}
- **Blocks:** {task_data.get('blocks', 'None')}

## Git Worktree

```bash
# Create worktree for this task
git worktree add ../nav_blog-{task_data['branch_name']} -b {task_data['branch_name']}
cd ../nav_blog-{task_data['branch_name']}

# After completion
git add .
git commit -m "{task_data['commit_message']}"
git push -u origin {task_data['branch_name']}

# Create PR
gh pr create --title "{task_data['title']}" --body "Closes #{task_data['epic_number']}"
```

## Related

- Epic: #{task_data['epic_number']} {task_data['epic_title']}
"""

        labels = task_data.get('labels', [])

        result = self.run_gh_command([
            'issue', 'create',
            '--title', task_data['title'],
            '--body', body,
            '--label', ','.join(labels),
            '--milestone', str(self.milestone_numbers.get(task_data['milestone'], ''))
        ])

        if result:
            issue_url = result
            issue_number = int(issue_url.split('/')[-1])
            print(f"    ✓ Created Task: {task_data['title']} (#{issue_number})")
            return issue_number
        return None

    def create_all_issues(self):
        """Create all Epics and Tasks"""
        print("\n" + "="*80)
        print("Creating Epic and Task Issues")
        print("="*80)

        # Epic 1: Cyberpunk Visual Style
        epic1_number = self.create_epic_1()
        time.sleep(1)

        # Epic 2: Dynamic Particle Background
        epic2_number = self.create_epic_2()
        time.sleep(1)

        # Epic 3: 3D Card Effects
        epic3_number = self.create_epic_3()
        time.sleep(1)

        # Epic 4: Anime Icons
        epic4_number = self.create_epic_4()
        time.sleep(1)

        # Epic 5: Kanban Musume
        epic5_number = self.create_epic_5()

        print("\n" + "="*80)
        print("All issues created successfully!")
        print("="*80)

    def create_epic_1(self) -> Optional[int]:
        """Epic 1: Cyberpunk Visual Style"""
        print("\n📦 Creating Epic 1: Cyberpunk Visual Style")

        epic_data = {
            'title': '[Epic 1] 赛博朋克视觉风格 (Cyberpunk Visual Style)',
            'description': '实现完整的赛博朋克配色方案，包括深色基调、霓虹色强调、渐变效果和发光元素。',
            'as_a': '二次元爱好者',
            'i_want': '看到深蓝、紫色、霓虹色调的赛博朋克配色方案',
            'so_that': '界面能反映我的审美偏好，而不是千篇一律的商务风格',
            'acceptance_criteria': '''- [ ] 主色调采用深蓝（#0a0e27）、紫色（#6366f1）、霓虹粉（#ec4899）、霓虹青（#06b6d4）
- [ ] 背景使用深色基调，避免刺眼的亮色
- [ ] 文字和图标使用高对比度的霓虹色，确保可读性
- [ ] 支持暗色模式（默认）和亮色模式切换
- [ ] 移动端保持相同的配色方案''',
            'task_count': 10,
            'tasks_list': '''1. Setup Tailwind CSS cyberpunk color palette
2. Create dark theme base styles
3. Implement neon color scheme for text/icons
4. Add glow effects to interactive elements
5. Create light mode variant
6. Update all existing components
7. Add theme toggle functionality
8. Implement responsive color adjustments
9. Add high contrast mode for accessibility
10. Create color system documentation''',
            'success_metrics': '''- All pages use new cyberpunk color scheme
- Theme toggle works smoothly
- Accessibility contrast ratios meet WCAG AA standards
- Mobile and desktop have consistent styling''',
            'dependencies': 'None - This is a foundational epic',
            'milestone': 'Phase 1: Visual Style Refactoring',
            'labels': ['phase-1', 'ui', 'design', 'priority-p0']
        }

        epic_number = self.create_epic_issue(epic_data)
        if epic_number:
            self.epic_numbers['epic1'] = epic_number
            self.create_epic_1_tasks(epic_number)
        return epic_number

    def create_epic_1_tasks(self, epic_number: int):
        """Create tasks for Epic 1"""
        print("  Creating tasks for Epic 1...")

        tasks = [
            {
                'title': '[Epic 1 - Task 1] Setup Tailwind CSS cyberpunk color palette',
                'background': '需要在 Tailwind 配置中定义赛博朋克风格的颜色系统，包括深蓝、紫色、霓虹粉、霓虹青等主题色。',
                'acceptance_criteria': '''- [ ] 在 tailwind.config.js 中添加自定义颜色
- [ ] 定义 CSS 变量用于动态主题切换
- [ ] 颜色命名清晰且语义化
- [ ] 包含所有必需的色调变体（50-950）''',
                'files_to_modify': '''- `tailwind.config.js`
- `src/app/globals.css`''',
                'implementation_steps': '''1. 在 tailwind.config.js 的 theme.extend.colors 中添加颜色定义
2. 在 globals.css 中定义 CSS 变量
3. 测试颜色在不同组件中的显示效果''',
                'estimated_time': '2 hours',
                'core_logic': '''// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        cyber: {
          dark: '#0a0e27',
          purple: '#6366f1',
          pink: '#ec4899',
          cyan: '#06b6d4',
        }
      }
    }
  }
}''',
                'testing_requirements': '''- 验证所有颜色在浏览器中正确显示
- 检查颜色对比度是否符合可访问性标准''',
                'priority': 'P0',
                'size': 'size-small',
                'branch_name': 'feat/epic1-task1-tailwind-colors',
                'commit_message': 'feat: Add cyberpunk color palette to Tailwind config',
                'epic_number': epic_number,
                'epic_title': 'Cyberpunk Visual Style',
                'milestone': 'Phase 1: Visual Style Refactoring',
                'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p0', 'size-small']
            },
            {
                'title': '[Epic 1 - Task 2] Create dark theme base styles',
                'background': '创建深色主题的基础样式，包括深蓝色背景和基础布局样式。',
                'acceptance_criteria': '''- [ ] 页面背景使用深蓝色（#0a0e27）
- [ ] 文字颜色具有足够的对比度
- [ ] 所有基础组件应用深色主题
- [ ] 避免刺眼的亮色''',
                'files_to_modify': '''- `src/app/globals.css`
- `src/app/layout.tsx`''',
                'implementation_steps': '''1. 在 globals.css 中定义 dark theme 基础样式
2. 更新 body 背景色
3. 设置默认文字颜色和链接颜色''',
                'estimated_time': '2 hours',
                'core_logic': '''/* globals.css */
:root {
  --bg-primary: #0a0e27;
  --text-primary: #e2e8f0;
}

body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
}''',
                'testing_requirements': '''- 检查所有页面的背景色和文字色
- 验证可读性''',
                'priority': 'P0',
                'size': 'size-small',
                'blocked_by': f'#{epic_number} Task 1',
                'branch_name': 'feat/epic1-task2-dark-theme-base',
                'commit_message': 'feat: Implement dark theme base styles',
                'epic_number': epic_number,
                'epic_title': 'Cyberpunk Visual Style',
                'milestone': 'Phase 1: Visual Style Refactoring',
                'labels': ['feature', 'phase-1', 'ui', 'design', 'priority-p0', 'size-small']
            },
        ]

        for task in tasks[:2]:  # Create first 2 tasks
            self.create_task_issue(task)
            time.sleep(0.5)


def main():
    creator = GitHubIssueCreator()

    # Step 1: Create labels
    creator.create_labels()

    # Step 2: Create milestones
    creator.create_milestones()

    # Step 3: Create all issues
    creator.create_all_issues()


if __name__ == '__main__':
    main()
