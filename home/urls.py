from django.urls import path
from . import views  # Import the views module

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup,name="signup"),
    path("login", views.login,name="login"),
  
]