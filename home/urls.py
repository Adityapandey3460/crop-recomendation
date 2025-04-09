from django.urls import path
from . import views  # Make sure this imports your views correctly

urlpatterns = [
    path("", views.index, name="index"),  # Homepage
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recommend/', views.recommend_view, name='recommend'),
    # 
    # path('', views.base, name='base'),  # Base template or another page
]