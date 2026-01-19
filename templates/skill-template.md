---
name: your-skill-name
description: What this skill does and when to use it. Include specific keywords for agent identification.
# Optional fields (uncomment as needed):
# license: Apache-2.0
# compatibility: Requires git, docker, jq
# metadata:
#   author: your-name
#   version: "1.0"
# allowed-tools: Bash(git:*) Read
---

# Your Skill Name

Brief overview of what this skill does.

## Instructions

[Clear, step-by-step guidance for Claude to follow]

1. First step
2. Second step
3. Third step

## Examples

[Concrete input/output examples]

**Input:**
```
[Example user request]
```

**Output:**
```
[Example response or action]
```

## Workflow (optional)

[Checklist for complex tasks - copy and track progress]

- [ ] Step 1: Analyze input
- [ ] Step 2: Validate requirements
- [ ] Step 3: Execute main task
- [ ] Step 4: Verify output

## References (optional)

For detailed information, see:
- [references/REFERENCE.md](references/REFERENCE.md)

<!--
================================================================================
SKILL AUTHORING GUIDE
================================================================================

## Directory Structure

your-skill-name/
├── SKILL.md          # Required: this file (rename from skill-template.md)
├── scripts/          # Optional: executable code
├── references/       # Optional: additional documentation
└── assets/           # Optional: templates, images, data files

## Frontmatter Field Rules

### name (required)
- Max 64 characters
- Lowercase letters, numbers, hyphens only
- No leading/trailing/consecutive hyphens
- Must match parent directory name

### description (required)
- Max 1024 characters
- Write in third person
- Include WHAT it does AND WHEN to use it
- Add specific keywords for agent identification

Good: "Extracts text from PDF files. Use when working with PDFs or document extraction."
Bad: "Helps with PDFs." (too vague)

### license (optional)
- License name (e.g., Apache-2.0, MIT) or reference to bundled file

### compatibility (optional)
- Max 500 characters
- Environment requirements (tools, packages, network access)

### metadata (optional)
- Arbitrary key-value string mapping
- Common keys: author, version, tags

### allowed-tools (optional, experimental)
- Space-delimited pre-approved tools list
- Example: Bash(git:*) Bash(jq:*) Read

## Best Practices

1. Keep SKILL.md under 500 lines
2. Move detailed content to references/ directory
3. Use relative paths for file references
4. Include concrete examples with input/output
5. Add workflows with checklists for complex tasks

## Progressive Disclosure

Optimize context usage:
- Metadata (~100 tokens): Loaded at startup
- Instructions (<5000 tokens): Loaded when skill activates
- Resources (as needed): Loaded on demand

For more details, see: https://agentskills.io/specification
================================================================================
-->
