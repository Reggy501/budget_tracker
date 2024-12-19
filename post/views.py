from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum  # Import for calculating totals
from .forms import IncomeForm, ExpenseForm
from .models import Income, Expense
from django.utils import timezone

# Home page
def home(request):
    return render(request, 'home.html')

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Log the user in
            return redirect('dashboard')  # Redirect to the dashboard after login

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

# Signup view
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        password2 = request.POST.get('password2')

        if password == password2:
            if len(password) <= 5:
                messages.warning(request, 'Password must be at least 6 characters long.')
                return render(request, 'signup.html')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'signup.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return render(request, 'signup.html')

            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, "Account created successfully.")
            return redirect('login')  # Redirect to login after successful signup

        messages.error(request, "Passwords do not match.")
        return render(request, 'signup.html')

    return render(request, 'signup.html')

# Dashboard view
@login_required
def dashboard(request):
    # Fetch total income and expenses
    total_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses

    # Fetch income and expense records for the user
    income_records = Income.objects.filter(user=request.user).order_by('-date_added')
    expense_records = Expense.objects.filter(user=request.user).order_by('-date_added')

    return render(request, 'dashboard.html', {
        'user': request.user,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'income_records': income_records,
        'expense_records': expense_records,
    })
# Income view
@login_required
def income(request):
    # Fetch all income records for the user
    income_records = Income.objects.filter(user=request.user)

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Set the user to the logged-in user
            income.save()
            messages.success(request, 'New income added successfully.')
            return redirect('income')  # Redirect to the income page
    else:
        form = IncomeForm()

    return render(request, 'income.html', {'form': form, 'income_records': income_records})
@login_required
def expenses(request):
    # Retrieve the balance from the session
    balance = request.session.get('balance', 0)  # Default to 0 if not set

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)

            # Check the current balance
            user_income = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
            user_expenses = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
            current_balance = user_income - user_expenses

            if expense.amount > current_balance:
                messages.error(request, 'You have insufficient funds for this expense! Your balance is Tshs {:.2f}.'.format(current_balance))
                return redirect('expenses')

            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense recorded successfully.')
            return redirect('expenses')
    else:
        form = ExpenseForm()

    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    return render(request, 'expenses.html', {
        'form': form,
        'expenses': expenses,
        'balance': balance  # Pass the balance to the template
    })
def logout(request):
    auth_logout(request)  # Log the user out
    messages.success(request, 'Logged out successfully.')
    return redirect('home')  # Redirect to home after logout
