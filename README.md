# Claude Settings

A collection of Claude Code configuration templates, rules, skills, and commands.

## Overview

This repository provides reusable configurations for Claude Code to maintain consistent coding standards and workflows across projects.

## Structure

```
claude-settings/
├── .claude/
│   ├── settings.json       # Project settings
│   └── settings.local.json # Local overrides (gitignored)
├── commands/               # Slash commands (shortcuts)
│   └── commit.md
├── rules/                  # Coding style guides
│   ├── kotlin.md
│   ├── typescript.md
│   └── commit.md
├── skills/                 # Custom skills (16 skills)
│   ├── code-review/
│   ├── commit-changes/
│   ├── create-branch-from-jira/
│   ├── create-pull-request/
│   └── ...
├── templates/              # Reusable templates
│   ├── skill-template.md
│   ├── commit-template.md
│   └── pr-template.md
└── CLAUDE.md               # Project instructions
```

## Rules

Language-specific style guides emphasizing clean, readable code.

| Language | File | Based On |
|----------|------|----------|
| Kotlin | `rules/kotlin.md` | [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html) |
| TypeScript | `rules/typescript.md` | [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) |

### Core Principles

- Write human-readable, clean code
- Follow OOP, SOLID, and functional principles pragmatically
- **Do not over-engineer** - simple is best
- Do not duplicate code - write reusable code

## Skills

Custom skills for Claude Code automation.

| Skill | Description |
|-------|-------------|
| `software-engineer` | Senior engineer guidance using coding and review skills |
| `code-review` | Comprehensive code review with structured output format |
| `commit-changes` | Create git commits following Conventional Commits with Jira integration |
| `create-branch-from-jira` | Create git feature branches from Jira tickets |
| `create-pull-request` | Create GitHub pull requests with Jira ticket integration |
| `create-jira-issue` | Create Jira issues from user-provided context |
| `create-github-issue` | Create GitHub issues with repo labels and Jira integration |
| `code-typescript` | TypeScript development following Google TypeScript Style Guide |
| `code-kotlin` | Kotlin development following Kotlin Coding Conventions |
| `web-to-markdown` | Convert web pages to clean, well-structured markdown files |
| `web-to-asciidoc` | Convert web pages to clean, well-structured AsciiDoc files |
| `generate-api-document` | Generate API spec documents in AsciiDoc from controller code |
| `technical-writing` | Complete technical writing process through 3 sequential steps |
| `determine-document-type` | Step 1: Recommend appropriate document type based on goals |
| `structure-documentation` | Step 2: Guide information architecture for documents |
| `refine-sentences` | Step 3: Refine sentences for clarity and natural Korean |

### Git Workflow Skills

```
/create-branch-from-jira  → Create feature branch from Jira ticket
/commit-changes           → Commit with Conventional Commits format
/create-pull-request      → Create PR with Jira integration
```

### Technical Writing Workflow

```
/technical-writing
    ├── Step 1: /determine-document-type
    ├── Step 2: /structure-documentation
    └── Step 3: /refine-sentences
```

### Creating a New Skill

1. Copy `templates/skill-template.md`
2. Create folder in `skills/` with skill name
3. Name the file `SKILL.md`

```
skills/
└── my-skill/
    └── SKILL.md
```

## Commands

Slash commands are simple shortcuts for frequently used prompts.

| Command | Description |
|---------|-------------|
| `commit` | Create a git commit using the commit-changes skill |

### Commands vs Skills

| Aspect | Commands | Skills |
|--------|----------|--------|
| **Structure** | Single `.md` file | Directory with `SKILL.md` |
| **Complexity** | Simple prompts | Complex workflows |
| **Use case** | Quick shortcuts | Multi-step processes |

See `commands/README.md` for detailed guide.

## Templates

| Template | Description |
|----------|-------------|
| `skill-template.md` | Template for creating new skills |
| `commit-template.md` | [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format |
| `pr-template.md` | Pull request template with checklist |

## Usage

### Copy to Your Project

```bash
# Copy rules to your project
cp -r rules/ /path/to/your/project/

# Copy CLAUDE.md
cp CLAUDE.md /path/to/your/project/
```

### Use as Reference

Reference these files in your project's `CLAUDE.md`:

```markdown
## Coding Standards

Follow the Kotlin style guide: [link to rules/kotlin.md]
```

