---
name: creating-jira-issue
description: Creates a Jira issue from user-provided context. Uses AskUserQuestion to confirm project, issue type, assignee, and priority before creating. Use when user wants to create a new Jira ticket.
---

# Creating Jira Issue

$ARGUMENTS

## Instructions

1. **Analyze user context**
   - Extract key information from user's description
   - Identify potential summary and description content
   - Determine suggested issue type based on context

2. **Draft issue content**
   - Generate concise summary (max 100 chars)
   - Create detailed description with context
   - Suggest appropriate issue type and priority

3. **Ask user to confirm issue details**
   - Use `AskUserQuestion` tool to confirm/select:
     - Project key
     - Issue type
     - Assignee
     - Priority
   - Show drafted summary and description

4. **Create the issue**
   - Use `mcp__mcp-atlassian__jira_create_issue` tool
   - Return the created issue key and URL

---

## Issue Types

| Type | When to Use |
|------|-------------|
| `Story` | New feature or user-facing functionality |
| `Task` | Technical work, maintenance, or general tasks |
| `Bug` | Defect or unexpected behavior |
| `Epic` | Large feature spanning multiple stories |
| `Sub-task` | Breakdown of a larger issue |

---

## Priority Levels

| Priority | Description |
|----------|-------------|
| `Highest` | Critical blocker, needs immediate attention |
| `High` | Important, should be addressed soon |
| `Medium` | Normal priority (default) |
| `Low` | Can be addressed when time permits |
| `Lowest` | Nice to have, no urgency |

---

## Pre-Creation Confirmation

**IMPORTANT: Use `AskUserQuestion` tool to confirm issue details**

### Example Output Before Asking

```markdown
## New Jira Issue

**Summary:** Add user authentication with OAuth2

**Description:**
Implement OAuth2 authentication flow for the application.

Requirements:
- Support Google and GitHub OAuth providers
- Store user tokens securely
- Implement token refresh logic

**Suggested Settings:**
- Issue Type: Story
- Priority: Medium
```

### AskUserQuestion Options

Ask for each setting using `AskUserQuestion`:

1. **Project** - Select target project
   - Options based on available projects

2. **Issue Type** - Select issue type
   - `Story` - new feature
   - `Task` - technical work
   - `Bug` - defect fix
   - `Epic` - large feature

3. **Assignee** - Select assignee
   - `Unassigned` - leave unassigned
   - `Me` - assign to current user
   - Custom - specify other user

4. **Priority** - Select priority level
   - `High` - important
   - `Medium` - normal (default)
   - `Low` - not urgent

---

## Examples

### Example 1: Feature Request

**User Input:**
"We need to add a dark mode toggle to the settings page"

**Generated Issue:**
```
Summary: Add dark mode toggle to settings page

Description:
Implement a dark mode toggle feature in the application settings.

Requirements:
- Add toggle switch in Settings page
- Persist user preference
- Apply dark theme across all components

Acceptance Criteria:
- [ ] Toggle is visible in Settings
- [ ] Theme changes immediately on toggle
- [ ] Preference persists after app restart
```

**Suggested:** Story, Medium priority

### Example 2: Bug Report

**User Input:**
"Users are getting logged out randomly after about 30 minutes"

**Generated Issue:**
```
Summary: Users getting logged out unexpectedly after ~30 minutes

Description:
Users report being logged out of the application unexpectedly
after approximately 30 minutes of usage.

Steps to Reproduce:
1. Log into the application
2. Use the application for ~30 minutes
3. Observe unexpected logout

Expected: User remains logged in
Actual: User is logged out unexpectedly

Impact: Users lose unsaved work and must re-authenticate
```

**Suggested:** Bug, High priority

### Example 3: Technical Task

**User Input:**
"Need to upgrade Spring Boot to version 3.2"

**Generated Issue:**
```
Summary: Upgrade Spring Boot to 3.2

Description:
Upgrade Spring Boot framework from current version to 3.2.

Tasks:
- Update build.gradle dependencies
- Review breaking changes in release notes
- Update deprecated API usage
- Run full test suite
- Verify application startup and functionality
```

**Suggested:** Task, Medium priority

---

## Jira API Reference

```
mcp__mcp-atlassian__jira_create_issue

Parameters:
- project_key: "PROJ" (required)
- summary: "Issue title" (required)
- issue_type: "Story" | "Task" | "Bug" | "Epic" (required)
- description: "Detailed description" (optional)
- assignee: "user@example.com" (optional)
- priority: "High" | "Medium" | "Low" (optional via additional_fields)
- additional_fields: {"priority": {"name": "High"}} (optional)
```
