# MCP Markdown Server

A Model Context Protocol (MCP) server for markdown-based knowledge management.

## Features

- **File Operations**: Create, read, update, and delete markdown files
- **Search**: Search across all markdown content
- **Templates**: Support for markdown templates
- **LLM Integration**: Built-in LLM usage guide for consistent behavior
- **Flexible Structure**: Works with any directory structure (only requires `system/` directory)

## Installation

```bash
pip install -e .
```

## Usage

### Basic Usage

```bash
# Start server with default configuration
mcp-markdown-server

# Use custom knowledge base directory
mcp-markdown-server --knowledge-base /path/to/your/notes

# Use custom configuration file
mcp-markdown-server --config config.yaml
```

### Python Usage

```python
from mcp_markdown import MarkdownMCPServer

server = MarkdownMCPServer()
# Server provides MCP tools for file operations
```

## MCP Tools

The server provides the following MCP tools:

- **create_file**: Create new markdown files with optional frontmatter
- **read_file**: Read existing files with metadata
- **update_file**: Update content and/or frontmatter
- **delete_file**: Remove files
- **list_files**: List all markdown files
- **search_content**: Search across all content

## MCP Resources

- **LLM Usage Guide**: Provides instructions for LLMs on how to use the knowledge management system effectively

## Directory Structure

The server works with any directory structure but requires a `system/` directory:

```
your-knowledge-base/
├── system/                # Required system directory
│   ├── templates/         # Optional: markdown templates
│   ├── .index/           # Optional: search index (auto-created)
│   └── llm-guide.md      # Optional: LLM usage instructions
├── ... any other files and directories ...
```

## Configuration

Default configuration can be overridden with a YAML file:

```yaml
knowledge_base:
  root_directory: "./knowledge-base"
  system_directory: "system"

server:
  host: "localhost"
  port: 8000
  log_level: "INFO"
```

## Development

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/
```

## License

MIT License