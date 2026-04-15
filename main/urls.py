from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('setup/', views.setup, name='setup'),
    path('dashboard/', views.dashboard, name='dashboard'),
]