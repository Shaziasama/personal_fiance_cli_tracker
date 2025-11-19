# 🏗️ Project Blueprint: FinTrack Pro CLI
**A Professional, AI-Powered Personal Finance CLI Application**

## 1. Project Overview
FinTrack Pro is a terminal-based financial management system. It mimics the capabilities of a Fintech mobile app (budgeting, insights, categorization) but runs in a developer-friendly CLI environment. It leverages **Google Gemini** to parse natural language transaction logs and generate financial advice.

## 2. Tech Stack & Dependencies
* **Core:** Python 3.10+
* **CLI Framework:** `Typer` (for commands and argument parsing)
* **UI/UX:** `Rich` (for tables, panels, colors, and loading spinners)
* **Database:** `SQLModel` (SQLite) (for relational data storage)
* **AI Integration:** `google-generativeai` (Gemini API)
* **Data Analysis:** `Pandas` (for calculating insights and trends)
* **Visualization:** `Plotext` (for rendering charts in the terminal)

## 3. Project Directory Structure
The project must follow this modular architecture to ensure scalability. **Every directory must contain a `README.md` explaining its specific purpose.**

```text
finance-cli/
├── GEMINI.md                  # This Architecture Documentation
├── .env                       # Stores GEMINI_API_KEY and DB_URL
├── .gitignore                 # Ignores venv, .env, __pycache__
├── requirements.txt           # List of all python dependencies
├── main.py                    # The entry point (CLI runner)
│
├── app/                       # Main Application Source Code
│   ├── __init__.py
│   ├── README.md              # Documentation for the App module
│   │
│   ├── models/                # Database Schemas (SQLModel)
│   │   ├── __init__.py
│   │   ├── transaction.py     # Transaction Table definition
│   │   ├── budget.py          # Budget Table definition
│   │   └── README.md          # Docs for Data Models
│   │
│   ├── database/              # Database Connection & Sessions
│   │   ├── __init__.py
│   │   ├── engine.py          # SQLite setup & initialization
│   │   └── README.md          # Docs for DB operations
│   │
│   ├── commands/              # CLI Command Logic (Typer)
│   │   ├── __init__.py
│   │   ├── log.py             # 'add' and 'log' (AI) commands
│   │   ├── view.py            # 'dashboard' and 'list' commands
│   │   ├── budget.py          # Budget setting commands
│   │   └── README.md          # Docs for available commands
│   │
│   ├── services/              # Business Logic & External APIs
│   │   ├── __init__.py
│   │   ├── ai_service.py      # Google Gemini API Handler (NLP)
│   │   ├── analytics.py       # Pandas logic for calculations
│   │   └── README.md          # Docs for Logic Services
│   │
│   └── utils/                 # Helpers & UI Components
│       ├── __init__.py
│       ├── ui.py              # Shared Rich components (Tables, Headers)
│       ├── helpers.py         # Date formatting, Currency formatting
│       └── README.md          # Docs for utility functions
│
└── tests/                     # Unit Tests
    ├── __init__.py
    └── README.md              # Instructions on running tests
