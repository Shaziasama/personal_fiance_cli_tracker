# main.py
import typer
from app.database.engine import create_db_and_tables
from app.commands import log, view

app = typer.Typer(
    name="fintrack",
    help="A professional Personal Finance CLI using Python and Google Gemini AI.",
    add_completion=False,
)

@app.callback()
def main():
    """
    FinTrack Pro: Your personal finance CLI.
    """
    create_db_and_tables()

app.add_typer(log.app, name="log")
app.add_typer(view.app, name="view")

if __name__ == "__main__":
    app()