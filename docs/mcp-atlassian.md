# MCP Atlassian Server

Connect Claude Code to Jira and Confluence using the [mcp-atlassian](https://github.com/sooperset/mcp-atlassian) MCP server.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- Atlassian API token

## Installation

### 1. Install uv (if not installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Get Atlassian API Token

1. Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Enter a label (e.g., "Claude Code MCP")
4. Copy and save the generated token

### 3. Configure Claude Code

Add the following to your Claude Code settings:

**Location**: `~/.claude/settings.json` (user) or `.claude/settings.json` (project)

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_USERNAME": "your.email@company.com",
        "JIRA_API_TOKEN": "your_api_token",
        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "your.email@company.com",
        "CONFLUENCE_API_TOKEN": "your_api_token"
      }
    }
  }
}
```

### Configuration Options

| Variable | Required | Description |
|----------|----------|-------------|
| `JIRA_URL` | Yes | Your Atlassian Jira URL |
| `JIRA_USERNAME` | Yes | Your Atlassian email address |
| `JIRA_API_TOKEN` | Yes | API token from step 2 |
| `CONFLUENCE_URL` | No | Your Confluence URL (usually `{JIRA_URL}/wiki`) |
| `CONFLUENCE_USERNAME` | No | Same as Jira username |
| `CONFLUENCE_API_TOKEN` | No | Same as Jira token |

## Usage

After configuration, Claude Code can:

### Jira
- Search and get issues (`jira_search`, `jira_get_issue`)
- Create and update issues (`jira_create_issue`, `jira_update_issue`)
- Manage sprints and boards (`jira_get_sprints_from_board`)
- Add comments and worklogs (`jira_add_comment`, `jira_add_worklog`)
- Transition issues (`jira_transition_issue`)

### Confluence
- Search pages (`confluence_search`)
- Read and update pages (`confluence_get_page`, `confluence_update_page`)
- Create pages (`confluence_create_page`)
- Manage comments and labels

## Example Commands

```
# Search Jira issues
"Find all bugs assigned to me in PROJ"

# Get issue details
"Show me the details of PROJ-123"

# Create an issue
"Create a bug in PROJ for the login error"

# Search Confluence
"Find documentation about API authentication"
```

## Troubleshooting

### "uvx: command not found"
Ensure uv is installed and in your PATH:
```bash
which uvx
# Should output: /Users/username/.local/bin/uvx
```

### Authentication errors
- Verify your API token is correct
- Ensure the username is your email address (not display name)
- Check the URL format (no trailing slash)

### Connection issues
- Verify network access to Atlassian
- Check if VPN is required for your organization

## Related Skills

This MCP server works with the following skills in this repository:

| Skill | Description |
|-------|-------------|
| `create-branch-from-jira` | Create git branches from Jira tickets |
| `create-jira-issue` | Create Jira issues with MCP |
| `commit-changes` | Commit with Jira ticket integration |
| `create-pull-request` | Create PRs with Jira links |
