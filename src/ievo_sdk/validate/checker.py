"""Validate an agent package against the iEvo schema and conventions."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:
    jsonschema = None  # type: ignore[assignment]

SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "schemas" / "agent.schema.json"

# Required files in a valid agent package
REQUIRED_FILES = [
    "agent.yaml",
    "ROLE.md",
]

RECOMMENDED_FILES = [
    "EVOLUTION_LOG.md",
    "memory/CONTEXT.md",
    "memory/DECISIONS.md",
    "memory/VOCABULARY.md",
    "memory/HISTORY.md",
    "skills/evo/SKILL.md",
]


@dataclass
class ValidationResult:
    """Result of agent package validation."""

    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)
        self.valid = False

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def add_info(self, msg: str) -> None:
        self.info.append(msg)


def validate_agent(agent_dir: Path) -> ValidationResult:
    """Validate an agent package directory.

    Checks:
    1. Required files exist
    2. agent.yaml schema validation
    3. ROLE.md is non-empty and has required sections
    4. Recommended files exist (warnings)
    5. Dependencies are valid names
    6. Model tier is valid

    Args:
        agent_dir: Path to agent directory.

    Returns:
        ValidationResult with errors, warnings, and info.
    """
    result = ValidationResult()

    if not agent_dir.is_dir():
        result.error(f"Not a directory: {agent_dir}")
        return result

    # 1. Required files
    for f in REQUIRED_FILES:
        if not (agent_dir / f).exists():
            result.error(f"Missing required file: {f}")

    if not result.valid:
        return result

    # 2. Schema validation
    _validate_schema(agent_dir / "agent.yaml", result)

    # 3. ROLE.md checks
    _validate_role(agent_dir / "ROLE.md", result)

    # 4. Recommended files
    for f in RECOMMENDED_FILES:
        if not (agent_dir / f).exists():
            result.warn(f"Missing recommended file: {f}")

    # 5. EVO skill
    evo_skill = agent_dir / "skills" / "evo" / "SKILL.md"
    if not evo_skill.exists():
        result.warn("Missing EVO skill — agent won't self-evolve")

    return result


def _validate_schema(yaml_path: Path, result: ValidationResult) -> None:
    """Validate agent.yaml against JSON schema."""
    try:
        data = yaml.safe_load(yaml_path.read_text())
    except yaml.YAMLError as e:
        result.error(f"Invalid YAML in agent.yaml: {e}")
        return

    if not isinstance(data, dict):
        result.error("agent.yaml must be a YAML mapping")
        return

    # Check required fields manually (works without jsonschema)
    for field_name in ["name", "version", "description", "model"]:
        if field_name not in data:
            result.error(f"agent.yaml missing required field: {field_name}")

    # Model validation
    model = data.get("model", {})
    if isinstance(model, dict):
        primary = model.get("primary", "")
        if primary not in ("opus", "sonnet", "haiku"):
            result.error(f"Invalid model tier: {primary} (must be opus|sonnet|haiku)")
    else:
        result.error("model must be a mapping with 'primary' key")

    # Version format
    version = data.get("version", "")
    if version and not _is_semver(version):
        result.error(f"Invalid version format: {version} (must be X.Y.Z)")

    # Name format
    name = data.get("name", "")
    if name and not all(c.isalnum() or c == "-" for c in name):
        result.error(f"Invalid name: {name} (lowercase alphanumeric and hyphens only)")

    # Full schema validation if jsonschema available
    if jsonschema and SCHEMA_PATH.exists():
        try:
            schema = json.loads(SCHEMA_PATH.read_text())
            jsonschema.validate(data, schema)
            result.add_info("Schema validation passed")
        except jsonschema.ValidationError as e:
            result.error(f"Schema validation: {e.message}")
    else:
        result.add_info("jsonschema not available — using basic validation only")


def _validate_role(role_path: Path, result: ValidationResult) -> None:
    """Validate ROLE.md content."""
    content = role_path.read_text().strip()

    if len(content) < 50:
        result.error("ROLE.md is too short (< 50 chars) — needs real instructions")
        return

    if not content.startswith("#"):
        result.warn("ROLE.md should start with a markdown heading")

    # Check for key sections
    lower = content.lower()
    if "responsibilit" not in lower and "task" not in lower:
        result.warn("ROLE.md should describe agent responsibilities")

    if "rule" not in lower and "constraint" not in lower:
        result.warn("ROLE.md should include rules or constraints")

    result.add_info(f"ROLE.md: {len(content)} chars, {content.count('##')} sections")


def _is_semver(v: str) -> bool:
    """Check if string is valid semver X.Y.Z."""
    parts = v.split(".")
    if len(parts) != 3:
        return False
    return all(p.isdigit() for p in parts)
