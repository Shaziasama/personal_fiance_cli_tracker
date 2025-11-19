# App Module Documentation

This directory contains the main application source code for FinTrack Pro. It is structured into several sub-modules, each with a specific responsibility:

- `models/`: Defines the database schemas using SQLModel.
- `database/`: Handles database connection and session management.
- `commands/`: Contains the business logic for CLI commands using Typer.
- `services/`: Implements core business logic and external API integrations (e.g., Google Gemini).
- `utils/`: Provides helper functions and UI components.

Each sub-directory has its own `README.md` for more detailed documentation.