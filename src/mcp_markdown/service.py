"""
Core service layer for markdown operations.
This layer contains the business logic that both MCP and HTTP servers can use.
"""
from typing import List, Dict, Any, Optional
from mcp.types import Tool, Resource, TextContent
from .config import Config
from .file_operations import FileManager


class MarkdownService:
    """Core service for markdown operations"""
    
    def __init__(self, config: Config):
        self.config = config
        self.file_manager = FileManager(
            config.knowledge_base.root_directory,
            config.knowledge_base.system_directory
        )
        # Create the LLM guide on initialization
        self.file_manager.create_llm_guide()
    
    def get_tools(self) -> List[Tool]:
        """Get list of available tools"""
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
                },
                annotations={
                    "destructiveHint": True
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
                },
                annotations={
                    "readOnlyHint": True
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
                },
                annotations={
                    "destructiveHint": True,
                    "idempotentHint": True
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
                },
                annotations={
                    "destructiveHint": True
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
                },
                annotations={
                    "readOnlyHint": True
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
                },
                annotations={
                    "readOnlyHint": True
                }
            )
        ]
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute a tool with given arguments"""
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
            return [TextContent(type="text", text=f"Error executing tool '{name}': {str(e)}")]
    
    def get_resources(self) -> List[Resource]:
        """Get list of available resources"""
        return [
            Resource(
                uri="llm-guide://system/llm-guide.md",
                name="LLM Usage Guide",
                title="LLM Usage Guide",
                description="Comprehensive guide for LLMs on how to effectively use the markdown knowledge management system, including file operations, directory structure, and best practices",
                mimeType="text/markdown"
            )
        ]
    
    def read_resource(self, uri: str) -> str:
        """Read a resource by URI"""
        # Validate URI scheme
        if not uri.startswith("llm-guide://"):
            raise ValueError(f"Invalid URI scheme. Expected 'llm-guide://', got: {uri}")
        
        if uri == "llm-guide://system/llm-guide.md":
            try:
                guide_data = self.file_manager.read_file("system/llm-guide.md")
                content = guide_data['content']
                if guide_data['metadata']:
                    # Add metadata as frontmatter
                    metadata_str = "\n".join([f"{k}: {v}" for k, v in guide_data['metadata'].items()])
                    content = f"---\n{metadata_str}\n---\n\n{content}"
                return content
            except FileNotFoundError as e:
                raise ValueError(f"Resource not found: {uri} - {str(e)}")
            except Exception as e:
                raise ValueError(f"Error reading resource {uri}: {str(e)}")
        else:
            raise ValueError(f"Unknown resource URI: {uri}")