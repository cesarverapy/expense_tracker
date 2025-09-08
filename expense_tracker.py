from expense import Expense
from budget import Budget
import csv
import os

def get_user_expense():
    expense_name = input("Enter expense name: ")
    
    while True:
        try:
            expense_amount = int(input("Enter expense amount: "))
            if expense_amount < 0:
                print("Amount cannot be negative. Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    print(f"you've entered: {expense_name}, and {expense_amount}")

    expense_category = [
        "food", 
        "transport", 
        "housing", 
        "utilities", 
        "entertainment", 
        "other"
    ]
    
    while True:
        print("select a category:")
        for index, category_name in enumerate(expense_category):
            print(f"{index + 1}, {category_name}")

        value_range = f"1 - {len(expense_category)}"
        try:
            selected_index = int(input(f"Enter a category number: {value_range}: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if 1 <= selected_index <= len(expense_category):
            selected_category = expense_category[selected_index - 1]
            new_expense = Expense(expense_name, selected_category, expense_amount)
            return new_expense
        else:
            print("Invalid category number. Please try again.")

def save_expense_to_file(expense):
    csv_file = "expenses.csv"
    try:
        file_exists = os.path.exists(csv_file)
        
        with open(csv_file, "a", newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Name", "Category", "Amount"])
            writer.writerow([expense.name, expense.category, expense.amount])
        print("Expense saved successfully!")
    except Exception as e:
        print(f"Error saving expense: {e}")

def display_current_expense(expense):
    """Display the current expense that was just added"""
    print("\n--- Current Expense ---")
    print(expense)

def display_all_expenses():
    """Display all expenses from the CSV file"""
    csv_file = "expenses.csv"
    try:
        if not os.path.exists(csv_file):
            print("No expenses found. File doesn't exist.")
            return
            
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            if len(rows) <= 1:
                print("No expenses found.")
                return
                
            print("\n--- All Expenses ---")
            for row in rows[1:]:
                if len(row) >= 3:
                    print(f"Expense: {row[0]} | Category: {row[1]} | Amount: ₲{int(row[2].strip()):,}")
    except Exception as e:
        print(f"Error reading expenses: {e}")

def get_total_expenses():
    """Calculate and display total amount spent"""
    csv_file = "expenses.csv"
    try:
        if not os.path.exists(csv_file):
            print("No expenses found.")
            return 0
            
        total = 0
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            for row in rows[1:]:
                if len(row) >= 3:
                    total += int(row[2].strip())
        
        print(f"\n--- Total Expenses: ₲{total:,} ---")
        return total
    except Exception as e:
        print(f"Error calculating total: {e}")
        return 0

def set_budget():
    """Allow user to set a budget for a specific category"""
    expense_category = [
        "food", "transport", "housing", "utilities", 
        "entertainment", "other"
    ]
    
    print("\n--- Set Budget ---")
    print("Select a category for your budget:")
    for index, category_name in enumerate(expense_category):
        print(f"{index + 1}, {category_name}")
    
    while True:
        try:
            selected_index = int(input(f"Enter category number (1-{len(expense_category)}): "))
            if 1 <= selected_index <= len(expense_category):
                selected_category = expense_category[selected_index - 1]
                break
            else:
                print("Invalid category number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    while True:
        try:
            budget_amount = int(input(f"Enter budget amount for {selected_category}: "))
            if budget_amount <= 0:
                print("Budget amount must be positive. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    budget = Budget(selected_category, budget_amount)
    save_budget_to_file(budget)
    print(f"Budget set successfully: {budget}")
    return budget

def save_budget_to_file(budget):
    """Save budget to CSV file"""
    budget_file = "budgets.csv"
    try:
        file_exists = os.path.exists(budget_file)
        
        with open(budget_file, "a", newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Category", "Amount", "Period", "Created_Date"])
            writer.writerow([budget.category, budget.amount, budget.period, budget.created_date])
        print("Budget saved successfully!")
    except Exception as e:
        print(f"Error saving budget: {e}")

def display_budgets():
    """Display all budgets"""
    budget_file = "budgets.csv"
    try:
        if not os.path.exists(budget_file):
            print("No budgets found. File doesn't exist.")
            return
            
        with open(budget_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            if len(rows) <= 1:
                print("No budgets found.")
                return
                
            print("\n--- All Budgets ---")
            for row in rows[1:]:
                if len(row) >= 4:
                    print(f"Category: {row[0]} | Amount: ₲{int(row[1].strip()):,} | Period: {row[2]} | Created: {row[3]}")
    except Exception as e:
        print(f"Error reading budgets: {e}")

def get_category_spending(category):
    """Calculate total spending for a specific category"""
    csv_file = "expenses.csv"
    total = 0
    try:
        if not os.path.exists(csv_file):
            return 0
            
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            for row in rows[1:]:
                if len(row) >= 3 and row[1].strip().lower() == category.lower():
                    total += int(row[2].strip())
        
        return total
    except Exception as e:
        print(f"Error calculating category spending: {e}")
        return 0

def check_budget_status():
    """Check spending against budgets and show status"""
    budget_file = "budgets.csv"
    try:
        if not os.path.exists(budget_file):
            print("No budgets found. Please set a budget first.")
            return
            
        with open(budget_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            if len(rows) <= 1:
                print("No budgets found.")
                return
                
            print("\n--- Budget Status ---")
            for row in rows[1:]:
                if len(row) >= 4:
                    category = row[0]
                    budget_amount = int(row[1].strip())
                    spent = get_category_spending(category)
                    remaining = budget_amount - spent
                    percentage = (spent / budget_amount) * 100 if budget_amount > 0 else 0
                    
                    print(f"\n{category.upper()}:")
                    print(f"  Budget: ₲{budget_amount:,}")
                    print(f"  Spent: ₲{spent:,}")
                    print(f"  Remaining: ₲{remaining:,}")
                    print(f"  Percentage used: {percentage:.1f}%")
                    
                    if percentage >= 100:
                        print("  BUDGET EXCEEDED! ⚠️")
                    elif percentage >= 80:
                        print("  Warning: 80% of budget used ⚠️")
                    elif percentage >= 50:
                        print("  Half of budget used ℹ️")
                    else:
                        print("  On track ✅")
                        
    except Exception as e:
        print(f"Error checking budget status: {e}")

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
    print("7. Exit")
    print("="*50)

def main():
    print("Welcome to Expense Tracker!")
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-7): ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        
        if choice == "1":
            expense = get_user_expense()
            display_current_expense(expense)
            save_expense_to_file(expense)
            
        elif choice == "2":
            display_all_expenses()
            
        elif choice == "3":
            get_total_expenses()
            
        elif choice == "4":
            set_budget()
            
        elif choice == "5":
            display_budgets()
            
        elif choice == "6":
            check_budget_status()
            
        elif choice == "7":
            print("Thank you for using Expense Tracker. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or 7.")
        

        if choice in ["1", "2", "3", "4", "5", "6"]:
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