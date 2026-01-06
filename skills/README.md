# Skills

Custom skills for Claude Code automation.

## What are Skills?

Skills are folders of instructions that Claude loads dynamically to improve performance on specialized tasks. Each skill requires a `SKILL.md` file with YAML frontmatter and instructions.

## Available Skills

| Skill | Description |
|-------|-------------|
| `code-review` | Comprehensive code review with structured output format |
| `committing-changes` | Create git commits following Conventional Commits format with Jira integration |
| `creating-branch-from-jira` | Create git feature branches from Jira tickets |
| `creating-pull-request` | Create GitHub pull requests with Jira ticket integration |
| `creating-jira-issue` | Create Jira issues from user-provided context |
| `creating-github-issue` | Create GitHub issues with repo labels and Jira integration |
| `coding-typescript` | TypeScript development following Google TypeScript Style Guide |
| `coding-kotlin` | Kotlin development following Kotlin Coding Conventions |
| `web-to-markdown` | Convert web pages to clean, well-structured markdown files |
| `web-to-asciidoc` | Convert web pages to clean, well-structured AsciiDoc files |
| `generate-api-document` | Generate API spec documents in AsciiDoc from controller code |
| `technical-writing` | Complete technical writing process through 3 sequential steps |
| `determining-document-type` | Step 1: Recommend appropriate document type based on goals and context |
| `structuring-documentation` | Step 2: Guide information architecture for technical documents |
| `refining-sentences` | Step 3: Refine sentences for clarity, conciseness, and natural Korean |

## Installing Skills

Skills are installed to `~/.claude/skills/`. Choose one of the following methods:

### Option 1: Symbolic Link (Recommended)

Best for development or when you want skills to auto-update with the repo.

```bash
# Clone the repository
git clone https://github.com/your-username/claude-settings.git
cd claude-settings

# Create symlinks for all skills
REPO_SKILLS="$(pwd)/skills"
CLAUDE_SKILLS="$HOME/.claude/skills"

for skill in "$REPO_SKILLS"/*/; do
  skill_name=$(basename "$skill")
  rm -rf "$CLAUDE_SKILLS/$skill_name"  # Remove if exists
  ln -s "$skill" "$CLAUDE_SKILLS/$skill_name"
  echo "Linked: $skill_name"
done
```

### Option 2: Copy Files

Best for stable, standalone installation.

```bash
# Clone the repository
git clone https://github.com/your-username/claude-settings.git
cd claude-settings

# Copy all skills
cp -r skills/*/ ~/.claude/skills/
```

### Verify Installation

```bash
ls -la ~/.claude/skills/
```

---

## Creating a New Skill

### 1. Create Folder Structure

```
skills/
└── your-skill-name/
    └── SKILL.md
```

### 2. Use the Template

Copy from `templates/skill-template.md` and customize.

### 3. YAML Frontmatter Requirements

```yaml
---
name: your-skill-name
description: What this Skill does and when Claude should use it.
---
```

#### `name` field:
- Maximum 64 characters
- Lowercase letters, numbers, and hyphens only
- Use gerund form (verb + -ing): `reviewing-code`, `processing-pdfs`
- Cannot contain: XML tags, "anthropic", "claude"

#### `description` field:
- Maximum 1024 characters
- Must be non-empty
- Write in **third person** (not "I can help" or "You can use")
- Include **what** it does AND **when** to use it

**Good examples:**
```yaml
description: Performs comprehensive code reviews focusing on quality, security, and performance. Use when reviewing pull requests or code changes.
```
```yaml
description: Generates commit messages following Conventional Commits spec. Use when the user asks for help writing commit messages.
```

**Bad examples:**
```yaml
description: Helps with code  # Too vague, no trigger context
description: I review your code  # Wrong person
```

---

## Skill Authoring Best Practices

### Core Principles

1. **Concise is Key**
   - Claude is already smart - only add context it doesn't have
   - Challenge each piece: "Does Claude really need this?"
   - Every token competes with conversation history

2. **Set Appropriate Freedom**
   - High freedom: Text instructions for tasks with multiple valid approaches
   - Medium freedom: Templates when a preferred pattern exists
   - Low freedom: Specific scripts for fragile operations

3. **Keep Under 500 Lines**
   - Use progressive disclosure - reference separate files for details
   - Keep references one level deep from SKILL.md

### Structure Guidelines

```markdown
---
name: skill-name
description: What and when.
---

# Skill Name

## Instructions
[Clear, step-by-step guidance]

## Examples
[Concrete input/output examples]

## Workflow (optional)
[Checklist for complex tasks]
```

### Progressive Disclosure

For complex skills, split content into separate files:

```
skill-name/
├── SKILL.md              # Main instructions (loaded when triggered)
├── REFERENCE.md          # Detailed reference (loaded as needed)
├── EXAMPLES.md           # Usage examples (loaded as needed)
└── scripts/
    └── utility.py        # Executable scripts
```

Reference in SKILL.md:
```markdown
**Advanced features**: See [REFERENCE.md](REFERENCE.md)
**Examples**: See [EXAMPLES.md](EXAMPLES.md)
```

### Workflows with Checklists

For complex tasks, provide checkable progress:

```markdown
## Workflow

Copy this checklist and track progress:

- [ ] Step 1: Analyze input
- [ ] Step 2: Validate data
- [ ] Step 3: Process
- [ ] Step 4: Verify output
```

### Feedback Loops

Include validation steps for quality-critical operations:

```markdown
1. Make changes
2. Run validation: `python validate.py`
3. If validation fails, fix and repeat step 2
4. Only proceed when validation passes
```

---

## Anti-Patterns to Avoid

| Avoid | Instead |
|-------|---------|
| Time-sensitive info ("after Aug 2025...") | Use "old patterns" section |
| Inconsistent terminology | Pick one term, use throughout |
| Too many options | Provide a default with escape hatch |
| Windows paths (`\`) | Use forward slashes (`/`) |
| Deeply nested references | Keep references one level deep |
| Vague descriptions | Be specific with trigger contexts |

---

## Resources

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Skill authoring best practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
