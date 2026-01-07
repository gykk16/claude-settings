# Commands

Custom slash commands for Claude Code.

## What are Commands?

Commands are single Markdown files that define frequently used prompts. Unlike skills (which are directories with multiple files), commands are simple `.md` files invoked explicitly with `/command-name`.

## Available Commands

| Command | Skill | Description |
|---------|-------|-------------|
| `commit` | commit-changes | Create a git commit |
| `review` | code-review | Review code changes |
| `create-pr` | create-pull-request | Create a GitHub pull request |
| `create-jira` | create-jira-issue | Create a Jira issue |
| `create-issue` | create-github-issue | Create a GitHub issue |
| `create-branch` | create-branch-from-jira | Create a feature branch from a Jira ticket |

## Installing Commands

Commands are installed to `~/.claude/commands/`. Choose one of the following methods:

### Option 1: Symbolic Link (Recommended)

Best for development or when you want commands to auto-update with the repo.

```bash
# Clone the repository
git clone https://github.com/your-username/claude-settings.git
cd claude-settings

# Create symlinks for all commands
REPO_COMMANDS="$(pwd)/commands"
CLAUDE_COMMANDS="$HOME/.claude/commands"

mkdir -p "$CLAUDE_COMMANDS"

for cmd in "$REPO_COMMANDS"/*.md; do
  [ -f "$cmd" ] || continue
  cmd_name=$(basename "$cmd")
  [[ "$cmd_name" == "README.md" ]] && continue
  rm -f "$CLAUDE_COMMANDS/$cmd_name"
  ln -s "$cmd" "$CLAUDE_COMMANDS/$cmd_name"
  echo "Linked: $cmd_name"
done
```

### Option 2: Copy Files

Best for stable, standalone installation.

```bash
# Clone the repository
git clone https://github.com/your-username/claude-settings.git
cd claude-settings

# Copy all commands (excluding README)
mkdir -p ~/.claude/commands
for cmd in commands/*.md; do
  [[ "$(basename "$cmd")" == "README.md" ]] && continue
  cp "$cmd" ~/.claude/commands/
done
```

### Verify Installation

```bash
ls -la ~/.claude/commands/
```

---

## Creating a New Command

### 1. Create the File

```
commands/
└── your-command.md
```

### 2. Basic Structure

```markdown
---
description: Brief description of what this command does
---

Your prompt text here.
```

### 3. YAML Frontmatter

```yaml
---
description: Brief description (shown in command list)
---
```

---

## Command Features

### Arguments

**Using `$ARGUMENTS` (all arguments):**

```markdown
---
description: Fix an issue by number
---

Fix issue #$ARGUMENTS following our coding standards.
```

Usage: `/fix-issue 123`

**Using positional arguments (`$1`, `$2`, etc.):**

```markdown
---
description: Review pull request
argument-hint: [pr-number] [priority]
---

Review PR #$1 with priority $2.
```

Usage: `/review-pr 456 high`

### Bash Command Execution

Prefix with `!` to execute bash commands:

```markdown
---
description: Commit with context
---

## Context

- Current git status: !`git status`
- Current git diff: !`git diff HEAD`

## Task

Create a commit based on the above changes.
```

### File References

Use `@` prefix to reference files:

```markdown
Review the implementation in @src/utils/helpers.js
```

### Invoking Skills

Reference skills in your command:

```markdown
---
description: Quick commit
---

Use the `/commit-changes` skill to create a git commit.

$ARGUMENTS
```

---

## Commands vs Skills

| Aspect | Commands | Skills |
|--------|----------|--------|
| **Structure** | Single `.md` file | Directory with `SKILL.md` |
| **Location** | `commands/` or `~/.claude/commands/` | `skills/` or `~/.claude/skills/` |
| **Complexity** | Simple prompts | Complex workflows |
| **Use case** | Quick shortcuts, simple tasks | Multi-step processes, reference docs |

### When to Use Commands

- Quick, frequently used prompts
- Shortcuts to invoke skills
- Simple one-liner tasks
- Personal workflow shortcuts

### When to Use Skills

- Complex workflows with multiple steps
- Tasks requiring reference documentation
- Team-standardized processes
- Capabilities with scripts or utilities

---

## Resources

- [Slash Commands Documentation](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Common Workflows](https://docs.anthropic.com/en/docs/claude-code/common-workflows)
