from django.shortcuts import redirect, render
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def policy(request):
    return render(request, 'policy.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully.")

        login(request, user)
        return redirect('home')
    else:
        return render(request, 'register.html', {})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, category_name):
    try:
        category = Category.objects.get(slug=category_name)
        products = Product.objects.filter(category=category)
    except Category.DoesNotExist:
        return redirect('home')

    return render(request, 'category.html', {'products': products, 'category_name': category.name})

def category_summary(request):
    return render(request, 'category_summary.html', {})

def update_user(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to update your profile.")
            return redirect('login')

        user = request.user
        new_username = request.POST.get('username', '')
        new_email = request.POST.get('email', '')
        new_first_name = request.POST.get('first_name', '')
        new_last_name = request.POST.get('last_name', '')
        new_password = request.POST.get('password', '')
        confirm_password = request.POST.get('password_confirm', '')

        if new_password and new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('update_user')

        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, "Username already exists.")
                return redirect('update_user')
            user.username = new_username

        if new_email:
            user.email = new_email

        user.first_name = new_first_name
        user.last_name = new_last_name

        if new_password:
            user.set_password(new_password)

        user.save()
        messages.success(request, "Profile updated successfully.")

        # Re-authenticate the user if password was changed
        if new_password:
            login(request, user)

        return redirect('home')
    else:
        return render(request, 'update_user.html', {})

def index(request):
    return render(request, 'index.html', {})
