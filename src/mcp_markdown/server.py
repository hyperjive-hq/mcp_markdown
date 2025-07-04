import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource, TextResourceContents
import argparse
import logging
import traceback
from .config import load_config
from .file_operations import FileManager

# Set up logging
# Set up logging
log_file_path = "server.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler() # Also keep console output for immediate feedback
    ]
)
logger = logging.getLogger(__name__)

class MarkdownMCPServer:
    def __init__(self, config_path: str = None):
        self.config = load_config(config_path)
        self.file_manager = FileManager(
            self.config.knowledge_base.root_directory,
            self.config.knowledge_base.system_directory
        )
        self.server = Server("markdown-knowledge-base")
        self.file_manager.create_llm_guide()
        self._register_tools()
        self._register_resources()
    
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
                tb = traceback.format_exc()
                logger.error(tb)
                return [TextContent(type="text", text=f"Error executing tool '{name}':\n\n{tb}")]
    
    def _register_resources(self):
        """Register all MCP resources"""
        
        @self.server.list_resources()
        async def list_resources():
            return [
                Resource(
                    uri="llm-guide://system/llm-guide.md",
                    name="LLM Usage Guide",
                    description="Instructions for LLMs on how to use the knowledge management system",
                    mimeType="text/markdown"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str):
            try:
                if uri == "llm-guide://system/llm-guide.md":
                    guide_data = self.file_manager.read_file("system/llm-guide.md")
                    content = guide_data['content']
                    if guide_data['metadata']:
                        # Add metadata as frontmatter
                        metadata_str = "\n".join([f"{k}: {v}" for k, v in guide_data['metadata'].items()])
                        content = f"---\n{metadata_str}\n---\n\n{content}"
                    # Return content string - MCP library handles the wrapping
                    return content
                else:
                    return f"Unknown resource: {uri}"
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                return f"Error: {str(e)}"
    
    def app(self):
        return self.server

def main():
    parser = argparse.ArgumentParser(description="Markdown Knowledge Base MCP Server")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--knowledge-base", help="Path to knowledge base directory")
    parser.add_argument("--host", help="Host to bind to")
    parser.add_argument("--port", help="Port to bind to")
    
    args = parser.parse_args()
    
    # Override config with command line arguments
    if args.knowledge_base:
        import os
        os.environ["KNOWLEDGE_BASE_ROOT"] = args.knowledge_base
    
    mcp_server = MarkdownMCPServer(args.config)
    
    # Get host and port from args or config
    host = args.host or mcp_server.config.server.host
    port = args.port or mcp_server.config.server.port
    
    import uvicorn
    logger.info(f"Starting MCP server for knowledge base: {mcp_server.config.knowledge_base.root_directory} on {host}:{port}")
    uvicorn.run(mcp_server.server, host=host, port=port)

if __name__ == "__main__":
    main()