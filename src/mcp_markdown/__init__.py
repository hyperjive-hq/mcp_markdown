"""
MCP Markdown Server - A Model Context Protocol server for markdown-based knowledge management.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .config import Config, load_config
from .file_operations import FileManager

# Conditionally import server to avoid MCP dependency issues
try:
    from .server import MarkdownMCPServer
    __all__ = ["MarkdownMCPServer", "Config", "load_config", "FileManager"]
except ImportError:
    __all__ = ["Config", "load_config", "FileManager"]