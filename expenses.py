class Expenses:
    
    def __init__(expense, name, category, amount) -> None:
        expense.name = name
        expense.category = category
        expense.amount = amount

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, ${self.amount:.2f} >"