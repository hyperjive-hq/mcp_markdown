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
    
    def get_llm_guide(self) -> Dict[str, Any]:
        """Get the LLM guide content, creating it from template if needed"""
        guide_path = "system/llm-guide.md"
        full_path = self.root_path / guide_path
        
        # If guide doesn't exist, create it from template
        if not full_path.exists():
            template_path = Path(__file__).parent / "templates" / "llm-guide-template.md"
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                
                # Create the guide from template
                self.create_file(guide_path, template_content, {
                    "type": "system",
                    "title": "LLM Usage Guide",
                    "generated": datetime.now().isoformat()
                })
        
        # Read and return the guide
        return self.read_file(guide_path)