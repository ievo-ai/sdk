# iEvo SDK

Developer toolkit for building self-evolving iEvo agents.

## Install

```bash
# uv (recommended)
uv pip install ievo-sdk

# pip
pip install ievo-sdk

# dev
git clone https://github.com/ievo-ai/sdk.git
cd sdk
uv pip install -e ".[dev]"
```

## Commands

```bash
# Scaffold a new agent
ievo-sdk new my-agent

# Validate an agent package
ievo-sdk validate agents/my-agent

# Show agent info
ievo-sdk info agents/my-agent
```

## What it generates

```
my-agent/
├── agent.yaml           # Package manifest (name, version, model, deps)
├── ROLE.md              # Agent instructions (progressive disclosure L2)
├── EVOLUTION_LOG.md     # Self-evolution history
├── memory/
│   ├── CONTEXT.md       # Project context (filled on first session)
│   ├── DECISIONS.md     # Architecture decisions log
│   ├── VOCABULARY.md    # Domain terminology
│   └── HISTORY.md       # Session history
└── skills/
    └── evo/
        └── SKILL.md     # Self-evolution skill (every agent has it)
```

## Validation

The SDK validates:
- **Required files** — `agent.yaml` and `ROLE.md` must exist
- **Schema** — `agent.yaml` conforms to the agent package schema
- **ROLE.md quality** — must have sufficient content, headings, responsibilities
- **Recommended files** — memory templates, EVO skill (warnings)
- **Model tiers** — must be `opus`, `sonnet`, or `haiku`
- **Semver** — version must be `X.Y.Z` format

## Programmatic usage

```python
from ievo_sdk.scaffold import scaffold_agent
from ievo_sdk.scaffold.generator import AgentSpec
from ievo_sdk.validate import validate_agent

# Create an agent
spec = AgentSpec(
    name="code-reviewer",
    description="Reviews pull requests for quality and consistency",
    model="sonnet",
    category="dev",
    specialty="code review",
)
agent_dir = scaffold_agent(spec, Path("agents"))

# Validate it
result = validate_agent(agent_dir)
assert result.valid
```

## Related

- [ievo-ai/cli](https://github.com/ievo-ai/cli) — iEvo CLI tool
- [ievo-ai/marketplace](https://github.com/ievo-ai/marketplace) — Agent registry
- [ievo.ai](https://ievo.ai) — Project homepage
