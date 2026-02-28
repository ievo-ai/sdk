"""Tests for agent scaffolding."""

from pathlib import Path

import pytest

from ievo_sdk.scaffold.generator import AgentSpec, scaffold_agent


@pytest.fixture
def tmp_output(tmp_path: Path) -> Path:
    return tmp_path / "agents"


def test_scaffold_creates_directory(tmp_output: Path) -> None:
    spec = AgentSpec(name="test-agent")
    result = scaffold_agent(spec, tmp_output)
    assert result.is_dir()
    assert result.name == "test-agent"


def test_scaffold_creates_required_files(tmp_output: Path) -> None:
    spec = AgentSpec(name="test-agent", description="A test agent")
    agent_dir = scaffold_agent(spec, tmp_output)

    assert (agent_dir / "agent.yaml").exists()
    assert (agent_dir / "ROLE.md").exists()
    assert (agent_dir / "EVOLUTION_LOG.md").exists()


def test_scaffold_creates_memory(tmp_output: Path) -> None:
    spec = AgentSpec(name="test-agent")
    agent_dir = scaffold_agent(spec, tmp_output)

    for f in ["CONTEXT.md", "DECISIONS.md", "VOCABULARY.md", "HISTORY.md"]:
        assert (agent_dir / "memory" / f).exists()


def test_scaffold_creates_evo_skill(tmp_output: Path) -> None:
    spec = AgentSpec(name="test-agent")
    agent_dir = scaffold_agent(spec, tmp_output)
    assert (agent_dir / "skills" / "evo" / "SKILL.md").exists()


def test_scaffold_renders_agent_yaml(tmp_output: Path) -> None:
    spec = AgentSpec(
        name="my-agent",
        description="Does things",
        model="opus",
        category="dev",
    )
    agent_dir = scaffold_agent(spec, tmp_output)
    content = (agent_dir / "agent.yaml").read_text()

    assert "name: my-agent" in content
    assert "Does things" in content
    assert "primary: opus" in content
    assert "category: dev" in content


def test_scaffold_renders_role_md(tmp_output: Path) -> None:
    spec = AgentSpec(
        name="my-agent",
        description="Does things",
        specialty="code review",
    )
    agent_dir = scaffold_agent(spec, tmp_output)
    content = (agent_dir / "ROLE.md").read_text()

    assert "My Agent" in content  # display_name
    assert "code review" in content


def test_display_name_auto_generated() -> None:
    spec = AgentSpec(name="code-reviewer")
    assert spec.display_name == "Code Reviewer"
