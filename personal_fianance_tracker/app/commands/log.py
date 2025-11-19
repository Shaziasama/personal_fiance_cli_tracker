# app/commands/log.py
import typer
from datetime import datetime
from typing import Optional
from sqlmodel import Session, select
from rich.console import Console

from app.database.engine import get_session
from app.models.transaction import Transaction, TransactionType, TransactionCategory
from app.services.ai_service import AIService
from app.utils.ui import print_success, print_error, print_info

app = typer.Typer(help="Commands for logging and adding transactions.")
console = Console()
ai_service = AIService()

@app.command(name="add")
def add_transaction(
    amount: int = typer.Option(..., "--amount", "-a", help="Amount of the transaction (integer only)."),
    category: TransactionCategory = typer.Option(..., "--category", "-c", help="Category of the transaction."),
    transaction_type: TransactionType = typer.Option(
        ..., "--type", "-t", help="Type of the transaction (income or expense)."
    ),
    description: str = typer.Option(..., "--desc", "-d", help="Description of the transaction."),
    date: Optional[datetime] = typer.Option(
        None, "--date", "-D", help="Date of the transaction (YYYY-MM-DD). Defaults to now."
    ),
):
    """
    Manually add a new transaction to the record.
    """
    transaction_date = date if date else datetime.utcnow()
    
    transaction = Transaction(
        amount=amount,
        category=category,
        transaction_type=transaction_type,
        description=description,
        date=transaction_date,
    )

    with get_session() as session: # Corrected call to get_session
        try:
            session.add(transaction)
            session.commit()
            session.refresh(transaction)
            print_success(f"Transaction added: {transaction}")
        except Exception as e:
            print_error(f"Failed to add transaction: {e}")

@app.command(name="log")
def log_transaction_ai(
    transaction_text: str = typer.Argument(..., help="Natural language description of the transaction."),
):
    """
    Log a transaction using AI to parse the natural language input.
    """
    parsed_data = ai_service.parse_transaction(transaction_text)

    if not parsed_data:
        print_error("AI failed to parse the transaction. Please try again or use 'add' command for manual entry.")
        return

    # Validate parsed data
    try:
        raw_amount = float(parsed_data.get("amount")) # AI might return float
        if raw_amount != int(raw_amount):
            print_info(f"Warning: AI parsed amount '{raw_amount}' has decimal places, but amounts are stored as integers. Truncating to {int(raw_amount)}.")
        amount = int(raw_amount)
        description = parsed_data.get("description")
        category_str = parsed_data.get("category")
        type_str = parsed_data.get("type")

        # Convert category and type strings to Enum members
        category = TransactionCategory(category_str)
        transaction_type = TransactionType(type_str)

    except (ValueError, TypeError) as e:
        print_error(f"AI returned invalid data types or enum values: {e}. Parsed data: {parsed_data}")
        return
    except KeyError as e:
        print_error(f"AI response missing expected key: {e}. Parsed data: {parsed_data}")
        return

    transaction = Transaction(
        amount=amount,
        category=category,
        transaction_type=transaction_type,
        description=description,
        date=datetime.utcnow(),
    )

    with get_session() as session: # Corrected call to get_session
        try:
            session.add(transaction)
            session.commit()
            session.refresh(transaction)
            print_success(f"Transaction logged by AI: {transaction}")
        except Exception as e:
            print_error(f"Failed to log transaction: {e}")

if __name__ == "__main__":
    app()
