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

### Basic Usage

```bash
# Start server with default configuration (uses ./knowledge-base)
mcp-markdown-server

# Use custom knowledge base directory
mcp-markdown-server --knowledge-base /path/to/your/notes

# Use custom configuration file
mcp-markdown-server --config config.yaml

# Specify host and port
mcp-markdown-server --host 0.0.0.0 --port 8080
```

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