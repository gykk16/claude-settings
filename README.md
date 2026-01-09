# Claude Settings

Claude Code skills, commands, and coding rules.

## Why Claude Settings?

- **Consistent workflows** - Same standards for commits, PRs, and code reviews
- **18 ready-to-use skills** - No setup required
- **Install once, use everywhere** - Symlinks to ~/.claude/

## Quick Start

```bash
# 1. Clone or fork the repository
git clone https://github.com/gykk16/claude-settings.git
# or fork via GitHub and clone your fork
cd claude-settings

# 2. Install skills and commands
python scripts/manage-skills.py install

# 3. Use in any Claude Code session
/commit          # Create a git commit
/review          # Review code changes
/create-pr       # Create a pull request
```

## Features

### Skills

Custom skills for development workflows.

| Category | Skills |
|----------|--------|
| **Git Workflow** | `commit-changes`, `create-pull-request`, `create-branch-from-jira` |
| **Code Quality** | `code-review`, `software-engineer` |
| **Code Style** | `code-kotlin`, `code-typescript`, `code-java`, `code-spring`, `code-sql` |
| **Documentation** | `web-to-markdown`, `web-to-asciidoc`, `generate-api-document` |
| **Issue Tracking** | `create-jira-issue`, `create-github-issue` |

See [skills/README.md](skills/README.md) for the full list and usage examples.

### Commands

Shortcuts for common skills.

| Command | Description |
|---------|-------------|
| `/commit` | Create a git commit with Conventional Commits format |
| `/review` | Review code changes |
| `/create-pr` | Create a GitHub pull request |
| `/create-branch` | Create a feature branch from a Jira ticket |

## Project Structure

```
claude-settings/
├── skills/          # Custom skills (18 skills)
├── commands/        # Slash command shortcuts
├── rules/           # Coding style guides
├── templates/       # Reusable templates
├── scripts/         # Installation scripts
└── CLAUDE.md        # Project instructions
```

## Installation Options

### Global Installation (Recommended)

Install globally to `~/.claude/`:

```bash
python scripts/manage-skills.py install      # Install
python scripts/manage-skills.py status       # Check status
python scripts/manage-skills.py uninstall    # Uninstall
```

### Copy to Project

Copy to your project:

```bash
cp -r rules/ /path/to/your/project/
cp CLAUDE.md /path/to/your/project/
```

### Creating a New Skill

```bash
# 1. Copy the template
cp -r templates/skill-template.md skills/my-skill/SKILL.md

# 2. Edit the skill file
# 3. Run install to create symlinks
python scripts/manage-skills.py install
```

See [skills/README.md](skills/README.md) for the skill authoring guide.
