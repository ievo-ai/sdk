"""Tests for agent validation."""

from pathlib import Path

import pytest

from ievo_sdk.scaffold.generator import AgentSpec, scaffold_agent
from ievo_sdk.validate.checker import validate_agent


@pytest.fixture
def valid_agent(tmp_path: Path) -> Path:
    spec = AgentSpec(name="test-agent", description="A valid test agent")
    return scaffold_agent(spec, tmp_path)


def test_valid_agent_passes(valid_agent: Path) -> None:
    result = validate_agent(valid_agent)
    assert result.valid
    assert not result.errors


def test_missing_agent_yaml(tmp_path: Path) -> None:
    agent_dir = tmp_path / "broken"
    agent_dir.mkdir()
    (agent_dir / "ROLE.md").write_text("# Test\n\nSome content here for validation.")
    result = validate_agent(agent_dir)
    assert not result.valid
    assert any("agent.yaml" in e for e in result.errors)


def test_missing_role_md(tmp_path: Path) -> None:
    agent_dir = tmp_path / "broken"
    agent_dir.mkdir()
    (agent_dir / "agent.yaml").write_text(
        "name: test\nversion: 0.1.0\ndescription: test\nmodel:\n  primary: sonnet\n"
    )
    result = validate_agent(agent_dir)
    assert not result.valid
    assert any("ROLE.md" in e for e in result.errors)


def test_invalid_model_tier(tmp_path: Path) -> None:
    agent_dir = tmp_path / "broken"
    agent_dir.mkdir()
    (agent_dir / "agent.yaml").write_text(
        "name: test\nversion: 0.1.0\ndescription: test\nmodel:\n  primary: gpt4\n"
    )
    (agent_dir / "ROLE.md").write_text("# Test\n\nResponsibilities and rules here.")
    result = validate_agent(agent_dir)
    assert not result.valid
    assert any("model tier" in e.lower() or "gpt4" in e for e in result.errors)


def test_not_a_directory(tmp_path: Path) -> None:
    f = tmp_path / "notadir.txt"
    f.write_text("hi")
    result = validate_agent(f)
    assert not result.valid


def test_warnings_for_missing_recommended(tmp_path: Path) -> None:
    agent_dir = tmp_path / "minimal"
    agent_dir.mkdir()
    (agent_dir / "agent.yaml").write_text(
        "name: test\nversion: 0.1.0\ndescription: test\nmodel:\n  primary: sonnet\n"
    )
    (agent_dir / "ROLE.md").write_text(
        "# Test Agent\n\n## Responsibilities\n\nDo things.\n\n## Rules\n\n1. Be good.\n"
    )
    result = validate_agent(agent_dir)
    assert result.valid  # warnings don't fail
    assert len(result.warnings) > 0
