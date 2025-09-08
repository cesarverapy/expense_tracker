from datetime import datetime
from typing import Optional


class Expense:
    """
    Represents an expense with name, category, amount, and timestamp.
    
    Attributes:
        name (str): The name/description of the expense
        category (str): The category of the expense
        amount (float): The amount of the expense
        created_date (str): The date when the expense was created
        expense_id (str): Unique identifier for the expense
    """
    
    def __init__(self, name: str, category: str, amount: float, expense_id: Optional[str] = None):
        """
        Initialize a new Expense object.
        
        Args:
            name (str): The name/description of the expense
            category (str): The category of the expense
            amount (float): The amount of the expense (must be positive)
            expense_id (str, optional): Unique identifier. If not provided, will be generated.
        
        Raises:
            ValueError: If amount is negative or zero
        """
        if amount <= 0:
            raise ValueError("Expense amount must be positive")
        
        self.name = name.strip()
        self.category = category.strip().lower()
        self.amount = float(amount)
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.expense_id = expense_id or self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate a unique ID for the expense."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"exp_{timestamp}_{hash(self.name) % 10000:04d}"
    
    def __str__(self) -> str:
        """String representation of the expense."""
        return f"Expense: {self.name} | Category: {self.category} | Amount: ₲{self.amount:,.2f}"
    
    def __repr__(self) -> str:
        """Detailed string representation of the expense."""
        return (f"Expense(name='{self.name}', category='{self.category}', "
                f"amount={self.amount}, id='{self.expense_id}')")
    
    def to_dict(self) -> dict:
        """Convert expense to dictionary for serialization."""
        return {
            'id': self.expense_id,
            'name': self.name,
            'category': self.category,
            'amount': self.amount,
            'created_date': self.created_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Expense':
        """Create an Expense object from a dictionary."""
        expense = cls(
            name=data['name'],
            category=data['category'],
            amount=data['amount'],
            expense_id=data.get('id')
        )
        expense.created_date = data.get('created_date', expense.created_date)
        return expense
    
    def __eq__(self, other) -> bool:
        """Check if two expenses are equal based on their ID."""
        if not isinstance(other, Expense):
            return False
        return self.expense_id == other.expense_id
    
    def __hash__(self) -> int:
        """Hash the expense based on its ID."""
        return hash(self.expense_id)
