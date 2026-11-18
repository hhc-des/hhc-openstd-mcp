# hhc-openstd-mcp

MCP server for searching, querying, and downloading Chinese national standards from the [国家标准全文公开系统](https://openstd.samr.gov.cn).

## Features

- **search_standards** — Search by keyword, filter by status (现行/即将实施/废止) and type (GB/GBT/GBZ)
- **get_standard_info** — Query full metadata for a standard number or URL
- **download_standard_pdf** — Download standard as PDF (handles both direct download and preview mode)

## Installation

```bash
# Using uvx (recommended, no install needed)
uvx hhc-openstd-mcp

# Using pip
pip install hhc-openstd-mcp
hhc-openstd-mcp
```

## MCP Client Configuration

### Claude Desktop / Claude Code

```json
{
  "mcpServers": {
    "hhc-openstd": {
      "command": "uvx",
      "args": ["hhc-openstd-mcp"]
    }
  }
}
```

### Cursor / VS Code

```json
{
  "mcp": {
    "hhc-openstd": {
      "type": "local",
      "command": ["npx", "-y", "hhc-openstd-mcp"]
    }
  }
}
```

(Or use `uvx` directly if available on PATH.)

### Cline

```json
{
  "mcpServers": {
    "hhc-openstd": {
      "command": "uvx",
      "args": ["hhc-openstd-mcp"]
    }
  }
}
```

## Example Tools

| Tool | Purpose |
|------|---------|
| `search_standards(keyword="通信管道", status="现行")` | Find current standards about communication ducts |
| `get_standard_info("GB 50374-2018")` | Get metadata for a specific standard |
| `download_standard_pdf("GB 50374-2018")` | Download the standard as PDF |

## License

GPL-3.0-or-later (same as upstream [OpenSTD_Spider](https://github.com/SocialSisterYi/OpenSTD_Spider)).
