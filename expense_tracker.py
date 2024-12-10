from expenses import Expenses
import os

def main():
    print("Runnning Expense Tracker!")
    expense_file_path = 'expenses.csv'
    budget_file_path = 'budget.txt'
    budget = 2000
    #Get user input for expense
    expense = get_user_expense()
    

    # Write user expense to a file
    save_expense_to_file(expense, expense_file_path)

    # Read and summarize file expenses
    summarize_expenses(expense_file_path, budget)

    #clear_expenses(expense_file_path)

def get_user_expense():
    print("Getting User Expense!")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = [
        "Food", "Transportation", "Utilities", "Health", "Shopping", "Fun"  
    ]

    while True: 
        print("Select a Category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}. {category_name}")
        
        value_range  = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category numnber {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expenses(name=expense_name, category=selected_category, amount = expense_amount)
            return new_expense
        else:
            print("Invalid category")

        break
def save_expense_to_file(expense, expense_file_path):
    print(f"Saving User Expense!: {expense}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name}, {expense.category}, {expense.amount}\n")

def summarize_expenses(expense_file_path, budget_file_path):
    # Attempt to read the budget from budget.txt
    try:
        with open(budget_file_path, 'r') as f:
            budget = float(f.read().strip())
    except FileNotFoundError:
        print("Budget file not found. Using default budget of 0.")
        budget = 0.0
    except ValueError:
        print("Invalid budget value. Using default budget of 0.")
        budget = 0.0
    
    expenses = []
    with open(expense_file_path, "r") as f:
        for line in f:
            name, category, amount = line.strip().split(",")
            expenses.append({'name': name, 'category': category, 'amount': float(amount)})
    
    # Calculate total spent
    total_spent = sum(expense['amount'] for expense in expenses)
    
    # Calculate remaining budget
    remaining_budget = budget - total_spent

    # Calculate amount spent by category
    amount_by_category = {}
    for expense in expenses:
        if expense['category'] in amount_by_category:
            amount_by_category[expense['category']] += expense['amount']
        else:
            amount_by_category[expense['category']] = expense['amount']
    
    # Return a summary including amount by category
    return {
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'amount_by_category': amount_by_category,
    }

def clear_expenses(expense_file_path):
    print(f"Clearing Expenses!:")
    # Open the file in write mode to clear its contents
    with open(expense_file_path, 'w') as file:
        print
        file.truncate()  # This is actually redundant when opening in 'w' mode, as it clears the file.

def save_budget(budget, budget_file_path):
    try:
        with open(budget_file_path, 'w') as f:
            f.write(str(budget))
        print("Budget saved successfully.")
    except Exception as e:
        print(f"Failed to save budget: {e}")


if __name__ == "__main__":
    main()