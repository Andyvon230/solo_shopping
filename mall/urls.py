from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page with merchandise list
    path('login/', views.user_login, name='login'),  # Login page URL
    path('logout/', views.user_logout, name='logout'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.confirm_checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin_charts/', views.admin_charts, name='admin_charts'),
]
