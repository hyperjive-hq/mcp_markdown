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