# app/utils/ui.py
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

def print_table(
    title: str,
    columns: list[str],
    rows: list[list[str]],
    show_header: bool = True,
    show_row_numbers: bool = False,
    box: bool = True
):
    """
    Prints a stylized table to the console.

    Args:
        title (str): The title of the table.
        columns (list[str]): A list of column headers.
        rows (list[list[str]]): A list of lists, where each inner list represents a row.
        show_header (bool): Whether to show the header row. Defaults to True.
        show_row_numbers (bool): Whether to show row numbers. Defaults to False.
        box (bool): Whether to draw a box around the table. Defaults to True.
    """
    table = Table(
        title=title,
        show_header=show_header,
        show_row_numbers=show_row_numbers,
        box=box,
        header_style="bold magenta"
    )

    for col in columns:
        table.add_column(col)

    for row in rows:
        table.add_row(*row)

    console.print(table)


def print_success(message: str):
    """
    Prints a success message to the console.
    """
    console.print(f"[bold green]✔[/bold green] {message}")


def print_error(message: str):
    """
    Prints an error message to the console.
    """
    console.print(f"[bold red]✖[/bold red] {message}")


def print_info(message: str):
    """
    Prints an informational message to the console.
    """
    console.print(f"[bold blue]ℹ[/bold blue] {message}")

