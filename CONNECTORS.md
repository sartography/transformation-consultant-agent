# Connectors

This plugin uses MCP (Model Context Protocol) servers to connect Claude to external tools. Connectors are configured in [.mcp.json](.mcp.json).

## Available Connectors

### Slack

Share transformation analysis results, BPMN summaries, and optimization recommendations with your team channels.

**Setup:** Add your Slack MCP server URL to `.mcp.json`:
```json
"slack": {
  "type": "http",
  "url": "https://mcp.slack.com/mcp"
}
```

### Microsoft 365

Read process transcripts from SharePoint/OneDrive and save analysis outputs to shared document libraries.

**Setup:** Add your Microsoft 365 MCP server URL to `.mcp.json`:
```json
"ms365": {
  "type": "http",
  "url": "https://microsoft365.mcp.claude.com/mcp"
}
```

## Adding More Connectors

Edit `.mcp.json` to add connections to your organization's tools. Common additions for transformation consulting:

| Tool | Purpose | MCP Server |
|------|---------|------------|
| **Jira / Linear** | Track implementation roadmap tasks | Project management MCP |
| **Notion** | Store and share analysis documentation | Knowledge management MCP |
| **Google Workspace** | Read/write documents and spreadsheets | Google MCP |
| **Snowflake / BigQuery** | Query process metrics and volumes | Data warehouse MCP |

### Example: Adding Jira

```json
{
  "mcpServers": {
    "slack": { "type": "http", "url": "..." },
    "ms365": { "type": "http", "url": "..." },
    "jira": { "type": "http", "url": "https://your-jira-mcp-url" }
  }
}
```

For the latest list of available MCP servers, see [modelcontextprotocol.io](https://modelcontextprotocol.io/).
