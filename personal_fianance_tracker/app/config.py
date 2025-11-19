import os
import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # allow static type checkers / IDEs to recognize load_dotenv even if package isn't installed
    from dotenv import load_dotenv  # type: ignore

try:
    _dotenv = importlib.import_module("dotenv")
    load_dotenv = getattr(_dotenv, "load_dotenv")
except Exception:
    # python-dotenv not available (e.g., in editor environment); provide a no-op fallback
    def load_dotenv(*args, **kwargs):
        return False

# Load environment variables from .env file
load_dotenv()

class AppConfig:
    """
    Application configuration for FinTrack Pro.
    Loads sensitive information like API keys and database URLs from environment variables.
    """
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyCOEQWYYaxIYOe1VQKBwB9BHjKUSAKzJ_c")
    DATABASE_URL: str = os.getenv("DB_URL", "sqlite:///./data/fintrack.db") # Default SQLite path

    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not found in environment variables. AI features may not work.")
    if not DATABASE_URL:
        print("Warning: DB_URL not found in environment variables. Using default SQLite path.")

