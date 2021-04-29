from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from django.db import IntegrityError, transaction
from django.contrib.auth.models import Group

# forms
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .forms import UserForm, OldPassForm,UserUpdateForm,CategoryForm

from .models import Categories


from django.forms import inlineformset_factory

from .decorators import unauthenticated_user, allowed_users
from .models import User

# Create your views here.
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def index(request):
    return render(request, 'myapp/starter.html')


# @unauthenticated_user
def login(request):
    if request.method == 'POST':

        username=request.POST.get('username')
        password = request.POST.get('password')
        valuenext = request.POST.get('next')

        user = authenticate(request, username=username, password=password)

        groups = request.user.groups.values_list('name',flat = True)

        if user is not None and valuenext == '':

            if 'admin' in groups or user.is_superuser:
                auth_login(request, user)
                messages.success(request, 'you are logged in')
                return redirect('myapp:index')
            else:

                messages.warning(request, 'you are not authorized for it')
        elif user is not None and valuenext != '':

            if 'admin' in groups or user.is_superuser:
                auth_login(request, user)
                return redirect(valuenext)
            else:
                messages.warning(request, 'you are not authorized for it')
        else:
            messages.info(request, 'please enter right credentials')

    return render(request, 'myapp/login.html')


def logoutUser(request):
   logout(request)
   return redirect('myapp:login')

# ----------------------------------------- users -------------------------------------------------
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def UserList(request):
    users = User.objects.all()
    return render(request, 'myapp/user_list.html', {'users': users})


@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def UserChange(request):
    instance = request.user
    if request.method == 'POST':
        form = ChangeDetailForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
    else:
        form = ChangeDetailForm(instance=instance)
    return render(request, 'myapp/change_detail.html', {'form': form})


@login_required(login_url='myapp:login')
def UserChangePsw(request,id):
    instance=get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = OldPassForm(request.POST, instance=instance)
        if form.is_valid():
            # instance = form.save(commit=False)
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password == confirm_password:
                user = request.user
                print(user.password)
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()    # add data to database
                    messages.success(request, 'password change succesfully')
                    return redirect('myapp:UserUpdate')
                else:
                    messages.warning(request, 'your current password  password is not matched ')
            else:
                messages.error(request, 'new password and current password is not matched ')

    form = OldPassForm()

    return render(request, 'myapp/user_psd_change.html', {'form': form})


@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def UserAdd(request):
    if request.method == 'POST':

        form = UserForm(request.POST)
        if form.is_valid():
            form.save()   # add data to database
            messages.success(request, "user added succesfully")
            return redirect('myapp:UserList')
    else:
        form = UserForm()
    return render(request, 'myapp/user_add.html', {'form': form, })


@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def UserUpdate(request, id):
    instance = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=instance)
        #print('in view')
        if form.is_valid():
            form.save()   # add data to database
            messages.success(request, "user updated successfuly")
            return redirect('myapp:UserList')
    else:
        form = UserUpdateForm(instance=instance)

    return render(request, 'myapp/user_update.html', {'form': form, 'id': id})


@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def UserDelete(request, id):
    data = get_object_or_404(User, id=id)
    try:
        data.delete()
        messages.success(request, "user deleted succesfully")
    except IntegrityError:
        messages.warning(request, "user cant deleted because of integrity")

    return redirect('myapp:UserList')



#------------------------------------category--------------------------------------
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def category_list(request):
    categories = Categories.objects.all()    #retrive all categories
    context = {'categories': categories}
    return render(request, 'myapp/categories_list.html', context)


# def detail_category(request, pk):
#     category = get_object_or_404(Categories, pk=pk)   #retrive single category
#     return render(request, 'myapp/categories_detail.html', {'category': category})

#create
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def new_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        #to see if the data is valid or not ..like form validation
        if form.is_valid():
            category = form.save(commit=False)  # add data to database
            category.save()
            return redirect('myapp:category_list')
    else:
        form = CategoryForm()
    return render(request, 'myapp/categories_add.html', {'form': form})

#update
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def edit_category(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()  # add data to database
            return redirect('myapp:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'myapp/categories_edit.html', {'form': form,'pk':pk})

#delete
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def delete_category(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    try:
        category.delete()
        messages.success(request, "Category deleted succesfully")
    except IntegrityError:
        messages.warning(request, "category cannot be deleted because of integrity")

    return redirect('myapp:category_list')