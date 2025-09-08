from classes import Expense, Budget
from classes.data_manager import DataManager
import os

def get_user_expense():
    """Get expense details from user input with improved validation."""
    expense_name = input("Enter expense name: ").strip()
    
    if not expense_name:
        print("Expense name cannot be empty.")
        return None
    
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount <= 0:
                print("Amount must be positive. Please enter a valid number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    print(f"You've entered: {expense_name}, and ₲{expense_amount:,.2f}")

    expense_categories = [
        "food", 
        "transport", 
        "housing", 
        "utilities", 
        "entertainment", 
        "other"
    ]
    
    while True:
        print("\nSelect a category:")
        for index, category_name in enumerate(expense_categories):
            print(f"{index + 1}. {category_name.title()}")

        value_range = f"1 - {len(expense_categories)}"
        try:
            selected_index = int(input(f"Enter a category number ({value_range}): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if 1 <= selected_index <= len(expense_categories):
            selected_category = expense_categories[selected_index - 1]
            try:
                new_expense = Expense(expense_name, selected_category, expense_amount)
                return new_expense
            except ValueError as e:
                print(f"Error creating expense: {e}")
                return None
        else:
            print("Invalid category number. Please try again.")

def save_expense_to_file(expense, data_manager):
    """Save expense using DataManager."""
    if data_manager.save_expense(expense):
        print("Expense saved successfully!")
    else:
        print("Failed to save expense.")

def display_current_expense(expense):
    """Display the current expense that was just added"""
    print("\n--- Current Expense ---")
    print(expense)

def display_all_expenses(data_manager):
    """Display all expenses using DataManager."""
    expenses = data_manager.load_expenses()
    
    if not expenses:
        print("No expenses found.")
        return
    
    print("\n--- All Expenses ---")
    for expense in expenses:
        print(f"ID: {expense.expense_id} | {expense}")
        print(f"  Created: {expense.created_date}")
        print()

def get_total_expenses(data_manager):
    """Calculate and display total amount spent using DataManager."""
    total = data_manager.get_total_spending()
    print(f"\n--- Total Expenses: ₲{total:,.2f} ---")
    return total

def set_budget(data_manager):
    """Allow user to set a budget for a specific category with improved validation."""
    expense_categories = [
        "food", "transport", "housing", "utilities", 
        "entertainment", "other"
    ]
    
    print("\n--- Set Budget ---")
    print("Select a category for your budget:")
    for index, category_name in enumerate(expense_categories):
        print(f"{index + 1}. {category_name.title()}")
    
    while True:
        try:
            selected_index = int(input(f"Enter category number (1-{len(expense_categories)}): "))
            if 1 <= selected_index <= len(expense_categories):
                selected_category = expense_categories[selected_index - 1]
                break
            else:
                print("Invalid category number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Select budget period
    periods = ["daily", "weekly", "monthly", "yearly"]
    print("\nSelect budget period:")
    for index, period in enumerate(periods):
        print(f"{index + 1}. {period.title()}")
    
    while True:
        try:
            period_index = int(input(f"Enter period number (1-{len(periods)}): "))
            if 1 <= period_index <= len(periods):
                selected_period = periods[period_index - 1]
                break
            else:
                print("Invalid period number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    while True:
        try:
            budget_amount = float(input(f"Enter budget amount for {selected_category} ({selected_period}): "))
            if budget_amount <= 0:
                print("Budget amount must be positive. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    try:
        budget = Budget(selected_category, budget_amount, selected_period)
        if data_manager.save_budget(budget):
            print(f"Budget set successfully: {budget}")
            return budget
        else:
            print("Failed to save budget.")
            return None
    except ValueError as e:
        print(f"Error creating budget: {e}")
        return None

def display_budgets(data_manager):
    """Display all budgets using DataManager."""
    budgets = data_manager.load_budgets()
    
    if not budgets:
        print("No budgets found.")
        return
    
    print("\n--- All Budgets ---")
    for budget in budgets:
        print(f"ID: {budget.budget_id} | {budget}")
        print(f"  Created: {budget.created_date}")
        print()

def get_category_spending(data_manager, category):
    """Calculate total spending for a specific category using DataManager."""
    return data_manager.get_total_spending(category)

def check_budget_status(data_manager):
    """Check spending against budgets and show status using DataManager."""
    budgets = data_manager.load_budgets()
    
    if not budgets:
        print("No budgets found. Please set a budget first.")
        return
    
    print("\n--- Budget Status ---")
    for budget in budgets:
        if not budget.is_active:
            continue
            
        spent = get_category_spending(data_manager, budget.category)
        status_message = budget.get_status_message(spent)
        
        print(f"\n{budget.category.upper()}:")
        print(f"  Budget: ₲{budget.amount:,.2f} ({budget.period.value})")
        print(f"  Spent: ₲{spent:,.2f}")
        print(f"  Remaining: ₲{budget.calculate_remaining_budget(spent):,.2f}")
        print(f"  Usage: {budget.calculate_usage_percentage(spent):.1f}%")
        print(f"  Status: {status_message}")
        
        # Show daily budget info if not daily period
        if budget.period.value != "daily":
            daily_amount = budget.get_daily_amount()
            remaining_days = budget.get_remaining_days_in_period()
            print(f"  Daily budget: ₲{daily_amount:,.2f}")
            print(f"  Days remaining: {remaining_days}")

def show_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("              EXPENSE TRACKER")
    print("="*50)
    print("1. Add new expense")
    print("2. View all expenses")
    print("3. View total expenses")
    print("4. Set budget")
    print("5. View budgets")
    print("6. Check budget status")
    print("7. Export to JSON")
    print("8. Exit")
    print("="*50)

def main():
    """Main function with improved structure and DataManager integration."""
    print("Welcome to Expense Tracker!")
    
    # Initialize data manager
    data_manager = DataManager()
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-8): ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        
        if choice == "1":
            expense = get_user_expense()
            if expense:
                display_current_expense(expense)
                save_expense_to_file(expense, data_manager)
            
        elif choice == "2":
            display_all_expenses(data_manager)
            
        elif choice == "3":
            get_total_expenses(data_manager)
            
        elif choice == "4":
            set_budget(data_manager)
            
        elif choice == "5":
            display_budgets(data_manager)
            
        elif choice == "6":
            check_budget_status(data_manager)
            
        elif choice == "7":
            # Export to JSON
            if data_manager.export_to_json():
                print("Data exported to JSON successfully!")
            else:
                print("Failed to export data to JSON.")
            
        elif choice == "8":
            print("Thank you for using Expense Tracker. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, or 8.")
        

        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            try:
                continue_choice = input("\nPress Enter to continue or 'q' to quit: ").strip().lower()
                if continue_choice == 'q':
                    print("Goodbye!")
                    break
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    main()