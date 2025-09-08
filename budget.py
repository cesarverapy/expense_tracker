from datetime import datetime

class Budget:
    def __init__(self, category, amount, period="monthly"):
        self.category = category
        self.amount = amount
        self.period = period
        self.created_date = datetime.now().strftime("%Y-%m-%d")
    
    def __str__(self):
        return f"Budget: {self.category} | Amount: ₲{self.amount:,} | Period: {self.period}"
