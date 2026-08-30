"""Shared Rich console formatting for the workshop scripts."""

from rich.console import Console

console = Console(highlight=False)

STEP_STYLE = "bold cyan"
INFO_STYLE = "green"


def print_step(title: str) -> None:
    """Print a clearly separated workshop step heading."""
    separator = "=" * max(1, console.width // 2)
    console.print(f"\n{separator}\n{title}\n{separator}", style=STEP_STYLE)


def print_result(result: object) -> None:
    """Print result content between uncolored delimiter lines."""
    separator = "-" * max(1, console.width // 2)
    console.print(separator)
    console.print(result, markup=False)
    console.print(separator)
