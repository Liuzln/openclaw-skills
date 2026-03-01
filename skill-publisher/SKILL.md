---
name: skill-publisher
description: Publish and share OpenClaw skills to GitHub repositories. Use when the user wants to share skills, create a skills collection repository, add skills to an existing repository, or manage skill sharing workflows. Automates repository creation, skill addition, README updates, and git operations.
---

# Skill Publisher

Publish and share OpenClaw skills to GitHub repositories with automated repository management.

## Quick Start

### Initialize a new skills repository

```bash
python3 scripts/init_repo.py <repo-name> [repo-path]
```

Example:
```bash
python3 scripts/init_repo.py openclaw-skills
```

This will:
- Create repository directory
- Generate README.md
- Initialize git
- Create public GitHub repository
- Push initial commit

### Add a skill to the repository

```bash
python3 scripts/add_skill.py <skill-path> [repo-path]
```

Example:
```bash
python3 scripts/add_skill.py ~/.openclaw/workspace/skills/my-skill
```

This will:
- Copy skill to repository
- Update README.md with skill entry
- Git add, commit, and push
- Display GitHub URL

## Workflows

### First-time setup

1. **Initialize repository:**
   ```bash
   python3 scripts/init_repo.py openclaw-skills
   ```

2. **Add your first skill:**
   ```bash
   python3 scripts/add_skill.py ~/.openclaw/workspace/skills/agent-creator
   ```

3. **Share the repository URL** with others

### Adding more skills

Simply run:
```bash
python3 scripts/add_skill.py <path-to-skill>
```

The script will:
- Copy the skill
- Update README automatically
- Commit and push to GitHub

## Default Paths

- **Repository location:** `~/.openclaw/workspace/<repo-name>`
- **Skills source:** `~/.openclaw/workspace/skills/`

You can override these with command-line arguments.

## README Management

The `add_skill.py` script automatically updates README.md:

- Extracts skill name and description from SKILL.md frontmatter
- Adds entry under "## 📚 技能列表" section
- Creates link to skill directory
- Avoids duplicates

Example entry:
```markdown
### [agent-creator](./agent-creator/)

Create and configure new OpenClaw agents with Telegram bot integration.
```

## Requirements

- `gh` CLI installed and authenticated
- Git configured
- GitHub account

## Troubleshooting

**Repository already exists:**
- Choose a different name
- Or use existing repository path with `add_skill.py`

**GitHub authentication failed:**
- Run `gh auth login` first
- Verify GitHub CLI is installed

**Skill not found in README:**
- Ensure SKILL.md has proper YAML frontmatter
- Check that `name` and `description` fields exist

**Git push failed:**
- Check network connection
- Verify GitHub authentication
- Try manual push: `cd <repo-path> && git push`

## Best Practices

1. **Test skills before publishing** - Ensure they work correctly
2. **Write clear descriptions** - Help others understand what the skill does
3. **Include examples** - Show how to use the skill
4. **Keep README updated** - The script does this automatically
5. **Use semantic commit messages** - The script generates these

## Repository Structure

```
openclaw-skills/
├── README.md              # Auto-generated, auto-updated
├── skill-1/
│   ├── SKILL.md
│   ├── scripts/
│   └── assets/
├── skill-2/
│   └── SKILL.md
└── ...
```

Each skill is a self-contained directory with its own SKILL.md and resources.
