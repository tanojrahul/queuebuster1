from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('scan/', views.scan_view, name='scan'),
    path('cart/', views.cart_view, name='cart'),
    path('', views.home_view, name='home'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

]
