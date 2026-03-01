# SDK Usage

## Installation

```bash
# Install globally
uv pip install ievo-sdk

# Or run without installing
uvx ievo-sdk
```

## Creating a New Agent

```bash
ievo-sdk new my-agent
```

Scaffolds a complete agent package in `./my-agent/` using Jinja2 templates. The command walks through an interactive prompt for:

- Agent name and description
- Model tier (haiku / sonnet / opus)
- Initial skills and dependencies

Output:

```
my-agent/
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

## Validating an Agent

```bash
ievo-sdk validate agents/my-agent/
```

Checks:

- All required files exist (agent.yaml, ROLE.md, memory/, skills/evo/)
- `agent.yaml` conforms to JSON Schema (`schemas/agent.schema.json`)
- Required fields are present and correctly typed

Returns exit code 0 on success, 1 on validation failure with details.

## Inspecting an Agent

```bash
ievo-sdk inspect agents/my-agent/
```

Displays agent metadata from `agent.yaml`:

- Name, version, description, author
- Model configuration (primary + fallback)
- Dependencies and MCP requirements
- Registered skills and hooks
- Evolution log entry count
