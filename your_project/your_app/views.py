from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import CartItem, Product

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('scan')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'login.html')

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please try again.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# def scan_view(request):
#     return render(request, 'scan.html')

# def cart_view(request):
#     if request.user.is_authenticated:
#         cart_items = CartItem.objects.filter(user=request.user)
#         return render(request, 'cart.html', {'cart_items': cart_items})
#     return redirect('login')

from django.shortcuts import render, redirect
from .models import Product, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.total_price() for item in cart_items)  # Calculate subtotal
    return render(request, 'cart.html', {'cart_items': cart_items, 'subtotal': subtotal})


def scan_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product
        )
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return JsonResponse({'success': True})
    return render(request, 'scan.html')

from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')