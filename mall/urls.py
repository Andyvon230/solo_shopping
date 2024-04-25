from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page with merchandise list
    path('login/', views.user_login, name='login'),  # Login page URL
    path('charts/', views.admin_charts, name='admin_charts'),  # Admin charts view
]
