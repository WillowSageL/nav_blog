# Quick Start Guide: Creating GitHub Issues

## Prerequisites

1. **GitHub CLI installed and authenticated**
   ```bash
   gh auth status
   ```

2. **Python 3.7+ installed** (for Python script)
   ```bash
   python3 --version
   ```

3. **Repository access**
   - Repository: WillowSageL/nav_blog
   - Permissions: Write access to create issues

## Option 1: Automated Creation (Recommended)

### Step 1: Run the Python Script

```bash
cd /Users/v_liangjiawei02/Desktop/导航页
python3 scripts/create_all_issues.py
```

This will:
- ✓ Create all 19 labels
- ✓ Create 2 milestones (Phase 1 & Phase 2)
- ✓ Create Epic 1 with 2 sample tasks
- ⚠️ Note: Currently creates Epic 1 only as a demonstration

### Step 2: Extend for All Epics

To create all 5 Epics with all ~50 tasks, you need to extend the script by adding:
- `create_epic_2()` and `create_epic_2_tasks()`
- `create_epic_3()` and `create_epic_3_tasks()`
- `create_epic_4()` and `create_epic_4_tasks()`
- `create_epic_5()` and `create_epic_5_tasks()`

Follow the pattern in `create_epic_1()` and `create_epic_1_tasks()`.

## Option 2: Manual Creation via Shell Script

### Step 1: Create Labels and Milestones

```bash
cd /Users/v_liangjiawei02/Desktop/导航页
./scripts/create_github_issues.sh
```

This creates:
- All 19 labels
- 2 milestones
- Epic 1 issue

### Step 2: Create Tasks Manually

Use the GitHub web interface or `gh` CLI to create individual tasks:

```bash
gh issue create \
  --title "[Epic 1-Task 1] Setup Tailwind CSS cyberpunk color palette" \
  --body "$(cat task_body.md)" \
  --label "feature,phase-1,ui,design,priority-p0,size-small" \
  --milestone 1
```

## Option 3: Use GitHub Web Interface

1. **Navigate to**: https://github.com/WillowSageL/nav_blog/issues

2. **Create Labels**: Settings → Labels → New label

3. **Create Milestones**: Issues → Milestones → New milestone

4. **Create Issues**: Issues → New issue
   - Use templates from `docs/github-issues-structure.md`
   - Copy/paste Epic and Task structures

## Verification

After running the scripts, verify:

```bash
# Check created labels
gh label list

# Check created milestones
gh api repos/WillowSageL/nav_blog/milestones --jq '.[] | {number, title}'

# Check created issues
gh issue list --limit 20

# Check specific epic
gh issue view <epic-number>
```

## Project Board Setup

### Create Project Board

```bash
# Create project
gh project create --title "nav_blog UI 升级" --body "Cyberpunk UI/UX upgrade project"

# Get project number
gh project list

# Add issues to project
gh project item-add <project-number> --owner WillowSageL --url https://github.com/WillowSageL/nav_blog/issues/<issue-number>
```

### Or use Web Interface

1. Go to: https://github.com/WillowSageL/nav_blog/projects
2. Click "New project"
3. Choose "Board" template
4. Name it "nav_blog UI 升级"
5. Add issues by clicking "+" and searching for issue numbers

## Troubleshooting

### Issue: "gh: command not found"

```bash
# Install GitHub CLI
# macOS
brew install gh

# Login
gh auth login
```

### Issue: "Permission denied"

```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

### Issue: "API rate limit exceeded"

```bash
# Check rate limit
gh api rate_limit

# Wait or use authenticated requests (already done if logged in)
```

### Issue: "Milestone not found"

```bash
# List milestones
gh api repos/WillowSageL/nav_blog/milestones --jq '.[] | {number, title}'

# Use the correct milestone number in scripts
```

## Next Steps

After creating issues:

1. **Review Issues**: Check all created issues on GitHub
2. **Organize Project Board**: Add issues to project board columns
3. **Assign Tasks**: Assign issues to team members
4. **Set Dependencies**: Link related issues
5. **Start Development**: Begin with Phase 1, Epic 1, Task 1

## Useful Commands

```bash
# List all issues with labels
gh issue list --label "epic"
gh issue list --label "phase-1"
gh issue list --label "priority-p0"

# View specific issue
gh issue view <issue-number>

# Edit issue
gh issue edit <issue-number> --add-label "in-progress"

# Close issue
gh issue close <issue-number>

# Create PR linked to issue
gh pr create --title "feat: ..." --body "Closes #<issue-number>"
```

## Documentation

- **Full Structure**: `docs/github-issues-structure.md`
- **PRD Document**: `docs/ui-ux-upgrade-cyberpunk-prd.md`
- **Scripts**: `scripts/create_all_issues.py`, `scripts/create_github_issues.sh`

## Support

For issues or questions:
1. Check `docs/github-issues-structure.md` for detailed breakdown
2. Review PRD for requirements clarification
3. Check GitHub Issues for existing discussions

---

*Last Updated: 2026-02-01*
