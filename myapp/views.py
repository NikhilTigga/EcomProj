from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate ,login, logout
from django.contrib import messages

from .models import *

# Create your views here.

def index_view(request):

    if not request.user.is_authenticated:
       return redirect('Login_page')

    product = Products.objects.all()

    context = {
        'productdata': product,
    }

    return render(request, 'pages/index.html',context)





def about_view(request):
    return render(request,'pages/about.html')

def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.error(request, 'Please fill in all fields.')
            return redirect('Login_page')
        user = User.objects.filter(username = username).first()

        if user is not None and user.check_password(password):
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index_page')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('Login_page')

    return render(request,'pages/loginpage.html')

from django.contrib.auth.models import User 


def register_view(request):
    if request.method == 'POST':
        # Process the form data
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not user_name or not email or not password:
            messages.error(request, 'Please fill in all fields.')
            return redirect('Register_page')
       
        if User.objects.filter(username = email).exists():
            messages.error(request, 'Username already exists.')
            return redirect('Register_page')

        user_data = User.objects.create_user(username=email, first_name=user_name, email=email, password=password)

        user_data.save()
        messages.success(request, 'Registration successful. Please login.')
        return redirect('Login_page')

    return render(request,'pages/registerpage.html')


def Logout_view(request):
    print("Logout view called")
    logout(request)
    messages.success(request, 'You have been Logged out successfully.')
    return redirect('Login_page')


def forgot_password_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        if not username or not password or not confirm_password:
            messages.error(request, 'Please fill in all fields.')
            return redirect('forgot_password_page')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match !')
            return redirect('forgot_password_page')
        
        user_is = User.objects.filter(username=username).first()

        if user_is is not None:
            user_is.set_password(password)
            user_is.save()
            messages.success(request, 'Password reset successful. Please login with your new password.')
            return redirect('Login_page')


    return render(request, 'pages/forget_password.html')



def add_to_cart_view(request, product_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in ' \
        'to add items to the cart.')
        return redirect('Login_page')
    
    productis = Products.objects.filter(id=product_id).first()
    if productis is None:
        messages.error(request, 'Product not found.')
        return redirect('index_page')
    user_cart, created = UserCart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItems.objects.get_or_create(cart=user_cart, 
                                                         product=productis)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'Added {productis.name} to your cart.')
    return redirect('index_page')



def cart_count(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to view your cart.')
        return redirect('Login_page')

    user_cart, created = UserCart.objects.get_or_create(user=request.user)

    cart_count = user_cart.cart_items.count()

    print(f"Cart count for user {request.user.username}: {cart_count}")

    return JsonResponse({
        'status': True,
        'cart_count': cart_count})


def cart_item_page_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be Logged in !')
        return redirect('Login_page')

    user_cart, created = UserCart.objects.get_or_create(user=request.user)
    cart_items = user_cart.cart_items.all()

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'pages/cart_items_page.html', context)


def update_cart_item_quantity(request, item_id, action):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to update your cart.')
        return redirect('Login_page')

    cart_item = CartItems.objects.filter(id=item_id, cart__user=request.user).first()
    if cart_item is None:
        messages.error(request, 'Cart item not found.')
        return redirect('cart_item_page_view')
    
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart_item_page_view')
    elif action == 'decrease':
        cart_item.quantity -= 1
       

        if cart_item.quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
            return redirect('cart_item_page_view')
    cart_item.save()
    return redirect('cart_item_page_view')
    

    
    
    
    
    

    
    
    
    

    
