from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Category


# Create your views here.
def home_page_view(request):
    # products=None
    # categories=Category.objects.all()
    # categoryId=request.GET.get("category")
    # print(categoryId)
    # if categoryId:
    #    products=Product.objects.filter(category=categoryId)
    # else:
    # products=Product.objects.all()
    #
    # data={}
    # data['products']=products
    # data['categories']=categories
    return render(request, 'store/index.html')


def product_list(request, pk):
    products = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if pk:
        category = get_object_or_404(Category, pk=pk)
        products = Product.objects.filter(category=category)

    data = {}
    data['categories'] = categories
    data['products'] = products

    return render(request, 'store/index.html', data)


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
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                return redirect("store:login")
        else:
            messages.info(request, "password not matching")
            return redirect("store:register")
        return redirect('/store')
    else:
        return render(request, 'store/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in')
            return redirect("/store")
        else:
            messages.warning(request, 'you are not authorized for it')
            return redirect("store:login")
    else:

        return render(request, 'store/login.html')


def logout(request):
    auth.logout(request)
    return redirect("/store")


def show_detail(request, id):
    product = Product.objects.get(id=id)
    # product = get_object_or_404(Product,pk=id)
    return render(request, "store/show_detail.html", {"product": product})
