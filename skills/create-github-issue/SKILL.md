---
name: create-github-issue
description: Creates a GitHub issue from user-provided context. Suggests repo labels and uses AskUserQuestion for assignees, labels, and milestone. Adds Jira ticket info if applicable. Use when user wants to create a GitHub issue.
---

# Creating GitHub Issue

$ARGUMENTS

## Instructions

> **⚠️ IMPORTANT: User confirmation is MANDATORY before creating any issue.**
> You MUST use `AskUserQuestion` tool in step 4 to get explicit user approval.
> NEVER create an issue without user confirmation.

1. **Analyze user context**
   - Extract key information from user's description
   - Identify potential title and body content
   - Check for Jira ticket references in context or branch name

2. **Fetch repository labels**
   - Run `gh label list` to get available labels
   - Suggest appropriate labels based on issue context

3. **Draft issue content**
   - Generate concise title
   - Create detailed body with context
   - Include Jira ticket link if applicable

4. **Ask user to confirm issue details (REQUIRED)**
   - **MUST use `AskUserQuestion` tool - NEVER skip this step**
   - Show drafted title and body first
   - Use `AskUserQuestion` tool to select:
     - Labels (from repo labels)
     - Assignees
     - Milestone (if available)
   - Final confirmation: Create / Edit / Cancel
   - **DO NOT proceed to step 5 without explicit user approval**

5. **Create the issue**
   - **Only execute after user confirms in step 4**
   - Use `gh issue create` command
   - Return the created issue URL

---

## Pre-Creation Confirmation (MANDATORY)

**⚠️ REQUIRED: You MUST use `AskUserQuestion` tool to confirm ALL issue details before creating:**

### Step 1: Fetch Available Labels

```bash
gh label list --json name,description --limit 50
```

### Step 2: Show Draft and Ask for Confirmation

```markdown
## New GitHub Issue

**Title:** Add dark mode support

**Body:**
Implement dark mode toggle for the application.

## Requirements
- Add theme toggle in settings
- Persist user preference
- Support system preference detection

## Related
- Jira: [PROJ-123](https://jira.example.com/browse/PROJ-123)

---

**Available Labels:** bug, enhancement, documentation, good first issue, help wanted
**Available Milestones:** v1.0, v1.1, v2.0
```

### Step 3: AskUserQuestion Options (ALL REQUIRED)

You MUST ask user for ALL of the following using `AskUserQuestion` tool:

1. **Labels** (multiSelect: true)
   - Suggest relevant labels from repo
   - Common: `bug`, `enhancement`, `documentation`, `feature`

2. **Assignees**
   - `None` - leave unassigned
   - `Me` - assign to current user
   - Custom - specify username

3. **Milestone**
   - Available milestones from repo
   - `None` - no milestone

4. **Final Confirmation (MUST ASK)**
   - `Create Issue` - proceed with creation
   - `Edit` - modify issue content
   - `Cancel` - abort issue creation

**DO NOT create issue until user explicitly selects "Create Issue"**

---

## Jira Ticket Integration

### Extract from Branch Name

```
feature/PROJ-123-add-feature  →  Jira: PROJ-123
bugfix/PROJ-456-fix-bug       →  Jira: PROJ-456
```

### Add to Issue Body

```markdown
## Related

- Jira: [PROJ-123](https://your-jira.atlassian.net/browse/PROJ-123)
```

### Fetch Jira Details (if applicable)

Use `mcp__mcp-atlassian__jira_get_issue` to get:
- Ticket summary
- Ticket description
- Include relevant context in GitHub issue

---

## Examples

### Example 1: Bug Report

**User Input:**
"The login button doesn't work on mobile Safari"

**Generated Issue:**
```markdown
Title: Login button not working on mobile Safari

## Description

The login button is unresponsive when accessed from mobile Safari browser.

## Steps to Reproduce

1. Open the application on iOS Safari
2. Navigate to login page
3. Tap the login button
4. Observe: Nothing happens

## Expected Behavior

Login form should be submitted and user authenticated.

## Environment

- Browser: Safari (iOS)
- Device: iPhone
```

**Suggested Labels:** `bug`, `mobile`, `high-priority`

### Example 2: Feature Request

**User Input:**
"We need export to PDF functionality for reports"

**Generated Issue:**
```markdown
Title: Add PDF export for reports

## Description

Implement PDF export functionality for report pages.

## Requirements

- [ ] Add "Export to PDF" button on report pages
- [ ] Generate well-formatted PDF with charts and tables
- [ ] Support custom page sizes (A4, Letter)
- [ ] Include report metadata (date, filters applied)

## Use Cases

- Users need to share reports with stakeholders
- Offline viewing and archival purposes
```

**Suggested Labels:** `enhancement`, `feature-request`

### Example 3: With Jira Ticket

**Branch:** `feature/PROJ-789-user-dashboard`
**User Input:** "Create GitHub issue for the dashboard feature"

**Generated Issue:**
```markdown
Title: Implement user dashboard [PROJ-789]

## Description

Create a user dashboard showing key metrics and recent activity.

## Requirements

- Display user statistics
- Show recent activity feed
- Add quick action shortcuts

## Related

- Jira: [PROJ-789](https://jira.example.com/browse/PROJ-789)
- Jira Summary: Implement user dashboard with metrics
```

**Suggested Labels:** `enhancement`, `feature`

---

## GitHub CLI Reference

```bash
# List available labels
gh label list --json name,description

# List milestones
gh api repos/{owner}/{repo}/milestones --jq '.[].title'

# Create issue
gh issue create \
  --title "Issue title" \
  --body "Issue body" \
  --label "bug,enhancement" \
  --assignee "@me" \
  --milestone "v1.0"

# Create issue with body from stdin
gh issue create --title "Title" --body-file -
```
