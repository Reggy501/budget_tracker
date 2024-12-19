from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incomes")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_period = models.CharField(
        max_length=10,
        choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly')],
        default='Monthly'  # Default to 'Monthly' if no selection is made
    )
    description = models.TextField(blank=True,null=True) 
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.time_period} Income: {self.amount}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount}"
