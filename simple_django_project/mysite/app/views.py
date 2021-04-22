from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User,auth
from app.models import Pizza,Salad,Noodle

# Create your views here.
def home_page_view(request):
    pizza=Pizza.objects.all()
    salad=Salad.objects.all()
    noodle=Noodle.objects.all()

    return render(request,'app/index.html',{'pizza':pizza,'salad':salad,'noodle':noodle})

def register_view(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:

            if User.objects.filter(username=username).exists():
                messages.info(request,"username already taken")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email already taken")
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                return redirect("app:login")
        else:
            messages.info(request,"password not matching")
            return redirect("app:register")
        return redirect('/')
    else:
        return render(request, 'app/register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'you are logged in')
            return redirect("/")
        else:
            messages.warning(request, 'you are not authorized for it')
            return redirect("app:login")
    else:

        return render(request,'app/login.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

def show_detail(request,image_id):
    images = get_object_or_404(Pizza,pk=image_id)
    return render(request,"app/show.html",{"images": images})

def show_detail_salad(request,pk):
    images_1 = get_object_or_404(Salad,pk=pk)
    return render(request,"app/show_detail_salad.html",{"images_1": images_1})
