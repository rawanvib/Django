from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from myapp.models import User, Banner

# Create your views here.
def home(request):
    banner=Banner.objects.all()
    return render(request, 'website/home.html',{'banners':banner})

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # username = request.POST.get('username_register')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            # if User.objects.filter(username=username).exists():
            #     messages.info(request, "username already taken")
            if User.objects.filter(email=email).exists():
                messages.info(request, "email already taken")
            else:
                user=User.objects.create_user(password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                login(request,user)
                messages.success(request, "You are successfully registered")
                return redirect("website:home")
        else:
            messages.info(request, "password not matching")
            return redirect("website:register_view")
        return redirect("website:home")
    else:
        return render(request, 'website/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email_login')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'you are logged in')
            return redirect('website:home')
        else:
            messages.warning(request, 'email or password is incorrect.')
            return redirect('website:login_view')
    else:
        return render(request, 'website/login.html')

def logout_view(request):
   logout(request)
   return redirect('website:home')


