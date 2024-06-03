from flask import Flask, render_template, request, redirect, url_for, flash
from expense_tracker import get_user_expense, save_expense_to_file, summarize_expenses, clear_expenses, save_budget
from expenses import Expenses

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        expense_name = request.form.get('expenseName')
        category = request.form.get('category')
        amount = request.form.get('amount')

        if not all([expense_name, category, amount]):
            flash('All fields are required.', 'error')  # 'error' is an optional category
        else:
            try:
                amount_float = float(amount)
                expense = Expenses(expense_name, category, amount_float)
                save_expense_to_file(expense, 'expenses.csv')
                flash('Expense added successfully!', 'success')  # 'success' is an optional category
                return redirect(url_for('home'))
            except ValueError:
                flash('Invalid amount. Please enter a valid number.', 'error')
    return render_template('index.html')

@app.route('/clear-expenses', methods=['POST'])
def clear_expenses_route():
    # Assuming Expenses.clear_expenses is a static method that accepts a file path
    clear_expenses('expenses.csv')  # Use the absolute path to your CSV file
    flash('All expenses have been cleared.', 'success')  # Optional: Provide user feedback
    return redirect(url_for('home'))

@app.route('/set-budget', methods=['POST'])
def set_budget_route():
    budget = request.form.get('budget')
    if budget:
        save_budget(budget, 'budget.txt')
        flash('Budget saved successfully.', 'success')
    else:
        flash('Please enter a valid budget.', 'error')
    return redirect(url_for('home'))

@app.route('/')
def home():
    # Example file paths - adjust as necessary
    expense_file_path = 'expenses.csv'
    budget_file_path = 'budget.txt'
    
    # Ensure you have a valid budget value or set a default
    try:
        with open(budget_file_path, 'r') as f:
            budget = (f.read().strip())
    except Exception:
        budget = 0.0  # Default budget if file is missing or invalid
    
    summary = summarize_expenses(expense_file_path, budget)
    
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)