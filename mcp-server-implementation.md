# MCP Server Implementation Guide

## Goal
Build a minimal but functional MCP server that can manage markdown files in any directory structure, with only a `system/` directory required.

## Prerequisites
- Python 3.8+
- Basic familiarity with MCP (Model Context Protocol)
- A target directory where you want to store markdown files

## Project Structure

```
mcp-markdown-server/
├── mcp_server.py          # Main server implementation
├── config.py              # Configuration handling
├── file_operations.py     # File CRUD operations  
├── frontmatter_parser.py  # YAML frontmatter handling
├── config.yaml            # Default configuration
├── pyproject.toml         # Project dependencies and configuration
└── README.md              # Usage instructions
```

## Target Knowledge Base Structure

The MCP server will work with any directory structure, requiring only:

```
your-knowledge-base/
├── system/                # Required system directory
│   ├── templates/         # Optional: markdown templates
│   ├── .index/           # Optional: search index (auto-created)
│   └── llm-guide.md      # Optional: LLM usage instructions
├── ... any other files and directories you want ...
```

## Implementation Steps

### Day 1: Basic Setup

#### 1. Create Project Directory
```bash
mkdir mcp-markdown-server
cd mcp-markdown-server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Create Project Configuration
Create `pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mcp-markdown-server"
version = "0.1.0"
description = "MCP server for markdown-based knowledge management"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "mcp>=0.1.0",
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "pydantic>=2.0.0",
    "python-frontmatter>=1.0.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

[project.scripts]
mcp-markdown-server = "mcp_server:main"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

#### 3. Install Dependencies
```bash
# Install the project in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

#### 4. Create Configuration System (`config.py`)
```python
from pydantic import BaseModel
from typing import Dict, List
import yaml
import os
from pathlib import Path

class KnowledgeBaseConfig(BaseModel):
    root_directory: str
    system_directory: str = "system"
    git: Dict = {"enabled": False}
    file_patterns: Dict = {
        "markdown_extensions": [".md", ".markdown"],
        "ignore_patterns": [".*", "*.tmp", "node_modules/", "system/.index/"]
    }

class ServerConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000
    log_level: str = "INFO"

class SearchConfig(BaseModel):
    index_directory: str = "system/.index"
    rebuild_on_startup: bool = False

class TemplatesConfig(BaseModel):
    template_directory: str = "system/templates"
    date_format: str = "%Y-%m-%d"
    time_format: str = "%H:%M"

class Config(BaseModel):
    knowledge_base: KnowledgeBaseConfig
    server: ServerConfig
    search: SearchConfig
    templates: TemplatesConfig

def load_config(config_path: str = None) -> Config:
    """Load configuration from file and environment variables"""
    
    # Default config
    config_data = {
        "knowledge_base": {
            "root_directory": os.getenv("KNOWLEDGE_BASE_ROOT", "./knowledge-base")
        },
        "server": {},
        "search": {},
        "templates": {}
    }
    
    # Load from config file if provided
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            file_config = yaml.safe_load(f)
            config_data.update(file_config)
    
    # Override with environment variables
    if os.getenv("KB_SYSTEM_DIR"):
        config_data["knowledge_base"]["system_directory"] = os.getenv("KB_SYSTEM_DIR")
    
    return Config(**config_data)
```

#### 5. Create Basic File Operations (`file_operations.py`)
```python
from pathlib import Path
from typing import List, Optional, Dict, Any
import frontmatter
import os
import json
from datetime import datetime

class FileManager:
    def __init__(self, root_directory: str, system_directory: str = "system"):
        self.root_path = Path(root_directory).resolve()
        self.system_path = self.root_path / system_directory
        
        # Ensure system directory exists
        self.system_path.mkdir(exist_ok=True)
    
    def create_file(self, relative_path: str, content: str, metadata: Dict[str, Any] = None) -> str:
        """Create a new markdown file with optional frontmatter"""
        file_path = self.root_path / relative_path
        
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create frontmatter post
        post = frontmatter.Post(content)
        if metadata:
            post.metadata.update(metadata)
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return str(file_path.relative_to(self.root_path))
    
    def read_file(self, relative_path: str) -> Dict[str, Any]:
        """Read a markdown file and return content + metadata"""
        file_path = self.root_path / relative_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        return {
            "content": post.content,
            "metadata": post.metadata,
            "file_path": relative_path
        }
    
    def update_file(self, relative_path: str, content: str = None, metadata: Dict[str, Any] = None) -> str:
        """Update an existing file's content and/or metadata"""
        file_path = self.root_path / relative_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")
        
        # Read existing file
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        # Update content and metadata
        if content is not None:
            post.content = content
        if metadata is not None:
            post.metadata.update(metadata)
        
        # Write updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        return str(file_path.relative_to(self.root_path))
    
    def delete_file(self, relative_path: str) -> bool:
        """Delete a file"""
        file_path = self.root_path / relative_path
        
        if not file_path.exists():
            return False
        
        file_path.unlink()
        return True
    
    def list_files(self, pattern: str = "*.md") -> List[str]:
        """List all markdown files in the knowledge base"""
        files = []
        for file_path in self.root_path.rglob(pattern):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.root_path)
                files.append(str(relative_path))
        return sorted(files)
    
    def search_content(self, query: str) -> List[Dict[str, Any]]:
        """Basic text search across all files"""
        results = []
        
        for file_path in self.root_path.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if query.lower() in content.lower():
                    relative_path = file_path.relative_to(self.root_path)
                    results.append({
                        "file_path": str(relative_path),
                        "match_preview": self._get_match_preview(content, query)
                    })
            except Exception:
                continue  # Skip files that can't be read
        
        return results
    
    def _get_match_preview(self, content: str, query: str, context_chars: int = 100) -> str:
        """Get a preview of the match with surrounding context"""
        content_lower = content.lower()
        query_lower = query.lower()
        
        index = content_lower.find(query_lower)
        if index == -1:
            return ""
        
        start = max(0, index - context_chars)
        end = min(len(content), index + len(query) + context_chars)
        
        preview = content[start:end]
        if start > 0:
            preview = "..." + preview
        if end < len(content):
            preview = preview + "..."
        
        return preview
```

### Day 2: MCP Server Implementation

#### 6. Create Main MCP Server (`mcp_server.py`)
```python
import asyncio
from mcp import Server
from mcp.types import Tool, TextContent, Resource
import argparse
import logging
from config import load_config
from file_operations import FileManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarkdownMCPServer:
    def __init__(self, config_path: str = None):
        self.config = load_config(config_path)
        self.file_manager = FileManager(
            self.config.knowledge_base.root_directory,
            self.config.knowledge_base.system_directory
        )
        self.server = Server("markdown-knowledge-base")
        self._register_tools()
    
    def _register_tools(self):
        """Register all MCP tools"""
        
        @self.server.list_tools()
        async def list_tools():
            return [
                Tool(
                    name="create_file",
                    description="Create a new markdown file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Relative path for the new file"},
                            "content": {"type": "string", "description": "File content"},
                            "metadata": {"type": "object", "description": "Optional frontmatter metadata"}
                        },
                        "required": ["path", "content"]
                    }
                ),
                Tool(
                    name="read_file",
                    description="Read a markdown file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Relative path to the file"}
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="update_file",
                    description="Update an existing markdown file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Relative path to the file"},
                            "content": {"type": "string", "description": "New content (optional)"},
                            "metadata": {"type": "object", "description": "Metadata to update (optional)"}
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="delete_file",
                    description="Delete a markdown file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Relative path to the file"}
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="list_files",
                    description="List all markdown files",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string", "description": "File pattern (default: *.md)"}
                        }
                    }
                ),
                Tool(
                    name="search_content",
                    description="Search for text across all files",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"}
                        },
                        "required": ["query"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            try:
                if name == "create_file":
                    result = self.file_manager.create_file(
                        arguments["path"],
                        arguments["content"],
                        arguments.get("metadata")
                    )
                    return [TextContent(type="text", text=f"Created file: {result}")]
                
                elif name == "read_file":
                    result = self.file_manager.read_file(arguments["path"])
                    content = f"# {result['file_path']}\n\n"
                    if result['metadata']:
                        content += f"**Metadata:** {result['metadata']}\n\n"
                    content += result['content']
                    return [TextContent(type="text", text=content)]
                
                elif name == "update_file":
                    result = self.file_manager.update_file(
                        arguments["path"],
                        arguments.get("content"),
                        arguments.get("metadata")
                    )
                    return [TextContent(type="text", text=f"Updated file: {result}")]
                
                elif name == "delete_file":
                    result = self.file_manager.delete_file(arguments["path"])
                    if result:
                        return [TextContent(type="text", text=f"Deleted file: {arguments['path']}")]
                    else:
                        return [TextContent(type="text", text=f"File not found: {arguments['path']}")]
                
                elif name == "list_files":
                    pattern = arguments.get("pattern", "*.md")
                    files = self.file_manager.list_files(pattern)
                    return [TextContent(type="text", text=f"Found {len(files)} files:\n" + "\n".join(files))]
                
                elif name == "search_content":
                    results = self.file_manager.search_content(arguments["query"])
                    if not results:
                        return [TextContent(type="text", text="No matches found")]
                    
                    content = f"Found {len(results)} matches:\n\n"
                    for result in results:
                        content += f"**{result['file_path']}**\n{result['match_preview']}\n\n"
                    return [TextContent(type="text", text=content)]
                
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            
            except Exception as e:
                logger.error(f"Error in tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def run(self):
        """Run the MCP server"""
        logger.info(f"Starting MCP server for knowledge base: {self.config.knowledge_base.root_directory}")
        await self.server.run()

def main():
    parser = argparse.ArgumentParser(description="Markdown Knowledge Base MCP Server")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--knowledge-base", help="Path to knowledge base directory")
    
    args = parser.parse_args()
    
    # Override config with command line arguments
    if args.knowledge_base:
        import os
        os.environ["KNOWLEDGE_BASE_ROOT"] = args.knowledge_base
    
    server = MarkdownMCPServer(args.config)
    asyncio.run(server.run())

if __name__ == "__main__":
    main()
```

### Day 3: Testing and Basic Templates

#### 7. Create Test Knowledge Base
```bash
mkdir test-knowledge-base
cd test-knowledge-base
mkdir system
mkdir system/templates
```

#### 8. Create Basic Template (`system/templates/note.template.md`)
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

#### 9. Test the Server
```bash
cd mcp-markdown-server
python mcp_server.py --knowledge-base ../test-knowledge-base
```

### Day 4: LLM Guide and Documentation

#### 10. Create LLM Usage Guide Generator
Add to `file_operations.py`:

```python
def generate_llm_guide(self) -> str:
    """Generate LLM usage guide based on current directory structure"""
    
    guide_content = """# LLM Usage Guide for Knowledge Management System

## Overview
This knowledge base uses a flexible directory structure with only one requirement: a `system/` directory for configuration and templates.

## Directory Structure
Current structure:
"""
    
    # Scan current directory structure
    for root, dirs, files in os.walk(self.root_path):
        level = root.replace(str(self.root_path), '').count(os.sep)
        indent = '  ' * level
        guide_content += f"{indent}- {os.path.basename(root)}/\n"
        
        subindent = '  ' * (level + 1)
        for file in files:
            if file.endswith('.md'):
                guide_content += f"{subindent}- {file}\n"
    
    guide_content += """
## File Operations
Use these MCP tools to manage files:

- `create_file`: Create new markdown files
- `read_file`: Read existing files with metadata
- `update_file`: Update content and frontmatter
- `delete_file`: Remove files
- `list_files`: List all markdown files
- `search_content`: Search across all content

## Best Practices
1. Use descriptive file names
2. Include relevant metadata in frontmatter
3. Organize files in a logical structure
4. Use consistent naming conventions
5. Link related files using markdown links

## Templates
Available templates in system/templates/:
"""
    
    # List available templates
    template_dir = self.system_path / "templates"
    if template_dir.exists():
        for template_file in template_dir.glob("*.template.md"):
            template_name = template_file.stem.replace('.template', '')
            guide_content += f"- {template_name}\n"
    
    return guide_content

def create_llm_guide(self):
    """Create or update the LLM guide"""
    guide_content = self.generate_llm_guide()
    guide_path = "system/llm-guide.md"
    
    self.create_file(guide_path, guide_content, {
        "type": "system",
        "title": "LLM Usage Guide",
        "generated": datetime.now().isoformat()
    })
```

#### 11. Create Default Configuration (`config.yaml`)
```yaml
knowledge_base:
  root_directory: "./knowledge-base"
  system_directory: "system"
  git:
    enabled: false
  file_patterns:
    markdown_extensions: [".md", ".markdown"]
    ignore_patterns: [".*", "*.tmp", "node_modules/", "system/.index/"]

server:
  host: "localhost"
  port: 8000
  log_level: "INFO"

search:
  index_directory: "system/.index"
  rebuild_on_startup: false

templates:
  template_directory: "system/templates"
  date_format: "%Y-%m-%d"
  time_format: "%H:%M"
```

## Success Criteria

After 1 week, you should have:

1. ✅ **Working MCP Server** - Can create, read, update, delete markdown files
2. ✅ **Configurable Target Directory** - Works with any directory structure
3. ✅ **Basic Search** - Can search content across files
4. ✅ **Template System** - Basic template support
5. ✅ **LLM Integration** - Works with Claude via MCP
6. ✅ **Minimal Requirements** - Only requires `system/` directory

## Next Steps

Once Phase 1 is complete:
- Add advanced search with indexing
- Implement Git integration
- Add file watching for real-time updates
- Create web UI for human editing

## Usage Examples

```bash
# Start server with default config
python mcp_server.py

# Use custom knowledge base
python mcp_server.py --knowledge-base /path/to/my/notes

# Use custom config
python mcp_server.py --config my-config.yaml

# Or use the installed script (if using pip install -e .)
mcp-markdown-server --knowledge-base /path/to/my/notes
```

The server will automatically:
- Create the `system/` directory if it doesn't exist
- Generate an LLM usage guide
- Provide all essential file operations via MCP tools
- Work with any directory structure you prefer