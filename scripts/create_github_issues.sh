#!/bin/bash
# GitHub Issues Creator for UI/UX Upgrade Project
# Creates Epics, Tasks, Milestones, and Labels based on PRD

set -e

PROJECT_NAME="nav_blog UI 升级"
REPO="WillowSageL/nav_blog"

echo "=========================================="
echo "GitHub Issues Creator"
echo "Project: $PROJECT_NAME"
echo "=========================================="

# Step 1: Create Labels
echo ""
echo "Step 1: Creating Labels..."
echo "----------------------------------------"

# Type labels
gh label create "epic" --color "7057ff" --description "Epic issue containing multiple tasks" --force 2>/dev/null || true
gh label create "feature" --color "a2eeef" --description "New feature or request" --force 2>/dev/null || true
gh label create "enhancement" --color "84b6eb" --description "Enhancement to existing feature" --force 2>/dev/null || true
gh label create "testing" --color "d4c5f9" --description "Testing related tasks" --force 2>/dev/null || true
gh label create "documentation" --color "0075ca" --description "Documentation improvements" --force 2>/dev/null || true

# Phase labels
gh label create "phase-1" --color "fbca04" --description "Phase 1: Visual Style Refactoring" --force 2>/dev/null || true
gh label create "phase-2" --color "d93f0b" --description "Phase 2: Interaction Enhancement" --force 2>/dev/null || true

# Domain labels
gh label create "ui" --color "e99695" --description "UI/Frontend related" --force 2>/dev/null || true
gh label create "backend" --color "c2e0c6" --description "Backend related" --force 2>/dev/null || true
gh label create "animation" --color "f9d0c4" --description "Animation and effects" --force 2>/dev/null || true
gh label create "design" --color "fef2c0" --description "Design assets and styling" --force 2>/dev/null || true
gh label create "performance" --color "bfd4f2" --description "Performance optimization" --force 2>/dev/null || true

# Priority labels
gh label create "priority-p0" --color "b60205" --description "Critical priority" --force 2>/dev/null || true
gh label create "priority-p1" --color "d93f0b" --description "High priority" --force 2>/dev/null || true
gh label create "priority-p2" --color "fbca04" --description "Medium priority" --force 2>/dev/null || true
gh label create "priority-p3" --color "0e8a16" --description "Low priority" --force 2>/dev/null || true

# Size labels
gh label create "size-small" --color "c5def5" --description "1-2 hours" --force 2>/dev/null || true
gh label create "size-medium" --color "bfdadc" --description "2-3 hours" --force 2>/dev/null || true
gh label create "size-large" --color "d4c5f9" --description "3-4 hours" --force 2>/dev/null || true

echo "✓ Labels created successfully"

# Step 2: Create Milestones
echo ""
echo "Step 2: Creating Milestones..."
echo "----------------------------------------"

# Create Phase 1 Milestone
MILESTONE1=$(gh api repos/$REPO/milestones -f title="Phase 1: Visual Style Refactoring" -f description="Establish cyberpunk visual foundation with core visual upgrades. Includes Epic 1 (Cyberpunk Visual Style), Epic 2 (Particle Background), Epic 3 (3D Card Effects)." -f state=open --jq '.number' 2>/dev/null || echo "")

if [ -z "$MILESTONE1" ]; then
  # Milestone might already exist, try to get it
  MILESTONE1=$(gh api repos/$REPO/milestones --jq '.[] | select(.title=="Phase 1: Visual Style Refactoring") | .number' 2>/dev/null || echo "1")
fi

echo "✓ Phase 1 Milestone: #$MILESTONE1"

# Create Phase 2 Milestone
MILESTONE2=$(gh api repos/$REPO/milestones -f title="Phase 2: Interaction Enhancement & Character System" -f description="Add anime elements and interactive features. Includes Epic 4 (Anime Icons), Epic 5 (Kanban Musume Character)." -f state=open --jq '.number' 2>/dev/null || echo "")

if [ -z "$MILESTONE2" ]; then
  MILESTONE2=$(gh api repos/$REPO/milestones --jq '.[] | select(.title=="Phase 2: Interaction Enhancement & Character System") | .number' 2>/dev/null || echo "2")
fi

echo "✓ Phase 2 Milestone: #$MILESTONE2"

# Step 3: Create Epic Issues
echo ""
echo "Step 3: Creating Epic Issues..."
echo "=========================================="

# Epic 1: Cyberpunk Visual Style
echo ""
echo "Creating Epic 1: Cyberpunk Visual Style..."
EPIC1_BODY="## Epic Overview

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

This epic will be broken down into 10 tasks:

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
*This is an Epic issue. Individual tasks will be created as separate issues and linked to this epic.*"

EPIC1_URL=$(gh issue create \
  --title "[Epic 1] 赛博朋克视觉风格 (Cyberpunk Visual Style)" \
  --body "$EPIC1_BODY" \
  --label "epic,phase-1,ui,design,priority-p0" \
  --milestone "$MILESTONE1" 2>&1)

EPIC1_NUM=$(echo "$EPIC1_URL" | grep -oE '[0-9]+$')
echo "✓ Created Epic 1: #$EPIC1_NUM"

# Wait a bit to avoid rate limiting
sleep 2

echo ""
echo "=========================================="
echo "Epic Issues Created Successfully!"
echo "=========================================="
echo ""
echo "Epic 1 (Cyberpunk Visual Style): #$EPIC1_NUM"
echo ""
echo "Next Steps:"
echo "1. Review the created Epic issues"
echo "2. Run the task creation script to create individual tasks"
echo "3. Assign tasks to team members"
echo ""
echo "To create tasks for Epic 1, run:"
echo "  ./create_epic1_tasks.sh $EPIC1_NUM"
