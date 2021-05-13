from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Cuisine, Category
from .documents import CuisineDocument
from django.contrib.auth.decorators import login_required

# Create your views here.
def home_page_view(request):

    categories=Category.objects.all()
    products = None
    category_id=request.GET.get('category')

    if category_id:
        products=Cuisine.get_all_Cuisines_by_category_id(category_id)
    else:
        products=Cuisine.get_all_Cuisines()

    data={}
    data['products']=products
    data['categories']=categories
    return render(request, 'store/index.html',data)

def search_dish(request):
    if request.method == 'POST':
        search=request.POST.get('searched')
        #products=Cuisine.objects.filter(name__icontains = search)
        # using elastic search

        if search:
            products= CuisineDocument.search().query('match',title=search)


        return render(request, 'store/search.html', {'search' : search, 'products':products})
    else:
        return render(request, 'store/search.html', {})



def register_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:

            if User.objects.filter(username=username).exists():
                messages.info(request, "username already taken")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email already taken")
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                return redirect("store:login")
        else:
            messages.info(request,"password not matching")
            return redirect("store:register")
        return redirect("/store")
    else:
        return render(request, 'store/register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request, 'you are logged in')
            return redirect("/store")
        else:
            messages.warning(request, 'you are not authorized for it')
            return redirect("store:login")
    else:

        return render(request,'store/login.html')

def logout(request):
    auth.logout(request)
    return redirect("/store")


def show_detail(request,id):
    product=Cuisine.objects.get(id=id)
    #product = get_object_or_404(Product,pk=id)
    return render(request, "store/show_detail.html", {"product": product})
