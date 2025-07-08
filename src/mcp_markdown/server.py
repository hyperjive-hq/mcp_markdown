import asyncio
import argparse
import logging
import os
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP
from .config import load_config
from .service import MarkdownService

# Set up logging
log_file_path = "server.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MarkdownMCPServer:
    def __init__(self, config_path: str = None):
        self.config = load_config(config_path)
        self.service = MarkdownService(self.config)
        self.mcp = FastMCP("markdown-knowledge-base")
        self._register_tools()
        self._register_resources()
    
    def _register_tools(self):
        """Register all MCP tools using the FastMCP decorator pattern"""
        
        @self.mcp.tool()
        def create_file(path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
            """Create a new markdown file"""
            try:
                result = self.service.file_manager.create_file(path, content, metadata)
                return f"Created file: {result}"
            except Exception as e:
                logger.error(f"Error creating file {path}: {e}")
                raise
        
        @self.mcp.tool()
        def read_file(path: str) -> str:
            """Read a markdown file"""
            try:
                result = self.service.file_manager.read_file(path)
                content = f"# {result['file_path']}\n\n"
                if result['metadata']:
                    content += f"**Metadata:** {result['metadata']}\n\n"
                content += result['content']
                return content
            except Exception as e:
                logger.error(f"Error reading file {path}: {e}")
                raise
        
        @self.mcp.tool()
        def update_file(path: str, content: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
            """Update an existing markdown file"""
            try:
                result = self.service.file_manager.update_file(path, content, metadata)
                return f"Updated file: {result}"
            except Exception as e:
                logger.error(f"Error updating file {path}: {e}")
                raise
        
        @self.mcp.tool()
        def delete_file(path: str) -> str:
            """Delete a markdown file"""
            try:
                result = self.service.file_manager.delete_file(path)
                if result:
                    return f"Deleted file: {path}"
                else:
                    return f"File not found: {path}"
            except Exception as e:
                logger.error(f"Error deleting file {path}: {e}")
                raise
        
        @self.mcp.tool()
        def list_files(pattern: str = "*.md") -> str:
            """List all markdown files"""
            try:
                files = self.service.file_manager.list_files(pattern)
                return f"Found {len(files)} files:\n" + "\n".join(files)
            except Exception as e:
                logger.error(f"Error listing files with pattern {pattern}: {e}")
                raise
        
        @self.mcp.tool()
        def search_content(query: str) -> str:
            """Search for text across all files"""
            try:
                results = self.service.file_manager.search_content(query)
                if not results:
                    return "No matches found"
                
                content = f"Found {len(results)} matches:\n\n"
                for result in results:
                    content += f"**{result['file_path']}**\n{result['match_preview']}\n\n"
                return content
            except Exception as e:
                logger.error(f"Error searching content for query '{query}': {e}")
                raise
    
    def _register_resources(self):
        """Register all MCP resources using the FastMCP decorator pattern"""
        
        @self.mcp.resource("llm-guide://system/llm-guide.md")
        def llm_usage_guide() -> str:
            """LLM Usage Guide - Comprehensive guide for LLMs on how to effectively use the markdown knowledge management system"""
            try:
                guide_data = self.service.file_manager.read_file("system/llm-guide.md")
                content = guide_data['content']
                if guide_data['metadata']:
                    # Add metadata as frontmatter
                    metadata_str = "\n".join([f"{k}: {v}" for k, v in guide_data['metadata'].items()])
                    content = f"---\n{metadata_str}\n---\n\n{content}"
                return content
            except FileNotFoundError as e:
                raise ValueError(f"Resource not found: llm-guide://system/llm-guide.md - {str(e)}")
            except Exception as e:
                raise ValueError(f"Error reading resource: {str(e)}")
    
    def app(self):
        """Return the FastMCP server instance"""
        return self.mcp

def main():
    parser = argparse.ArgumentParser(description="Markdown Knowledge Base MCP Server")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--knowledge-base", help="Path to knowledge base directory")
    parser.add_argument("--transport", choices=["stdio", "sse", "http"], default="stdio", 
                        help="Transport type: stdio for standard MCP, sse for Server-Sent Events, http for streamable HTTP")
    parser.add_argument("--host", default="localhost", help="Host to bind to (HTTP/SSE only)")
    parser.add_argument("--port", type=int, default=3005, help="Port to bind to (HTTP/SSE only)")
    
    args = parser.parse_args()
    
    # Override config with command line arguments
    if args.knowledge_base:
        os.environ["KNOWLEDGE_BASE_ROOT"] = args.knowledge_base
    
    try:
        mcp_server = MarkdownMCPServer(args.config)
        logger.info(f"Starting MCP server for knowledge base: {mcp_server.config.knowledge_base.root_directory}")
        
        if args.transport == "stdio":
            # Run the FastMCP server with standard I/O
            logger.info("Starting server with stdio transport")
            asyncio.run(mcp_server.mcp.run())
        elif args.transport == "sse":
            # Run the FastMCP server with SSE transport
            logger.info(f"Starting server with SSE transport on {args.host}:{args.port}")
            import uvicorn
            sse_app = mcp_server.mcp.sse_app()
            uvicorn.run(sse_app, host=args.host, port=args.port, log_level="info")
        elif args.transport == "http":
            # Run the FastMCP server with streamable HTTP transport
            logger.info(f"Starting server with streamable HTTP transport on {args.host}:{args.port}")
            import uvicorn
            http_app = mcp_server.mcp.streamable_http_app()
            uvicorn.run(http_app, host=args.host, port=args.port, log_level="info")
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == "__main__":
    main()