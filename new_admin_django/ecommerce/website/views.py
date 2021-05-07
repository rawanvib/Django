from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User, Group, AnonymousUser
# from django.contrib.auth import get_user_model

from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.core.paginator import Paginator

from django.contrib import messages

from myapp.models import User, Banner, Categories, Product, ProductImage, UserWishlist

from myapp.forms import RegisterForm


# Create your views here.
def home(request):
    banner = Banner.objects.filter(status='Active')
    categories = Categories.objects.filter(status=True)
    products=Product.objects.filter(status=True)
    product_images=ProductImage.objects.filter(product__is_featured__icontains=True)
    #product_images=ProductImage.product.all()
    #Product.objects.filter(attribute_values__value_option_id=2).filter(attribute_values__value_option_id=6)


    paginator=Paginator(products,6)
    products=paginator.page(1)

    return render(request, 'website/home.html', {'banners': banner,
                                                 'categories': categories,
                                                 'products':products,
                                                 'product_images':product_images})


# def register_view(request):
#     if request.method == 'POST':
    #     first_name = request.POST.get('first_name')
    #     last_name = request.POST.get('last_name')
    #     # username = request.POST.get('username_register')
    #     email = request.POST.get('email')
    #     password1 = request.POST.get('password1')
    #     password2 = request.POST.get('password2')
    #
    #     if password1 == password2:
    #         # if User.objects.filter(username=username).exists():
    #         #     messages.info(request, "username already taken")
    #         if User.objects.filter(email=email).exists():
    #             messages.info(request, "email already taken")
    #         else:
    #             user = User.objects.create_user(password=password1, email=email, first_name=first_name,
    #                                             last_name=last_name)
    #             user.save()
    #             login(request, user)
    #             messages.success(request, "You are successfully registered")
    #             return redirect("website:home")
    #     else:
    #         messages.info(request, "password not matching")
    #         return redirect("website:register_view")
    #     return redirect("website:home")
    # else:
    #     return render(request, 'website/register.html')

def register_view(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password1']
            form = form.save()
            # default_group = Group.objects.get(name='customer')
            # form.groups.add(default_group)
            form.save()
            messages.success(request, 'Registered was successfully created!')
            return redirect('website:login_view')
    else:
        form = RegisterForm()
    return render(request,'website/login.html',{'form':form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email_login')
        password = request.POST.get('password')
        # no need
        valuenext = request.POST.get('next')

        user = authenticate(request,email=email, password=password)
        if user is not None and valuenext == '':
            login(request, user)
            messages.success(request, 'you are logged in')
            return redirect('website:home')
        elif user is not None and valuenext != '':
            login(request, user)
            return redirect(valuenext)
        else:
            messages.warning(request, 'email or password is incorrect.')
            return redirect('website:login_view')
    else:
        return render(request, 'website/login.html')

@login_required(login_url='website:login_view')
def logout_view(request):
    logout(request)
    return redirect('website:home')

def category_item(request,id):
    categories=Categories.objects.all()
    products=Product.objects.filter(product__product_categories__id=id).order_by('-created_date')
    product_images=ProductImage.objects.filter(product__product_categories__id=id).order_by('-created_date')
    paginator = Paginator(products, 4)
    products = paginator.page(1)

    id = id
    return render(request, 'website/category_item.html',
                  {'products': products, 'categories': categories, 'id': id, 'product_images': product_images})

def ProductDetail(request, id):
    product = Product.objects.get(id=id)
    categories = Categories.objects.all()
    product_images = ProductImage.objects.filter(product=product)
    # for product_image in product_images:
    # print(product_images.image_name)

    return render(request, 'website/product_detail.html',
                  {'product_images': product_images, 'product': product, 'categories': categories})

@login_required(login_url='website:login_view')
def add_to_wishlist(request,id):

   product = get_object_or_404(Product,id=id)

   wished_item = UserWishlist.objects.get_or_create(product=product,user=request.user)

   messages.info(request,'The item was added to your wishlist')
   return redirect('website:home')