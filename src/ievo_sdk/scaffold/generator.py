"""Scaffold a new agent package from templates."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).parent.parent / "template"


@dataclass
class AgentSpec:
    """Specification for a new agent."""

    name: str
    description: str = "A custom iEvo agent"
    display_name: str = ""
    author: str = "iEvo"
    category: str = "community"
    model: str = "sonnet"
    specialty: str = "general tasks"
    primary_responsibility: str = "Complete assigned tasks accurately"
    primary_output: str = "Task artifacts as specified"
    upstream_agent: str = ""
    dependencies: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.display_name:
            self.display_name = self.name.replace("-", " ").title()


def scaffold_agent(spec: AgentSpec, output_dir: Path) -> Path:
    """Generate a complete agent package from spec.

    Args:
        spec: Agent specification.
        output_dir: Parent directory (agent dir will be created inside).

    Returns:
        Path to the created agent directory.
    """
    agent_dir = output_dir / spec.name
    agent_dir.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        keep_trailing_newline=True,
    )

    context = {
        "name": spec.name,
        "display_name": spec.display_name,
        "description": spec.description,
        "author": spec.author,
        "category": spec.category,
        "model": spec.model,
        "specialty": spec.specialty,
        "primary_responsibility": spec.primary_responsibility,
        "primary_output": spec.primary_output,
        "upstream_agent": spec.upstream_agent,
        "dependencies": spec.dependencies or [],
    }

    # Render Jinja2 templates
    for template_name in ["agent.yaml.j2", "ROLE.md.j2"]:
        template = env.get_template(template_name)
        output_name = template_name.removesuffix(".j2")
        (agent_dir / output_name).write_text(template.render(**context))

    # Copy static files
    _copy_static(agent_dir, "EVOLUTION_LOG.md")
    _copy_static_dir(agent_dir, "memory")
    _copy_static_dir(agent_dir, "skills")

    return agent_dir


def _copy_static(agent_dir: Path, filename: str) -> None:
    """Copy a static template file."""
    src = TEMPLATE_DIR / filename
    if src.exists():
        shutil.copy2(src, agent_dir / filename)


def _copy_static_dir(agent_dir: Path, dirname: str) -> None:
    """Copy a static template directory."""
    src = TEMPLATE_DIR / dirname
    dst = agent_dir / dirname
    if src.exists():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
