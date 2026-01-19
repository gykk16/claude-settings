# Skills

Custom skills for Claude Code automation.

## What are Skills?

**Agent Skills** are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows. They enable agents to perform specific tasks with domain expertise.

At its core, a skill is a **folder containing a `SKILL.md` file** with YAML frontmatter and Markdown instructions.

### How Skills Work: Progressive Disclosure

Skills use a progressive disclosure pattern to manage context efficiently:

1. **Discovery**: At startup, agents load only the `name` and `description` of each available skill—just enough to know when it might be relevant.
2. **Activation**: When a task matches a skill's description, the agent reads the full `SKILL.md` instructions into context.
3. **Execution**: The agent follows the instructions, optionally loading referenced files or executing bundled code as needed.

### Key Advantages

- **Self-documenting**: Both authors and users can read and understand what it does
- **Extensible**: From simple text instructions to complex packages with executable code
- **Portable**: Just files—easy to edit, version control, and share

This guide follows the [Agent Skills Specification](https://agentskills.io/specification).

## Available Skills

| Skill | Description |
|-------|-------------|
| `software-engineer` | Senior engineer guidance using coding and review skills |
| `deep-dive-plan` | Multi-agent collaborative planning system for comprehensive pre-implementation analysis |
| `code-review` | Comprehensive code review with structured output format |
| `commit-changes` | Create git commits following Conventional Commits format with Jira integration |
| `create-branch-from-jira` | Create git feature branches from Jira tickets |
| `create-pull-request` | Create GitHub pull requests with Jira ticket integration |
| `create-jira-issue` | Create Jira issues from user-provided context |
| `create-github-issue` | Create GitHub issues with repo labels and Jira integration |
| `code-typescript` | TypeScript development following Google TypeScript Style Guide |
| `code-kotlin` | Kotlin development following Kotlin Coding Conventions |
| `code-java` | Java development following comprehensive best practices and style guide |
| `web-to-markdown` | Convert web pages to clean, well-structured markdown files |
| `web-to-asciidoc` | Convert web pages to clean, well-structured AsciiDoc files |
| `generate-api-document` | Generate API spec documents in AsciiDoc from controller code |
| `technical-writing` | Complete technical writing process through 3 sequential steps |
| `determine-document-type` | Step 1: Recommend appropriate document type based on goals and context |
| `structure-documentation` | Step 2: Guide information architecture for technical documents |
| `refine-sentences` | Step 3: Refine sentences for clarity, conciseness, and natural Korean |

## Installing Skills

Skills are installed to `~/.claude/skills/`. Choose one of the following methods:

### Option 1: Use Install Script (Recommended)

Cross-platform script that creates symlinks for all skills and commands.

```bash
# Clone the repository
git clone https://github.com/your-username/claude-settings.git
cd claude-settings

# Install all skills and commands
python scripts/manage-skills.py install

# Check installation status
python scripts/manage-skills.py status

# Uninstall all skills and commands
python scripts/manage-skills.py uninstall
```

**Options:**
```bash
python scripts/manage-skills.py install -y  # Skip confirmation prompts
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

### Directory Structure

Minimal skill structure:

```
skill-name/
└── SKILL.md          # Required
```

Full structure with optional directories:

```
skill-name/
├── SKILL.md          # Required: main instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: additional documentation
└── assets/           # Optional: static resources (templates, images, data)
```

### Use the Template

Copy from `templates/skill-template.md` and customize.

### YAML Frontmatter

#### Required Fields

```yaml
---
name: skill-name
description: What this skill does and when to use it.
---
```

#### Optional Fields

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
compatibility: Requires git, docker, jq, and access to the internet
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

### Field Specifications

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | Max 64 chars. Lowercase letters, numbers, hyphens only. No leading/trailing/consecutive hyphens. Must match parent directory. |
| `description` | Yes | Max 1024 chars. Non-empty. Describe what it does and when to use it. |
| `license` | No | License name or reference to bundled file |
| `compatibility` | No | Max 500 chars. Environment requirements (product, packages, network access) |
| `metadata` | No | Arbitrary key-value string mapping |
| `allowed-tools` | No | Space-delimited pre-approved tools list (Experimental) |

### Name Field Rules

**Valid examples:**
```yaml
name: pdf-processing
name: data-analysis
name: code-review
```

**Invalid examples:**
```yaml
name: PDF-Processing      # uppercase not allowed
name: -pdf                # cannot start with hyphen
name: pdf--processing     # consecutive hyphens not allowed
```

### Description Field

Should include:
- What the skill does
- When to use it
- Specific keywords for agent identification

**Good examples:**
```yaml
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```
```yaml
description: Performs comprehensive code reviews focusing on quality, security, and performance. Use when reviewing pull requests or code changes.
```

**Bad examples:**
```yaml
description: Helps with PDFs.           # Too vague, no trigger context
description: I review your code         # Wrong person (use third person)
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

Skills should optimize context usage with three tiers:

1. **Metadata** (~100 tokens): Name and description loaded at startup
2. **Instructions** (<5000 tokens recommended): Full SKILL.md body loaded when skill activates
3. **Resources** (as needed): Scripts, references, assets loaded on demand

For complex skills, split content into separate files:

```
skill-name/
├── SKILL.md              # Main instructions (loaded when triggered)
├── references/
│   └── REFERENCE.md      # Detailed reference (loaded as needed)
├── scripts/
│   └── utility.py        # Executable scripts
└── assets/
    └── template.json     # Static resources
```

Reference in SKILL.md using relative paths:

```markdown
**Advanced features**: See [references/REFERENCE.md](references/REFERENCE.md)
**Run script**: `scripts/extract.py`
```

### Optional Directories

#### scripts/
Executable code files (Python, Bash, JavaScript, etc.)
- Must be self-contained or document dependencies
- Include helpful error messages
- Handle edge cases gracefully

#### references/
Additional documentation loaded on demand:
- `REFERENCE.md` - Technical reference
- Domain-specific files (`finance.md`, `legal.md`, etc.)

Keep files focused for efficient context usage.

#### assets/
Static resources:
- Templates (document, configuration)
- Images (diagrams, examples)
- Data files (lookup tables, schemas)

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

## Validation

Use the skills-ref reference library to validate your skill:

```bash
skills-ref validate ./my-skill
```

This checks SKILL.md frontmatter validity and naming convention compliance.

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

- [Agent Skills Specification](https://agentskills.io/specification)
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Skill authoring best practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
