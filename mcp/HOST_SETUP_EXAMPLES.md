# ARC MCP Host Setup Examples

These are host examples only. Keep secrets outside the repository.

## GitHub official MCP
Preferred for ARC generation: read-only.

Remote endpoint:
```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

Local Docker alternative should enable read-only mode for ordinary question generation.

## draw.io official MCP
```json
{
  "servers": {
    "drawio": {
      "command": "npx",
      "args": ["-y", "@drawio/mcp"]
    }
  }
}
```

## ChemCP
```json
{
  "mcpServers": {
    "chemcp": {
      "command": "npx",
      "args": ["chemcp"]
    }
  }
}
```

## Timeline Generator MCP
```json
{
  "mcpServers": {
    "timeline-generator-mcp": {
      "command": "uvx",
      "args": ["timeline-generator-mcp"]
    }
  }
}
```

## ARC runtime rule
Host syntax differs by client. Treat these as reference snippets, not a single universal config. The ARC source-of-truth remains `MCP_POLICY.yaml` and `SERVER_REGISTRY.yaml`.
