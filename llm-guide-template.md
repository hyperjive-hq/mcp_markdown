# LLM Usage Guide for Knowledge Management System

## Overview
This guide explains how to properly use the markdown-based knowledge management system. As an LLM, you should follow these conventions to ensure consistent behavior that matches user expectations.

## File Organization Rules

### Directory Structure
- **`inbox/`**: Temporary capture area for quick notes that need to be processed later
- **`tasks/`**: All task-related files
  - `tasks/active/`: Current tasks that need attention
  - `tasks/completed/`: Finished tasks (archived monthly)
  - `tasks/projects/`: Project-specific task collections
- **`notes/`**: Knowledge base and reference materials
  - `notes/daily/`: Daily notes with format YYYY-MM-DD.md
  - `notes/topics/`: Subject-based notes organized by topic
  - `notes/references/`: Reference materials and documentation
- **`calendar/`**: Time-based items
  - `calendar/appointments/`: Scheduled meetings and events
  - `calendar/reminders/`: Future reminders and alerts

### File Placement Rules
1. **New tasks**: Always create in `tasks/active/` unless part of a specific project
2. **Quick notes**: Use `inbox/` for immediate capture, then move to appropriate location
3. **Meeting notes**: Create in `notes/topics/` with appropriate tags
4. **Daily planning**: Use `notes/daily/` with today's date
5. **Reference materials**: Store in `notes/references/` with descriptive names

## Tagging System

### Standard Tags
- **Priority**: `high`, `medium`, `low`
- **Status**: `todo`, `in-progress`, `completed`, `cancelled`, `on-hold`
- **Context**: `work`, `personal`, `project`, `meeting`, `research`
- **Type**: `bug`, `feature`, `documentation`, `maintenance`, `idea`
- **Time**: `urgent`, `this-week`, `next-week`, `someday`

### Tag Usage Rules
1. **Always include a priority tag** for tasks
2. **Use context tags** to help with filtering
3. **Combine tags meaningfully** (e.g., `[work, high, urgent]`)
4. **Keep tags lowercase** and use hyphens for multi-word tags
5. **Limit to 5-7 tags per file** to avoid over-tagging

## Metadata Standards

### Required Fields by Type

#### Tasks
- `type: task` (required)
- `title` (required)
- `status` (required)
- `priority` (required)
- `created` (required)
- `tags` (recommended)

#### Notes
- `type: note` (required)
- `title` (required)
- `topic` (recommended)
- `created` (required)
- `tags` (recommended)

#### Appointments
- `type: appointment` (required)
- `title` (required)
- `date` (required)
- `time` (required)
- `status` (required)

### Optional but Useful Fields
- `due`: For tasks with deadlines
- `estimated_hours`: For time planning
- `project`: To group related items
- `related_notes`: For cross-references
- `source`: For reference materials

## File Naming Conventions

### Naming Patterns
- **Tasks**: `YYYY-MM-DD-task-slug.md`
- **Notes**: `topic-slug.md` or `YYYY-MM-DD-note-slug.md`
- **Daily notes**: `YYYY-MM-DD.md`
- **Appointments**: `YYYY-MM-DD-HH-MM-appointment-slug.md`
- **Projects**: `project-slug.md`

### Naming Rules
1. **Use lowercase** with hyphens for spaces
2. **Include dates** when chronological order matters
3. **Keep names descriptive** but concise (under 50 characters)
4. **Avoid special characters** except hyphens and underscores
5. **Be consistent** with existing naming patterns

## Cross-Reference Patterns

### Linking Conventions
- **Wiki-style links**: `[[filename]]` for internal references
- **Markdown links**: `[Description](path/to/file.md)` for external references
- **Tag references**: Use `#tag-name` to reference tags
- **Date references**: `[[2024-01-15]]` for daily notes

### When to Create Links
1. **Related tasks**: Link tasks that depend on each other
2. **Follow-up items**: Link notes to tasks they generate
3. **Project relationships**: Link all items within a project
4. **Reference materials**: Link to supporting documentation
5. **Meeting outcomes**: Link meeting notes to resulting tasks

## User Expectations

### Task Management
- **Creating tasks**: Users expect clear, actionable descriptions
- **Updating status**: Status changes should be immediate and accurate
- **Priority setting**: High priority means urgent attention needed
- **Due dates**: Respect deadlines and provide reminders
- **Dependencies**: Track task relationships and blocking issues

### Note Taking
- **Structure**: Users expect consistent formatting and organization
- **Searchability**: Include relevant keywords and tags
- **Linking**: Connect related information appropriately
- **Updates**: Keep modification dates current
- **Context**: Provide sufficient background for future reference

### Calendar Management
- **Scheduling**: Respect time zones and availability
- **Reminders**: Set appropriate reminder times
- **Conflicts**: Check for scheduling conflicts
- **Details**: Include necessary location and attendee information
- **Follow-up**: Create tasks for meeting outcomes

## Workflow Patterns

### Common Sequences

#### Task Creation Flow
1. Create task in `tasks/active/`
2. Set appropriate metadata (priority, tags, due date)
3. Link to related notes or projects
4. Add to appropriate project file if needed

#### Note Processing Flow
1. Quick capture in `inbox/`
2. Process and categorize
3. Move to appropriate directory
4. Add proper tags and metadata
5. Link to related content

#### Meeting Workflow
1. Create appointment in `calendar/appointments/`
2. Take notes in `notes/topics/` during meeting
3. Create follow-up tasks in `tasks/active/`
4. Link meeting notes to resulting tasks
5. Update project status if applicable

#### Daily Planning Flow
1. Create daily note in `notes/daily/`
2. Review active tasks and priorities
3. Check calendar for appointments
4. Plan day's activities
5. Link to relevant projects and tasks

### Error Prevention
- **Always validate metadata** before creating files
- **Check for existing files** before creating duplicates
- **Maintain link integrity** when moving or renaming files
- **Use templates** to ensure consistent structure
- **Update timestamps** when modifying files

## Best Practices

### File Management
1. **Use templates** for consistent file structure
2. **Archive completed items** regularly
3. **Clean up broken links** during maintenance
4. **Backup important files** before major changes
5. **Maintain directory organization** as system grows

### Content Quality
1. **Write clear, actionable descriptions**
2. **Include sufficient context** for future reference
3. **Use consistent formatting** within files
4. **Tag appropriately** for discoverability
5. **Link related content** to build knowledge connections

### System Maintenance
1. **Validate links** periodically
2. **Update tag taxonomy** as needed
3. **Archive old completed items**
4. **Monitor system performance**
5. **Keep documentation current**

## When to Ask for Clarification

### Ambiguous Requests
- Unclear task descriptions
- Missing priority information
- Vague due dates
- Conflicting requirements

### System Conflicts
- Duplicate file creation
- Scheduling conflicts
- Broken link resolution
- Metadata inconsistencies

### User Preferences
- Tagging preferences
- File organization preferences
- Workflow customizations
- Notification settings

Remember: The goal is to maintain a clean, organized, and useful knowledge management system that serves both human and AI users effectively.