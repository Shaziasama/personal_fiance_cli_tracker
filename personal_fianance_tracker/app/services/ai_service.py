# app/services/ai_service.py
import json
import google.generativeai as genai
from typing import Dict, Any

from app.config import AppConfig
from app.utils.ui import print_error, print_info

class AIService:
    """
    Service for interacting with the Google Gemini AI for natural language processing tasks.
    """
    def __init__(self):
        try:
            genai.configure(api_key=AppConfig.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print_error(f"Failed to configure Google Gemini AI: {e}")
            self.model = None

    def parse_transaction(self, text: str) -> Dict[str, Any] | None:
        """
        Parses a natural language transaction string and returns a structured JSON object.

        Args:
            text (str): The natural language string describing a transaction.

        Returns:
            Dict[str, Any] | None: A dictionary containing 'amount', 'category', 'type', and 'description'
                                 if parsing is successful, otherwise None.
        """
        if not self.model:
            print_error("AI Service is not configured. Please set GEMINI_API_KEY in your .env file.")
            return None

        prompt = f"""
        Analyze the following transaction description and extract the 'amount', 'category', 'type' (Income/Expense), and 'description'.
        The 'amount' should be a floating-point number.
        The 'category' should be one of: Food, Transport, Utilities, Rent, Salary, Entertainment, Shopping, Healthcare, Education, Savings, Investment, Other.
        The 'type' should be either 'Income' or 'Expense'.
        The 'description' should be a concise summary of the transaction.
        If any information is missing or unclear, use "Other" for category, and infer type if possible.
        Always respond with a JSON object.
        
        Example 1: "Bought groceries for $50 at Walmart"
        Expected JSON: {{"amount": 50.0, "category": "Food", "type": "Expense", "description": "Groceries at Walmart"}}
        
        Example 2: "Received salary of 2500"
        Expected JSON: {{"amount": 2500.0, "category": "Salary", "type": "Income", "description": "Received salary"}}
        
        Example 3: "Paid electricity bill $75"
        Expected JSON: {{"amount": 75.0, "category": "Utilities", "type": "Expense", "description": "Electricity bill"}}

        Transaction: "{text}"
        JSON:
        """
        
        try:
            print_info("Sending request to AI service to parse transaction...")
            response = self.model.generate_content(prompt)
            
            # Extract only the text content from the parts
            # Assuming the model returns a single part with text content.
            # You might need more robust parsing depending on actual model output.
            json_str = response.text.strip()
            
            # Attempt to parse the JSON string
            parsed_data = json.loads(json_str)
            
            # Basic validation for the expected keys
            required_keys = ["amount", "category", "type", "description"]
            if all(key in parsed_data for key in required_keys):
                return parsed_data
            else:
                print_error(f"AI response missing required keys: {json_str}")
                return None

        except json.JSONDecodeError as e:
            print_error(f"Failed to parse AI response as JSON: {e}\nResponse: {response.text}")
            return None
        except Exception as e:
            print_error(f"An error occurred while interacting with the AI service: {e}")
            return None
