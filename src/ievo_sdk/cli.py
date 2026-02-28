"""iEvo SDK CLI — developer tools for building agents."""

from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def main() -> None:
    """Entry point for ievo-sdk CLI."""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        _show_help()
        return

    cmd = args[0]

    if cmd == "new":
        _cmd_new(args[1:])
    elif cmd == "validate":
        _cmd_validate(args[1:])
    elif cmd == "info":
        _cmd_info(args[1:])
    elif cmd == "--version":
        from ievo_sdk import __version__
        console.print(f"ievo-sdk {__version__}")
    else:
        console.print(f"[red]Unknown command: {cmd}[/red]")
        _show_help()
        sys.exit(1)


def _show_help() -> None:
    """Display help."""
    console.print(Panel.fit(
        "[bold green]iEvo SDK[/bold green] — developer toolkit for building agents\n\n"
        "Commands:\n"
        "  [bold]new[/bold] <name>       Scaffold a new agent package\n"
        "  [bold]validate[/bold] <dir>   Validate an agent package\n"
        "  [bold]info[/bold] <dir>       Show agent package info\n"
        "  [bold]--version[/bold]        Show version",
        title="ievo-sdk",
    ))


def _cmd_new(args: list[str]) -> None:
    """Scaffold a new agent."""
    if not args:
        console.print("[red]Usage: ievo-sdk new <name> [--dir <output>][/red]")
        sys.exit(1)

    name = args[0]
    output_dir = Path(".")

    # Parse --dir
    if "--dir" in args:
        idx = args.index("--dir")
        if idx + 1 < len(args):
            output_dir = Path(args[idx + 1])

    from ievo_sdk.scaffold import scaffold_agent
    from ievo_sdk.scaffold.generator import AgentSpec

    console.print(f"\n[bold]Scaffolding agent:[/bold] {name}\n")

    # Interactive prompts
    description = _prompt("Description", f"A custom {name} agent")
    category = _prompt("Category [core/dev/ops/data/security/community]", "community")
    model = _prompt("Model tier [opus/sonnet/haiku]", "sonnet")
    specialty = _prompt("Specialty", name.replace("-", " "))

    spec = AgentSpec(
        name=name,
        description=description,
        category=category,
        model=model,
        specialty=specialty,
    )

    agent_dir = scaffold_agent(spec, output_dir)
    console.print(f"\n[green]✓[/green] Agent created at [bold]{agent_dir}[/bold]")
    console.print(f"  Edit [cyan]ROLE.md[/cyan] to define behavior")
    console.print(f"  Edit [cyan]agent.yaml[/cyan] to configure settings")
    console.print(f"  Run [cyan]ievo-sdk validate {agent_dir}[/cyan] to check\n")


def _cmd_validate(args: list[str]) -> None:
    """Validate an agent package."""
    if not args:
        console.print("[red]Usage: ievo-sdk validate <agent-dir>[/red]")
        sys.exit(1)

    agent_dir = Path(args[0])

    from ievo_sdk.validate import validate_agent

    result = validate_agent(agent_dir)

    if result.errors:
        console.print(f"\n[red bold]✗ Validation failed[/red bold] — {len(result.errors)} error(s)\n")
        for e in result.errors:
            console.print(f"  [red]✗[/red] {e}")
    else:
        console.print(f"\n[green bold]✓ Valid agent package[/green bold]\n")

    if result.warnings:
        for w in result.warnings:
            console.print(f"  [yellow]⚠[/yellow] {w}")

    if result.info:
        for i in result.info:
            console.print(f"  [dim]ℹ {i}[/dim]")

    console.print()
    sys.exit(0 if result.valid else 1)


def _cmd_info(args: list[str]) -> None:
    """Show agent package info."""
    if not args:
        console.print("[red]Usage: ievo-sdk info <agent-dir>[/red]")
        sys.exit(1)

    agent_dir = Path(args[0])
    yaml_path = agent_dir / "agent.yaml"

    if not yaml_path.exists():
        console.print(f"[red]No agent.yaml in {agent_dir}[/red]")
        sys.exit(1)

    import yaml
    data = yaml.safe_load(yaml_path.read_text())

    table = Table(title=f"Agent: {data.get('name', '?')}", show_header=False, padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()

    table.add_row("Version", data.get("version", "?"))
    table.add_row("Description", data.get("description", ""))
    table.add_row("Category", data.get("category", "?"))
    table.add_row("Author", data.get("author", "?"))

    model = data.get("model", {})
    if isinstance(model, dict):
        model_str = model.get("primary", "?")
        if model.get("fallback"):
            model_str += f" → {model['fallback']}"
        table.add_row("Model", model_str)

    deps = data.get("dependencies", [])
    table.add_row("Dependencies", ", ".join(deps) if deps else "none")

    # File inventory
    files = list(agent_dir.rglob("*"))
    md_files = [f for f in files if f.suffix == ".md"]
    yaml_files = [f for f in files if f.suffix in (".yaml", ".yml")]
    table.add_row("Files", f"{len(files)} total ({len(md_files)} .md, {len(yaml_files)} .yaml)")

    evo_log = agent_dir / "EVOLUTION_LOG.md"
    if evo_log.exists():
        evo_count = evo_log.read_text().count("\n## ")
        table.add_row("Evolutions", str(evo_count) if evo_count else "none yet")

    console.print()
    console.print(table)
    console.print()


def _prompt(label: str, default: str) -> str:
    """Prompt with default value."""
    try:
        value = input(f"  {label} [{default}]: ").strip()
        return value if value else default
    except (EOFError, KeyboardInterrupt):
        return default


if __name__ == "__main__":
    main()
