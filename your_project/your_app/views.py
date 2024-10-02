from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import CartItem, Product, Cart  # Ensure Cart is imported
from django.contrib.auth.decorators import login_required


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


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # Create or update the cart item
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return HttpResponse("Your cart is empty!!")

    cart_items = CartItem.objects.filter(cart=cart)
    subtotal = sum(item.subtotal() for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'subtotal': subtotal})


@login_required
def scan_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return JsonResponse({'success': True})
    return render(request, 'scan.html')


def home_view(request):
    return render(request, 'home.html')

