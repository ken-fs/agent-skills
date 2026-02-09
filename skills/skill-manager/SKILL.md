---
name: skill-manager
description: Manage and inspect skills in the skills directory. List all skills with names and descriptions, generate statistical reports (skill counts, resource distribution), and validate skill integrity (check SKILL.md format, frontmatter, required fields). Use when user wants to view available skills, check skill statistics, or verify skill completeness.
---

# Skill Manager

Comprehensive tool for managing and inspecting skills in your skills directory.

## Features

- **List Skills** - Display all skills with names and descriptions
- **Generate Statistics** - Show skill counts and resource distribution
- **Validate Skills** - Check skill integrity and compliance

## Usage

All commands use the `skill_manager.py` script:

```bash
python scripts/skill_manager.py <command> [options]
```

### List All Skills

Display all skills with their names and descriptions:

```bash
python scripts/skill_manager.py list
```

Show detailed information including resource counts:

```bash
python scripts/skill_manager.py list --verbose
```

Example output:
```
1. [notebooklm](notebooklm/SKILL.md)
   Use this skill to query your Google NotebookLM notebooks...
   Resources: 5 scripts, 3 references

2. [pdf-editor](pdf-editor/SKILL.md)
   Comprehensive PDF manipulation toolkit...
   Resources: 8 scripts
```

### Generate Statistics Report

Display comprehensive statistics about all skills:

```bash
python scripts/skill_manager.py stats
```

Example output:
```
Total Skills: 8
  [OK] Valid: 8
  [X] Invalid: 0

Resource Distribution:
  Scripts: 19 total (4 skills)
  References: 11 total (3 skills)
  Assets: 1 total (1 skills)

Average Resources per Skill:
  Scripts: 2.4
  References: 1.4
  Assets: 0.1
```

### Validate Skills

Check all skills for completeness and compliance:

```bash
python scripts/skill_manager.py validate
```

Show both valid and invalid skills:

```bash
python scripts/skill_manager.py validate --show-valid
```

The validation checks:
- SKILL.md file exists
- Valid YAML frontmatter format
- Required fields present (`name`, `description`)
- Description quality (length, "when to use" context)
- Unnecessary files (README.md, CHANGELOG.md, etc.)

Example output:
```
[X] my-skill
  [ERROR] Missing required field: 'description'
  [!] Description is quite short (25 chars)
  [!] Unnecessary file found: README.md
```

## Command Reference

| Command | Description | Options |
|---------|-------------|---------|
| `list` | List all skills | `--verbose` for detailed info |
| `stats` | Generate statistics | None |
| `validate` | Validate all skills | `--show-valid` to show valid skills |

### Common Options

- `--skills-dir <path>` - Specify custom skills directory (default: auto-detect)
- `--verbose` or `-v` - Show detailed information
- `--show-valid` - Include valid skills in validation report

## Auto-Detection

The script automatically detects the skills directory by looking at its parent directory structure. You can override this with `--skills-dir`:

```bash
python scripts/skill_manager.py list --skills-dir /path/to/skills
```

## Validation Rules

The validator checks for:

**Required:**
- SKILL.md file with valid YAML frontmatter
- `name` field in frontmatter
- `description` field in frontmatter (minimum 50 characters recommended)

**Warnings:**
- Short descriptions (< 50 characters)
- Missing "when to use" context in description
- Extra frontmatter fields beyond `name` and `description`
- Unnecessary documentation files (README.md, CHANGELOG.md, etc.)

## Workflow Examples

**View all skills:**
```bash
python scripts/skill_manager.py list --verbose
```

**Check skill quality:**
```bash
python scripts/skill_manager.py validate --show-valid
```

**Quick overview:**
```bash
python scripts/skill_manager.py stats
```
