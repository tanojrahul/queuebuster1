from django.urls import path
from . import views
from django.contrib import admin
from .views import remove_from_cart  # Import the view
from .views import checkout_view  # Import the view


urlpatterns = [
    path('login/', views.login_view, name='login'),  # User login
    path('register/', views.register_view, name='register'),  # User registration
    path('scan/', views.scan_view, name='scan'),  # Scan products
    path('cart/', views.cart_view, name='cart'),  # View the cart
    path('', views.home_view, name='home'),  # Home page
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add product to cart
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('admin1/manage_users/', views.manage_users, name='manage_users'),  # Manage users
    path('admin1/scan/', views.admin_scan_view, name='admin_scan'),  # Admin scan
    path('admin1/manage_products/', views.manage_products, name='manage_products'),  # Manage products
    path('admin1/add_product_scan/', views.add_product_scan, name='add_product_scan'),  # Add product by scan
    path('logout/', views.logout_view, name='logout'),  # Logout user
    path('admin1/add-product/<str:barcode>/', views.add_product_view, name='add_product'),  # Add product with barcode
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout_view, name='checkout'),

]

