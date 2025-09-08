from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum


class BudgetPeriod(Enum):
    """Enumeration of supported budget periods."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class Budget:
    """
    Represents a budget for a specific category and period.
    
    Attributes:
        category (str): The category this budget applies to
        amount (float): The budget amount
        period (BudgetPeriod): The period for this budget
        created_date (str): When the budget was created
        budget_id (str): Unique identifier for the budget
        is_active (bool): Whether the budget is currently active
    """
    
    def __init__(self, category: str, amount: float, period: str = "monthly", 
                 budget_id: Optional[str] = None, is_active: bool = True):
        """
        Initialize a new Budget object.
        
        Args:
            category (str): The category this budget applies to
            amount (float): The budget amount (must be positive)
            period (str): The period for this budget (daily, weekly, monthly, yearly)
            budget_id (str, optional): Unique identifier. If not provided, will be generated.
            is_active (bool): Whether the budget is currently active
        
        Raises:
            ValueError: If amount is negative or zero, or if period is invalid
        """
        if amount <= 0:
            raise ValueError("Budget amount must be positive")
        
        try:
            self.period = BudgetPeriod(period.lower())
        except ValueError:
            raise ValueError(f"Invalid period '{period}'. Must be one of: {[p.value for p in BudgetPeriod]}")
        
        self.category = category.strip().lower()
        self.amount = float(amount)
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.budget_id = budget_id or self._generate_id()
        self.is_active = is_active
    
    def _generate_id(self) -> str:
        """Generate a unique ID for the budget."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"budget_{timestamp}_{hash(self.category) % 10000:04d}"
    
    def __str__(self) -> str:
        """String representation of the budget."""
        status = "Active" if self.is_active else "Inactive"
        return f"Budget: {self.category} | Amount: ₲{self.amount:,.2f} | Period: {self.period.value} | Status: {status}"
    
    def __repr__(self) -> str:
        """Detailed string representation of the budget."""
        return (f"Budget(category='{self.category}', amount={self.amount}, "
                f"period='{self.period.value}', id='{self.budget_id}', active={self.is_active})")
    
    def to_dict(self) -> dict:
        """Convert budget to dictionary for serialization."""
        return {
            'id': self.budget_id,
            'category': self.category,
            'amount': self.amount,
            'period': self.period.value,
            'created_date': self.created_date,
            'is_active': self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Budget':
        """Create a Budget object from a dictionary."""
        budget = cls(
            category=data['category'],
            amount=data['amount'],
            period=data['period'],
            budget_id=data.get('id'),
            is_active=data.get('is_active', True)
        )
        budget.created_date = data.get('created_date', budget.created_date)
        return budget
    
    def get_daily_amount(self) -> float:
        """Calculate the daily budget amount based on the period."""
        if self.period == BudgetPeriod.DAILY:
            return self.amount
        elif self.period == BudgetPeriod.WEEKLY:
            return self.amount / 7
        elif self.period == BudgetPeriod.MONTHLY:
            return self.amount / 30  # Approximate
        elif self.period == BudgetPeriod.YEARLY:
            return self.amount / 365  # Approximate
        else:
            return self.amount
    
    def get_remaining_days_in_period(self) -> int:
        """Calculate remaining days in the current period."""
        now = datetime.now()
        
        if self.period == BudgetPeriod.DAILY:
            return 1
        elif self.period == BudgetPeriod.WEEKLY:
            days_since_monday = now.weekday()
            return 7 - days_since_monday
        elif self.period == BudgetPeriod.MONTHLY:
            # Get last day of current month
            if now.month == 12:
                next_month = now.replace(year=now.year + 1, month=1, day=1)
            else:
                next_month = now.replace(month=now.month + 1, day=1)
            last_day = next_month - timedelta(days=1)
            return (last_day - now).days + 1
        elif self.period == BudgetPeriod.YEARLY:
            # Get last day of current year
            next_year = now.replace(year=now.year + 1, month=1, day=1)
            last_day = next_year - timedelta(days=1)
            return (last_day - now).days + 1
        else:
            return 1
    
    def calculate_remaining_budget(self, spent_amount: float) -> float:
        """Calculate remaining budget amount."""
        return max(0, self.amount - spent_amount)
    
    def calculate_usage_percentage(self, spent_amount: float) -> float:
        """Calculate what percentage of the budget has been used."""
        if self.amount == 0:
            return 0.0
        return min(100.0, (spent_amount / self.amount) * 100)
    
    def is_over_budget(self, spent_amount: float) -> bool:
        """Check if spending has exceeded the budget."""
        return spent_amount > self.amount
    
    def get_status_message(self, spent_amount: float) -> str:
        """Get a status message based on budget usage."""
        percentage = self.calculate_usage_percentage(spent_amount)
        remaining = self.calculate_remaining_budget(spent_amount)
        
        if percentage >= 100:
            return f"BUDGET EXCEEDED! Over by ₲{abs(remaining):,.2f} ⚠️"
        elif percentage >= 90:
            return f"Critical: {percentage:.1f}% used, ₲{remaining:,.2f} remaining ⚠️"
        elif percentage >= 80:
            return f"Warning: {percentage:.1f}% used, ₲{remaining:,.2f} remaining ⚠️"
        elif percentage >= 50:
            return f"Half used: {percentage:.1f}% used, ₲{remaining:,.2f} remaining ℹ️"
        else:
            return f"On track: {percentage:.1f}% used, ₲{remaining:,.2f} remaining ✅"
    
    def __eq__(self, other) -> bool:
        """Check if two budgets are equal based on their ID."""
        if not isinstance(other, Budget):
            return False
        return self.budget_id == other.budget_id
    
    def __hash__(self) -> int:
        """Hash the budget based on its ID."""
        return hash(self.budget_id)
