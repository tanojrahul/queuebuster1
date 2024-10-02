from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
# from your_app import views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('scan/', views.scan_view, name='scan'),  # Make sure this matches
    path('cart/', views.cart_view, name='cart'),  # View the cart
    path('', views.home_view, name='home'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('admin/', admin.site.urls),  # Default Django admin
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin1/manage_users/', views.manage_users, name='manage_users'),
    path('admin1/scan/', views.admin_scan_view, name='admin_scan'),
    path('admin1/manage_products/', views.manage_products, name='manage_products'),
    path('admin1/add_product_scan/', views.add_product_scan, name='add_product_scan'),
    path('logout/', views.logout_view, name='logout'),
    path('admin1/add-product/<str:barcode>/', views.add_product_view, name='add_product'),

]
