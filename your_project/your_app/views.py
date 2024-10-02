from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Product, Cart  # Ensure Cart is imported
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

ADMIN_USERNAMES = ['admin1', 'admin2']  # Add your admin usernames here


# Function to check if the user is an admin
def is_admin(user):
    return user.username in ADMIN_USERNAMES  # Add your admin usernames here


# Login view (redirect based on user type)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            if is_admin(user):  # Redirect admin users to the admin dashboard
                return redirect('admin_dashboard')
            else:
                return redirect('home')  # Redirect regular users to the main home page
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'login.html')


@login_required
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


@login_required
def scan_product_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        try:
            product = Product.objects.get(barcode=product_id)
            return JsonResponse({'success': True, 'message': 'Product found: ' + product.name})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found in database.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


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
    product = get_object_or_404(Product, id=product_id)
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
        return HttpResponse("Your cart is empty!")

    cart_items = CartItem.objects.filter(cart=cart)
    subtotal = sum(item.subtotal() for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'subtotal': subtotal})


@login_required
def scan_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(barcode=product_id)  # Assuming barcode is used
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                cart_item.quantity += 1
            cart_item.save()

            return JsonResponse({'success': True, 'message': 'Product added to cart.'})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found.'}, status=404)

    return render(request, 'scan.html')


def home_view(request):
    return render(request, 'home.html')


# Admin views
@login_required
def product_management(request):
    products = Product.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        # You may add fields like description, quantity etc. as needed
        product = Product.objects.create(name=name, price=price)
        messages.success(request, f'Product "{product.name}" added successfully!')
        return redirect('product_management')

    return render(request, 'admin/product_management.html', {'products': products})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def checkout_view(request):
    # Implement your checkout logic here
    # For example, you can render a checkout template or process payment
    return render(request, 'checkout.html')  # Replace with your actual checkout template


@login_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})

@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()  # Remove the item from the cart
        messages.success(request, 'Item removed from cart successfully!')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart.')

    return redirect('cart')  # Redirect to the cart page after removal


@login_required
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'admin/manage_products.html', {'products': products})


@login_required
def add_product_scan(request):
    if request.method == 'POST':
        # Handle the scanned barcode and add product logic here
        pass
    return render(request, 'admin/add_product_scan.html')


@login_required
def user_management(request):
    users = User.objects.all()
    return render(request, 'admin/user_management.html', {'users': users})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout


def admin_scan_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        try:
            # Redirect to product detail page after scan
            return redirect('admin_add_product', product_id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found.'}, status=404)

    return render(request, 'admin/admin_scan.html')


def add_product_view(request, barcode):
    barcode = barcode.strip()

    product = get_object_or_404(Product, barcode=barcode)

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        # Check if a product with the same barcode already exists
        product, created = Product.objects.get_or_create(
            barcode=barcode,
            defaults={
                'name': product_name,
                'description': description,
                'price': price,
                'quantity': quantity,
            }
        )

        if not created:
            product.name = product_name
            product.description = description
            product.price = price
            product.quantity = quantity
            product.save()

        messages.success(request, 'Product added/updated successfully!')
        return redirect('admin_scan')

    return render(request, 'admin/admin_add_product.html', {'barcode': barcode})
