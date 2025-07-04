---
generated: '2025-07-04T05:31:18.526956'
title: LLM Usage Guide
type: system
---

# LLM Usage Guide for Knowledge Management System

## Overview
This knowledge base uses a flexible directory structure with only one requirement: a `system/` directory for configuration and templates.

## Directory Structure
Current structure:
- test-knowledge-base/
  - my-todos.md
  - system/
    - llm-guide.md
    - templates/
      - note.template.md
  - test/
    - example.md

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
- note