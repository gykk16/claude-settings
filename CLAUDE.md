# Project Instructions

## Overview

This repository contains Claude Code configuration templates, rules, and skills.

## Guidelines

> **⚠️ Always check for appropriate skills before starting a task**
- Follow consistent formatting in all configuration files
- Document all custom skills with usage examples
- Keep rules focused and actionable

## Writing Code

Key principles across all languages:

- Write human-readable, clean code
- Follow OOP, SOLID, and functional principles pragmatically
- **Do not over-engineer** - simple is best
- Do not duplicate code - write reusable code
- Apply best practices flexibly based on context

## Installing Skills

Install skills and commands to `~/.claude/` using the cross-platform script:

```bash
# Install all skills and commands
python scripts/manage-skills.py install

# Check installation status
python scripts/manage-skills.py status

# Uninstall all skills and commands
python scripts/manage-skills.py uninstall
```

**Options:**
- `install -y`: Skip confirmation prompts
- Supports Windows, macOS, and Linux

## Creating New Skills

When creating a new skill:

1. **Use the template**: Copy from `templates/skill-template.md`
2. **Create a folder**: Create a new folder in `skills/` with the skill name
3. **Name the file**: The skill file must be named `SKILL.md`

### Folder Structure

```
skills/
└── skill-name/
    ├── SKILL.md          # Required: main instructions
    ├── REFERENCE.md      # Optional: detailed reference
    └── EXAMPLES.md       # Optional: usage examples
```

### YAML Frontmatter Requirements

```yaml
---
name: your-skill-name
description: What this Skill does and when Claude should use it.
---
```

**`name` field:**
- Max 64 characters
- Lowercase letters, numbers, hyphens only
- Use imperative form: `review-code`, `process-pdfs`
- Cannot contain: "anthropic", "claude"

**`description` field:**
- Max 1024 characters
- Write in **third person**
- Include **what** it does AND **when** to use it

### Authoring Best Practices

1. **Be concise** - Claude is smart, only add context it doesn't have
2. **Keep under 500 lines** - Use separate files for details
3. **Provide examples** - Concrete input/output pairs
4. **Add workflows** - Checklists for complex tasks

See `skills/README.md` for detailed authoring guide.
