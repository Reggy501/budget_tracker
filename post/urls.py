from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('logout',views.logout,name="logout"),
    path('income/',views.income,name="income"),
    path('expenses/',views.expenses,name="expenses")


    
    ]
    