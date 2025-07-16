# cotisations/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    path('', views.dashboard, name='dashboard'),
    path('dashboard/participant/', views.dashboard_participant, name='dashboard_participant'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
]