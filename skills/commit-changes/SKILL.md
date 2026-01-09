---
name: commit-changes
description: Creates git commits following Conventional Commits format with Jira ticket and GitHub issue integration. Analyzes changes, drafts commit message, and asks for user confirmation before committing. Use when user asks to commit changes.
---

# Committing Changes

$ARGUMENTS

## Instructions

> **⚠️ IMPORTANT: User confirmation is MANDATORY before creating any commit.**
> You MUST use `AskUserQuestion` tool in step 4 to get explicit user approval.
> NEVER commit without user confirmation.

1. **Analyze changes**
   - Run `git status` to see modified/new files
   - Run `git diff --staged` or `git diff` to understand the changes
   - Identify the type and scope of changes

2. **Extract Jira ticket and GitHub issue (if applicable)**
   - Check branch name for Jira ticket: `feature/TICKET-123-*`, `bugfix/TICKET-123-*`
   - Check branch name for GitHub issue: `feature/123-*`, `fix/123-*`, `issue-123-*`
   - Use `AskUserQuestion` to confirm ticket/issue numbers with user
   - Options: detected number, enter different number, or none

3. **Draft commit message**
   - Follow Conventional Commits format
   - Select appropriate type based on changes
   - Determine scope from affected module/component
   - Write clear, imperative description

4. **Ask user to confirm before committing (REQUIRED)**
   - **MUST use `AskUserQuestion` tool - NEVER skip this step**
   - Show changed files and proposed commit message
   - Use `AskUserQuestion` tool to get user approval
   - Options: Commit / Edit message / Cancel
   - **DO NOT proceed to step 5 without explicit user approval**

5. **Create commit**
   - **Only execute after user confirms in step 4**
   - Stage files if needed
   - Execute git commit with the approved message

---

## Commit Message Format

```
<type>(<scope>): <description> [TICKET-123]

[optional body]

[optional footer(s)]
```

---

## Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(cart): resolve quantity update issue` |
| `docs` | Documentation only | `docs: update API documentation` |
| `style` | Code style (formatting) | `style: apply ktlint formatting` |
| `refactor` | Code refactoring | `refactor(order): extract validation logic` |
| `perf` | Performance improvement | `perf(search): add query caching` |
| `test` | Adding/updating tests | `test(payment): add unit tests` |
| `build` | Build system/dependencies | `build: upgrade Spring Boot to 3.2` |
| `ci` | CI/CD configuration | `ci: add GitHub Actions workflow` |
| `chore` | Other changes | `chore: update .gitignore` |
| `revert` | Reverting a commit | `revert: feat(auth): add OAuth2 login` |

---

## Rules

### Do
- Use imperative mood: "add" not "added" or "adds"
- Keep subject line under 72 characters
- Capitalize first letter of description
- Include Jira ticket when applicable
- Separate subject from body with blank line

### Don't
- End subject line with period
- Use vague messages: "fix bug", "update code"
- Mix multiple changes in one commit

---

## Pre-Commit Confirmation (MANDATORY)

**⚠️ REQUIRED: You MUST use `AskUserQuestion` tool at two points - NEVER skip these:**

### 1. Confirm Ticket/Issue Reference

If Jira ticket or GitHub issue detected from branch name:

```markdown
**Detected from branch:** `feature/PROJ-123-add-feature`

**Jira Ticket:** PROJ-123
**GitHub Issue:** (none detected)
```

Use `AskUserQuestion` with options:
- `PROJ-123` - use detected Jira ticket
- `#456` - use GitHub issue number
- `None` - no ticket/issue reference
- Custom - enter different number

### 2. Confirm Commit (MUST ASK)

Show the user:
- Changed files list with status (modified/new/deleted)
- Proposed commit message

Use `AskUserQuestion` tool with options:
- "Commit" - proceed with the commit
- "Edit message" - let user modify the message
- "Cancel" - abort the commit

**DO NOT commit until user explicitly selects "Commit"**

### Example Output Before Asking

```markdown
**Changed Files:**
- path/to/file1.kt (modified)
- path/to/file2.kt (new file)
- path/to/file3.kt (deleted)

**Commit Message:**
<type>(<scope>): <description> [TICKET-123]

<body if needed>
```

---

## GitHub Issue Integration

### Extract from Branch Name

| Branch Pattern | Extracted Issue |
|----------------|-----------------|
| `feature/123-add-feature` | `#123` |
| `fix/456-fix-bug` | `#456` |
| `issue-789-description` | `#789` |

### Verify Issue Exists

```bash
gh issue view 123 --json number,title,state
```

### Issue Reference in Footer

```
feat(auth): add OAuth2 login

Implement OAuth2 authentication flow.

Closes #123
```

### Multiple References

```
fix(cart): resolve quantity sync issue

Fixes #123
Refs #456
```

---

## Jira Ticket Integration

### Extract from Branch Name

| Branch Pattern | Extracted Ticket |
|----------------|------------------|
| `feature/PROJ-123-add-feature` | `[PROJ-123]` |
| `bugfix/PROJ-456-fix-bug` | `[PROJ-456]` |
| `hotfix/PROJ-789-urgent` | `[PROJ-789]` |

### Ticket Placement

**In Subject (Preferred)**
```
feat(order): implement cancellation flow [PROJ-123]
```

**In Footer (Alternative)**
```
feat(order): implement cancellation flow

Refs: PROJ-123
```

---

## Examples

### Feature with Jira Ticket

```
feat(flight): add fare search caching [PROJ-123]

Implement Redis caching for fare search results
to reduce external API calls.

- Cache TTL: 5 minutes
- Cache key: origin_destination_date
```

### Bug Fix

```
fix(order): prevent duplicate order creation [PROJ-456]

Add idempotency check using order reference ID.
```

### Simple Changes

```
docs: update API documentation

refactor(booking): extract validation logic

test(fare): add unit tests for price calculator

chore: update gradle dependencies
```

### Breaking Change

```
feat(api)!: change response format for v2 [PROJ-789]

BREAKING CHANGE: Response wrapper structure changed.
Old: { data: {...} }
New: { result: {...}, meta: {...} }
```
