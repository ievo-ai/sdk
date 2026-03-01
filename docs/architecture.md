# SDK Architecture

## Overview

ievo-sdk provides tooling for creating, validating, and inspecting agent packages in the iEvo ecosystem. It is the standard way to scaffold new agents and ensure they conform to the marketplace format.

## Core Commands

| Command | Module | Purpose |
|---------|--------|---------|
| `ievo-sdk new <name>` | `scaffold.py` | Generate a new agent package from templates |
| `ievo-sdk validate <path>` | `validate.py` | Check structure and schema compliance |
| `ievo-sdk inspect <path>` | `inspect.py` | Display agent metadata and capabilities |

## Stack

- **Language**: Python 3.13+
- **CLI framework**: Typer
- **Templating**: Jinja2 (agent package generation)
- **Validation**: JSON Schema (`schemas/agent.schema.json` validates `agent.yaml`)
- **Package manager**: uv (hatchling build)

## Project Structure

```
src/ievo_sdk/
├── scaffold.py         # Agent package generation from Jinja2 templates
├── validate.py         # Structure + schema validation
└── inspect.py          # Metadata display

templates/              # Jinja2 templates for agent packages
├── agent.yaml.j2
├── ROLE.md.j2
├── EVOLUTION_LOG.md.j2
├── memory/
│   ├── CONTEXT.md.j2
│   ├── DECISIONS.md.j2
│   ├── VOCABULARY.md.j2
│   └── HISTORY.md.j2
└── skills/evo/SKILL.md.j2

schemas/
└── agent.schema.json   # JSON Schema for agent.yaml validation
```

## Template System

Templates generate the standard agent package format:

```
agents/{name}/
├── agent.yaml
├── ROLE.md
├── EVOLUTION_LOG.md
├── memory/
│   ├── CONTEXT.md
│   ├── DECISIONS.md
│   ├── VOCABULARY.md
│   └── HISTORY.md
└── skills/evo/SKILL.md
```

The `scaffold.py` module renders Jinja2 templates with user-provided values (agent name, description, model tier, etc.) to produce a complete, valid agent package ready for development.

## Validation

`validate.py` performs two checks:

1. **Structure validation** — verifies all required files and directories exist
2. **Schema validation** — validates `agent.yaml` against `schemas/agent.schema.json` (fields: name, version, description, author, model, dependencies, skills, hooks)
