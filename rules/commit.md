# Commit Convention

Based on [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### With Jira Ticket

```
<type>(<scope>): <description> [TICKET-123]

[optional body]

[optional footer(s)]
```

---

## Commit Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Code style (formatting, missing semicolons, etc.) |
| `refactor` | Code refactoring (no feature change, no bug fix) |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Build system or dependencies |
| `ci` | CI/CD configuration |
| `chore` | Other changes (e.g., scripts, configs) |
| `revert` | Reverting a previous commit |

---

## Examples

### Feature with Jira Ticket

```
feat(flight): add fare search caching [TICKET-123]

Implement Redis caching for fare search results
to reduce external API calls.

- Cache TTL: 5 minutes
- Cache key: origin_destination_date
```

### Bug Fix

```
fix(order): prevent duplicate order creation [TICKET-123]

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
feat(api)!: change response format for v2 [TICKET-123]

BREAKING CHANGE: Response wrapper structure changed.
Old: { data: {...} }
New: { result: {...}, meta: {...} }
```

---

## Scope Examples

| Module | Scope |
|--------|-------|
| mars-mrt-app | `mrt`, `order`, `booking` |
| mars-flight-app-service | `flight`, `fare`, `search` |
| mars-ai-app | `ai`, `assistant` |
| domain | `entity`, `repository` |
| core modules | `core`, `mvc`, `http` |

---

## Rules

### Do

- **Always ask user to confirm commit message and changed files before committing**
- Use imperative mood: "add" not "added" or "adds"
- Keep subject line under 72 characters
- Capitalize first letter of description
- Include Jira ticket when applicable
- Separate subject from body with blank line

### Don't

- End subject line with period
- Use vague messages: "fix bug", "update code"
- Mix multiple changes in one commit
- Commit without testing

### Pre-Commit Confirmation Template

Before committing, show user the following:

```
**Changed Files:**
- path/to/file1.kt (modified)
- path/to/file2.kt (new file)

**Commit Message:**
<type>(<scope>): <description> [TICKET-123]

Proceed with commit?
```

---

## Jira Ticket Integration

### Extract from Branch Name

When working on a feature branch, extract the ticket from branch name:

```
feature/TICKET-123-add-fare-cache  →  [TICKET-123]
bugfix/TICKET-123-fix-order-bug    →  [TICKET-123]
hotfix/TICKET-123-urgent-fix       →  [TICKET-123]
```

### Ticket in Subject (Preferred)

```
feat(order): implement cancellation flow [TICKET-123]
```

### Ticket in Footer (Alternative)

```
feat(order): implement cancellation flow

Implements full cancellation flow with refund calculation.

Refs: TICKET-123
```

### Multiple Tickets

```
feat(booking): add multi-passenger support [TICKET-123]

Refs: TICKET-123, TICKET-456
```

---

## Quick Reference

```bash
# Feature
git commit -m "feat(scope): description [TICKET-XXX]"

# Bug fix
git commit -m "fix(scope): description [TICKET-XXX]"

# Documentation
git commit -m "docs: description"

# Refactoring
git commit -m "refactor(scope): description"

# Tests
git commit -m "test(scope): description"
```
