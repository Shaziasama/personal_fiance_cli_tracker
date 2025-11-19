# Business Logic & External APIs

This directory houses the core business logic and integrations with external services for FinTrack Pro.

- `ai_service.py`: Responsible for handling interactions with the Google Gemini API for natural language processing, such as parsing transaction descriptions or generating financial advice.
- `analytics.py`: Contains `Pandas`-based logic for performing data analysis, calculating insights, and identifying trends from financial data.

These services abstract away complex operations, providing clean interfaces for other parts of the application.