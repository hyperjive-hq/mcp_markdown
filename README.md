# MCP Markdown Server

A Model Context Protocol (MCP) server for markdown-based knowledge management.

## Features

- **File Operations**: Create, read, update, and delete markdown files
- **Search**: Search across all markdown content
- **Templates**: Support for markdown templates
- **LLM Integration**: Built-in LLM usage guide for consistent behavior
- **Flexible Structure**: Works with any directory structure (only requires `system/` directory)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Setup

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd mcp_markdown
   ```

2. **Install the package**
   ```bash
   pip install -e .
   ```

3. **Set up your knowledge base directory**
   
   The server requires a knowledge base directory with a `system/` subdirectory:
   ```bash
   mkdir -p your-knowledge-base/system
   mkdir -p your-knowledge-base/system/templates
   ```

4. **Test the installation**
   ```bash
   mcp-markdown-server --help
   ```

### Alternative Installation Methods

#### Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install the package
pip install -e .
```

#### Development Installation

```bash
# Install with development dependencies
pip install -e ".[dev]"
```

## Usage

The MCP Markdown Server supports three transport methods via command-line options:

### Transport Options

#### 1. Standard MCP (stdio) - Default
For standard MCP clients that communicate over stdio:

```bash
# Start server with default configuration (uses ./knowledge-base)
mcp-markdown-server

# Use custom knowledge base directory
mcp-markdown-server --knowledge-base /path/to/your/notes --transport stdio

# Use custom configuration file
mcp-markdown-server --config config.yaml --transport stdio
```

#### 2. Streamable HTTP Transport
For integration with tools like MCP Inspector:

```bash
# Start HTTP server on default port 3005
mcp-markdown-server --knowledge-base /path/to/your/notes --transport http

# Specify custom host and port
mcp-markdown-server --knowledge-base /path/to/your/notes --transport http --host 0.0.0.0 --port 3005

# Example with custom port
mcp-markdown-server --knowledge-base ~/notes --transport http --port 8080
```

#### 3. Server-Sent Events (SSE) Transport
For integration with n8n and other SSE-compatible clients:

```bash
# Start SSE server on default port 3005
mcp-markdown-server --knowledge-base /path/to/your/notes --transport sse

# Specify custom host and port
mcp-markdown-server --knowledge-base /path/to/your/notes --transport sse --host 0.0.0.0 --port 3005

# Example with custom port
mcp-markdown-server --knowledge-base ~/notes --transport sse --port 8080
```

### Transport Selection

Use the `--transport` option to choose your preferred transport method:

- `stdio` (default): Standard MCP protocol over stdin/stdout
- `http`: Streamable HTTP transport for web-based tools
- `sse`: Server-Sent Events for real-time streaming clients

All transports provide the same MCP tools and resources, just with different communication methods.

### Integration Examples

#### MCP Inspector Integration

To use with MCP Inspector:

1. Start the HTTP server:
   ```bash
   mcp-markdown-server --knowledge-base ~/notes --transport http --host 0.0.0.0 --port 3005
   ```

2. In MCP Inspector, connect to:
   - **Server URL**: `http://localhost:3005`
   - **Transport**: HTTP (Streamable)

3. The server will appear in MCP Inspector with full tool and resource support.

#### n8n Integration

To use with n8n (which requires SSE transport):

1. Start the SSE server:
   ```bash
   mcp-markdown-server --knowledge-base ~/notes --transport sse --host 0.0.0.0 --port 3005
   ```

2. In n8n, configure the MCP connection:
   - **Server URL**: `http://localhost:3005` (or `http://host.docker.internal:3005` from Docker)
   - **Transport**: SSE (Server-Sent Events)

3. Available MCP tools in n8n:
   - `create_file` - Create new markdown files
   - `read_file` - Read existing files
   - `update_file` - Update file content
   - `delete_file` - Remove files
   - `list_files` - List all markdown files
   - `search_content` - Search across content

#### Available Tools

The HTTP server provides the same tools as the stdio server:

- `create_file` - Create new markdown files with optional metadata
- `read_file` - Read existing files with frontmatter
- `update_file` - Update file content and/or metadata
- `delete_file` - Remove files
- `list_files` - List all markdown files (with pattern filtering)
- `search_content` - Search across all file content

#### Available Resources

- **LLM Usage Guide** (`llm-guide://system/llm-guide.md`) - Comprehensive guide for LLMs on how to effectively use the knowledge management system

### First Time Setup

1. **Create your knowledge base structure**
   ```bash
   mkdir -p my-knowledge-base/system/templates
   ```

2. **Start the server**
   ```bash
   mcp-markdown-server --knowledge-base my-knowledge-base
   ```

3. **The server will automatically create**:
   - `system/llm-guide.md` - Instructions for LLMs
   - Required directory structure
   - Default configuration files

### Verifying Installation

After starting the server, you should see log output similar to:
```
Starting MCP server for knowledge base: /path/to/your/knowledge-base on localhost:8000
```

The server provides an HTTP interface on the specified port for MCP protocol communication.

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

## Templates

The MCP server supports markdown templates to ensure consistent file structure and formatting. Templates are stored in the `system/templates/` directory and use placeholder variables that get replaced when creating new files.

### How Templates Work

Templates are markdown files with special naming convention and variable substitution:

1. **Template files** use `.template.md` extension (e.g., `note.template.md`)
2. **Variables** are enclosed in double curly braces: `{{variable_name}}`
3. **Frontmatter** can include template variables for metadata
4. **Content** can include template variables for structured content

### Built-in Template Variables

The system provides several built-in variables:

- `{{title}}` - The title of the new file
- `{{date}}` - Current date in YYYY-MM-DD format
- `{{time}}` - Current time in HH:MM format
- `{{datetime}}` - Full timestamp

### Example Template

Here's the built-in note template (`system/templates/note.template.md`):

```markdown
---
type: note
title: "{{title}}"
created: {{date}}
tags: []
---

# {{title}}

## Summary


## Details


## Related
```

### Using Templates

Templates are referenced by their name (filename without `.template.md`):

1. **Via MCP tools**: When creating files, the system can automatically apply templates
2. **Via LLM guide**: Templates are listed in the auto-generated LLM guide
3. **Manual creation**: Copy template structure when creating new files

### Template Configuration

Templates can be configured in the main configuration file:

```yaml
templates:
  template_directory: "system/templates"  # Where templates are stored
  date_format: "%Y-%m-%d"                # Format for {{date}} variable
  time_format: "%H:%M"                   # Format for {{time}} variable
```

### Creating Custom Templates

To create a custom template:

1. Create a new `.template.md` file in `system/templates/`
2. Include frontmatter with relevant metadata fields
3. Use `{{variable}}` syntax for dynamic content
4. Structure the content with appropriate headings and sections

Example custom template for meeting notes:

```markdown
---
type: meeting
title: "{{title}}"
date: {{date}}
time: {{time}}
attendees: []
tags: [meeting]
---

# {{title}}

**Date:** {{date}}  
**Time:** {{time}}  
**Attendees:** 

## Agenda


## Discussion


## Action Items


## Follow-up
```

## MCP Streamable HTTP Implementation

The HTTP server follows the official MCP Streamable HTTP transport specification (protocol version 2024-11-05). This implementation provides a more robust and standardized way to communicate with MCP clients over HTTP.

### Architecture Overview

The server uses a service layer architecture that separates business logic from transport concerns:

- **Service Layer** (`service.py`): Contains all markdown operations and MCP protocol logic
- **Unified Server** (`server.py`): Provides stdio, HTTP, and SSE transports via FastMCP

### Protocol Features

#### JSON-RPC 2.0 Communication

All MCP communication uses JSON-RPC 2.0 format:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

#### Session Management

The server supports stateful sessions with:

- **Session IDs**: Unique identifiers for client sessions
- **Session Tracking**: Maintains session state across requests
- **Session Cleanup**: Automatic cleanup of expired sessions

#### Event Streaming

Server-Sent Events provide real-time communication:

```
GET /mcp
X-Session-ID: session-123
Last-Event-ID: 42

id: 43
data: {"type": "tool_result", "content": "..."}
```

#### Resumability

Clients can resume interrupted connections:

- **Last-Event-ID**: Clients send last received event ID
- **Event Replay**: Server replays missed events (future feature)
- **Connection Recovery**: Seamless reconnection support

### Testing the Implementation

Use the included test script to verify the server:

```bash
# Start the SSE server for testing
mcp-markdown-server --knowledge-base ~/notes --transport sse --port 3005

# Run tests in another terminal
python test_sse.py
```

The test script validates:
- Basic HTTP endpoints
- JSON-RPC protocol compliance
- MCP tool and resource operations
- SSE streaming functionality

### Debugging Connections

Enable debug logging to troubleshoot connections:

```bash
# Debug SSE transport
mcp-markdown-server --knowledge-base ~/notes --transport sse --port 3005

# Debug HTTP transport  
mcp-markdown-server --knowledge-base ~/notes --transport http --port 3005
```

Common debugging steps:
1. Check server logs for connection attempts
2. Verify client sends proper JSON-RPC requests
3. Test endpoints individually with curl or test script
4. Monitor SSE stream for proper event formatting

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

templates:
  template_directory: "system/templates"
  date_format: "%Y-%m-%d"
  time_format: "%H:%M"
```

## Troubleshooting

### Common Issues

#### 1. Server won't start
- **Problem**: `mcp-markdown-server: command not found`
- **Solution**: Make sure you've installed the package with `pip install -e .` and your Python environment is activated

#### 2. Permission errors
- **Problem**: `Permission denied` when creating files
- **Solution**: Ensure the user has write permissions to the knowledge base directory:
  ```bash
  chmod -R 755 your-knowledge-base/
  ```

#### 3. Import errors
- **Problem**: `ModuleNotFoundError: No module named 'mcp'`
- **Solution**: Install missing dependencies:
  ```bash
  pip install -e .
  ```

#### 4. Configuration issues
- **Problem**: Server uses wrong directory or settings
- **Solution**: Check your config.yaml file and ensure it's in the correct location, or use command line arguments:
  ```bash
  mcp-markdown-server --config /path/to/config.yaml --knowledge-base /path/to/knowledge-base
  ```

#### 5. Port already in use
- **Problem**: `Address already in use` error
- **Solution**: Use a different port:
  ```bash
  mcp-markdown-server --port 8001
  ```

### Logging

The server logs to both console and `server.log` file. Check the log file for detailed error information:

```bash
tail -f server.log
```

### Getting Help

If you encounter issues not covered here:

1. Check the server logs for detailed error messages
2. Verify your Python version is 3.8 or higher
3. Ensure all dependencies are installed correctly
4. Try running with a fresh virtual environment

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