import csv
import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from .expense import Expense
from .budget import Budget


class DataManager:
    """
    Handles all data persistence operations for expenses and budgets.
    Supports both CSV and JSON formats.
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the DataManager.
        
        Args:
            data_dir (str): Directory to store data files
        """
        self.data_dir = data_dir
        self.expenses_file = os.path.join(data_dir, "expenses.csv")
        self.budgets_file = os.path.join(data_dir, "budgets.csv")
        self.expenses_json = os.path.join(data_dir, "expenses.json")
        self.budgets_json = os.path.join(data_dir, "budgets.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
    
    def save_expense(self, expense: Expense) -> bool:
        """
        Save an expense to CSV file.
        
        Args:
            expense (Expense): The expense to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            file_exists = os.path.exists(self.expenses_file)
            
            with open(self.expenses_file, "a", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["ID", "Name", "Category", "Amount", "Created_Date"])
                writer.writerow([
                    expense.expense_id,
                    expense.name,
                    expense.category,
                    expense.amount,
                    expense.created_date
                ])
            return True
        except Exception as e:
            print(f"Error saving expense: {e}")
            return False
    
    def load_expenses(self) -> List[Expense]:
        """
        Load all expenses from CSV file.
        
        Returns:
            List[Expense]: List of all expenses
        """
        expenses = []
        try:
            if not os.path.exists(self.expenses_file):
                return expenses
                
            with open(self.expenses_file, "r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        expense = Expense(
                            name=row['Name'],
                            category=row['Category'],
                            amount=float(row['Amount']),
                            expense_id=row.get('ID')
                        )
                        expense.created_date = row.get('Created_Date', expense.created_date)
                        expenses.append(expense)
                    except (ValueError, KeyError) as e:
                        print(f"Error parsing expense row: {e}")
                        continue
        except Exception as e:
            print(f"Error loading expenses: {e}")
        
        return expenses
    
    def save_budget(self, budget: Budget) -> bool:
        """
        Save a budget to CSV file.
        
        Args:
            budget (Budget): The budget to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            file_exists = os.path.exists(self.budgets_file)
            
            with open(self.budgets_file, "a", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["ID", "Category", "Amount", "Period", "Created_Date", "Is_Active"])
                writer.writerow([
                    budget.budget_id,
                    budget.category,
                    budget.amount,
                    budget.period.value,
                    budget.created_date,
                    budget.is_active
                ])
            return True
        except Exception as e:
            print(f"Error saving budget: {e}")
            return False
    
    def load_budgets(self) -> List[Budget]:
        """
        Load all budgets from CSV file.
        
        Returns:
            List[Budget]: List of all budgets
        """
        budgets = []
        try:
            if not os.path.exists(self.budgets_file):
                return budgets
                
            with open(self.budgets_file, "r", encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        budget = Budget(
                            category=row['Category'],
                            amount=float(row['Amount']),
                            period=row['Period'],
                            budget_id=row.get('ID'),
                            is_active=row.get('Is_Active', 'True').lower() == 'true'
                        )
                        budget.created_date = row.get('Created_Date', budget.created_date)
                        budgets.append(budget)
                    except (ValueError, KeyError) as e:
                        print(f"Error parsing budget row: {e}")
                        continue
        except Exception as e:
            print(f"Error loading budgets: {e}")
        
        return budgets
    
    def get_expenses_by_category(self, category: str) -> List[Expense]:
        """
        Get all expenses for a specific category.
        
        Args:
            category (str): The category to filter by
            
        Returns:
            List[Expense]: List of expenses in the category
        """
        all_expenses = self.load_expenses()
        return [exp for exp in all_expenses if exp.category.lower() == category.lower()]
    
    def get_total_spending(self, category: Optional[str] = None) -> float:
        """
        Calculate total spending, optionally filtered by category.
        
        Args:
            category (str, optional): Category to filter by
            
        Returns:
            float: Total spending amount
        """
        if category:
            expenses = self.get_expenses_by_category(category)
        else:
            expenses = self.load_expenses()
        
        return sum(exp.amount for exp in expenses)
    
    def get_budget_by_category(self, category: str) -> Optional[Budget]:
        """
        Get the active budget for a specific category.
        
        Args:
            category (str): The category to get budget for
            
        Returns:
            Budget or None: The budget if found, None otherwise
        """
        budgets = self.load_budgets()
        for budget in budgets:
            if budget.category.lower() == category.lower() and budget.is_active:
                return budget
        return None
    
    def export_to_json(self) -> bool:
        """
        Export all data to JSON files.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Export expenses
            expenses = self.load_expenses()
            expenses_data = [exp.to_dict() for exp in expenses]
            with open(self.expenses_json, 'w', encoding='utf-8') as f:
                json.dump(expenses_data, f, indent=2, ensure_ascii=False)
            
            # Export budgets
            budgets = self.load_budgets()
            budgets_data = [budget.to_dict() for budget in budgets]
            with open(self.budgets_json, 'w', encoding='utf-8') as f:
                json.dump(budgets_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    def import_from_json(self) -> bool:
        """
        Import data from JSON files.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Import expenses
            if os.path.exists(self.expenses_json):
                with open(self.expenses_json, 'r', encoding='utf-8') as f:
                    expenses_data = json.load(f)
                for exp_data in expenses_data:
                    expense = Expense.from_dict(exp_data)
                    self.save_expense(expense)
            
            # Import budgets
            if os.path.exists(self.budgets_json):
                with open(self.budgets_json, 'r', encoding='utf-8') as f:
                    budgets_data = json.load(f)
                for budget_data in budgets_data:
                    budget = Budget.from_dict(budget_data)
                    self.save_budget(budget)
            
            return True
        except Exception as e:
            print(f"Error importing from JSON: {e}")
            return False
    
    def clear_all_data(self) -> bool:
        """
        Clear all data files.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            files_to_clear = [self.expenses_file, self.budgets_file, self.expenses_json, self.budgets_json]
            for file_path in files_to_clear:
                if os.path.exists(file_path):
                    os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False
