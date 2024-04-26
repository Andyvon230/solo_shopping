from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page with merchandise list
    path('login/', views.user_login, name='login'),  # Login page URL
    path('logout/', views.user_logout, name='logout'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.confirm_checkout, name='success'),
]
