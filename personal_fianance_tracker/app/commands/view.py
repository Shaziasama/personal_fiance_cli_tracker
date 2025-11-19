# app/commands/view.py
import typer
from typing import List
from sqlmodel import Session, select
from rich.console import Console

from app.database.engine import get_session
from app.models.transaction import Transaction
from app.utils.ui import print_table, print_error, print_info

app = typer.Typer(help="Commands for viewing financial data.")
console = Console()

@app.command(name="list")
def list_transactions(
    limit: int = typer.Option(10, "--limit", "-l", help="Number of latest transactions to display.")
):
    """
    Lists the latest transactions.
    """
    transactions: List[Transaction] = []
    try:
        with get_session() as session: # Corrected call to get_session
            transactions = session.exec(
                select(Transaction).order_by(Transaction.date.desc()).limit(limit)
            ).all()

        if not transactions:
            print_info("No transactions found.")
            return

        columns = ["ID", "Date", "Description", "Category", "Type", "Amount"]
        rows = []
        for t in transactions:
            rows.append(
                [
                    str(t.id),
                    t.date.strftime("%Y-%m-%d %H:%M"),
                    t.description,
                    t.category.value,
                    t.transaction_type.value,
                    f"{t.amount}",
                ]
            )
        
        print_table(
            title=f"Latest {len(transactions)} Transactions",
            columns=columns,
            rows=rows,
            show_row_numbers=False,
            box=True
        )

    except Exception as e:
        print_error(f"Failed to fetch transactions: {e}")

@app.command(name="dashboard")
def view_dashboard():
    """
    Displays an overview of financial data (placeholder for future development).
    """
    print_info("Dashboard functionality is coming soon!")


if __name__ == "__main__":
    app()
