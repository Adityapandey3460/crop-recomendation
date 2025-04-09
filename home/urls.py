from django.urls import path
from . import views  # Make sure this imports your views correctly

urlpatterns = [
    path("", views.index, name="index"),  # Homepage
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]