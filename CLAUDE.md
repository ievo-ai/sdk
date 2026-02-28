# iEvo SDK

Developer toolkit for building self-evolving agents.

## Project

- **Name**: ievo-sdk
- **Language**: Python 3.10+
- **Framework**: Jinja2 (templates) + jsonschema (validation) + Rich (CLI output)
- **Package manager**: uv (hatchling build)
- **Entry point**: `ievo-sdk` → `src/ievo_sdk/cli.py`

## Architecture

```
src/ievo_sdk/
├── cli.py              # CLI entry point (new, validate, info)
├── scaffold/
│   ├── __init__.py
│   └── generator.py    # AgentSpec + scaffold_agent() — Jinja2 rendering
├── validate/
│   ├── __init__.py
│   └── checker.py      # validate_agent() — schema + structure checks
└── template/           # Jinja2 templates + static files
    ├── agent.yaml.j2   # Agent manifest template
    ├── ROLE.md.j2      # Agent instructions template
    ├── EVOLUTION_LOG.md
    ├── memory/         # Memory templates (CONTEXT, DECISIONS, VOCABULARY, HISTORY)
    └── skills/
        └── evo/
            └── SKILL.md  # Self-evolution skill

schemas/
└── agent.schema.json   # JSON Schema for agent.yaml

tests/
├── test_scaffold.py    # 7 tests — scaffold generation
└── test_validate.py    # 6 tests — validation
```

## Key patterns

- **AgentSpec** dataclass defines all agent parameters, auto-generates display_name
- **scaffold_agent(spec, output_dir)** renders Jinja2 templates + copies static files
- **validate_agent(agent_dir)** returns ValidationResult with errors/warnings/info
- **Schema**: JSON Schema at schemas/agent.schema.json, used by jsonschema lib
- **CLI**: argparse-style (no Typer) to keep dependencies light

## Commands

```bash
ievo-sdk new <name>         # Interactive scaffold — prompts for description, model, etc.
ievo-sdk validate <dir>     # Validate agent package — errors, warnings, info
ievo-sdk info <dir>         # Show agent metadata table
ievo-sdk --version          # Show version
```

## Running tests

```bash
pytest tests/ -v
```

## Related repos

- [ievo-ai/cli](https://github.com/ievo-ai/cli) — CLI tool (`ievo dev new` also scaffolds agents)
- [ievo-ai/marketplace](https://github.com/ievo-ai/marketplace) — Agent registry
- [ievo.ai](https://ievo.ai) — Project homepage

## Conventions

- Templates use Jinja2 (.j2 extension for rendered, plain for static)
- Validation returns structured ValidationResult, never raises
- CLI uses Rich for output formatting
- Tests use pytest fixtures with tmp_path
