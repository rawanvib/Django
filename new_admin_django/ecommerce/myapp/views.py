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

from .forms import UserForm, OldPassForm,UserUpdateForm,CategoryForm, ProductImageForm, ProductForm, ProductMetaForm
from .forms import ProductAttributeForm,ProductAttributeEditForm,ProductAttributeValueForm, ProductAttributeAssociationForm , BannerForm
from .models import User, Categories,Product,ProductAttributeValue, ProductAttributeAssociation, ProductImage, ProductMeta,ProductAttribute
from .models import Banner


from django.forms import inlineformset_factory

from .decorators import unauthenticated_user, allowed_users

# Create your views here.
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def index(request):
    return render(request, 'myapp/starter.html')


# @unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        valuenext = request.POST.get('next')
        user = authenticate(request, username=username, password=password)
        groups = request.user.groups.values_list('name', flat = True)
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
# def UserChangePsw(request,id):
def UserChangePsw(request):
    # instance=get_object_or_404(User, id=id)
    instance = request.user
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
            instance = form.save(commit=False)  # add data to database
            instance.created_by = request.user
            instance.modify_by = request.user
            instance.save()
            messages.success(request, "category added succesfully")
            return redirect('myapp:category_list')
    else:
        form = CategoryForm()
    return render(request, 'myapp/categories_add.html', {'form': form})

#update
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def edit_category(request, pk):
    instance = get_object_or_404(Categories, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.modify_by = request.user
            instance.save()  # add data to database
            messages.success(request, "category updated successfuly")
            return redirect('myapp:category_list')
    else:
        form = CategoryForm(instance=instance)
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

#---------------------------product attribute----------------------------#

@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def Product_Attribute(request):
    product_attributes = ProductAttribute.objects.all()

    return render(request, 'attribute/product_attribute.html', {'product_attributes': product_attributes})

@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def Product_Attribute_Add(request):

    if request.method == 'POST':
        form=ProductAttributeForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.created_by = request.user
            instance.modified_by = request.user
            instance.save()
            messages.success(request, "Attribute added succesfully")
            return redirect('myapp:ProductAttribute')
    else:
        form=ProductAttributeForm()
    return render(request, 'attribute/product_attribute_add.html', {'form': form})

@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def Product_Attribute_Edit(request,id):
    instance=get_object_or_404(ProductAttribute,id=id)
    if request.method == 'POST':
        form = ProductAttributeEditForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.modified_by = request.user
            instance.save()
            messages.success(request, "Attribute edited succesfully")
            return redirect('myapp:ProductAttribute')
    else:
        form = ProductAttributeEditForm(instance=instance)
    return render(request, 'attribute/product_attribute_edit.html', {'form': form,'id':id})

@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def Product_Attribute_Delete(request,id):
    data = get_object_or_404(ProductAttribute, id=id)
    try:
        data.delete()
        messages.success(request, "product attribute deleted succesfully")
    except IntegrityError:
        messages.warning(request, "product attribute have products so cant delete")

    return redirect('myapp:ProductAttribute')

#---------------------------product attribute----------------------------#

@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def Product_Attribute_Value(request):
    product_attribute_values = ProductAttributeValue.objects.all()
    return render(request, 'attribute/product_att_value.html', {'product_attribute_values': product_attribute_values})

@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def Product_Attribute_Value_Add(request):
    if request.method == 'POST':
        form = ProductAttributeValueForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.modified_by = request.user
            instance.save()
            messages.success(request, "Attribute value added succesfully")
            return redirect('myapp:ProductAttributeValue')
    else:
        form = ProductAttributeValueForm()
    return render(request, 'attribute/product_att_value_add.html', {'form': form})


@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def Product_Attribute_Value_Edit(request,id):
    instance=get_object_or_404(ProductAttributeValue,id=id)
    if request.method=="POST":
        form = ProductAttributeValueForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.modify_by = request.user
            instance.save()
            # form.save_m2m()
            messages.success(request, "product attribute value updated successfuly")
            return redirect('myapp:ProductAttributeValue')
    else:
        form = ProductAttributeValueForm(instance=instance)
    return render(request, 'attribute/product_att_value_edit.html', {'form': form, 'id': id})


@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def Product_Attribute_Value_Delete(request,id):
    data = get_object_or_404(ProductAttribute, id=id)
    try:
        data.delete()
        messages.success(request, "attribute value deleted succesfully")
    except IntegrityError:
        messages.warning(request, "product attribute have products so cant delete")
    return redirect('myapp:ProductAttributeValue')


#---------------------------products----------------------------#
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def product_list(request):
    products = Product.objects.all()  # retrive all categories
    context = {'products': products}
    return render(request, 'myapp/products_list.html', context)

@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def add_new_product(request):
    ProductImageFormSet=inlineformset_factory(Product, ProductImage,form=ProductImageForm,extra=1)
    ProductAttributeFormset=inlineformset_factory(Product, ProductAttributeAssociation,form=ProductAttributeAssociationForm,extra=2)
    ProductMetaFormset=inlineformset_factory(Product, ProductMeta,form=ProductMetaForm,extra=1)

    if request.method == "POST":
        form1 = ProductForm(request.POST)
        formset1 = ProductImageFormSet(request.POST, request.FILES)
        formset2 = ProductMetaFormset(request.POST)
        formset3 = ProductAttributeFormset(request.POST)

        if form1.is_valid() and formset1.is_valid() and formset2.is_valid() and formset3.is_valid():
            #Each query is immediately committed to the db
            with transaction.atomic():
                instance = form1.save(commit=False)
                instance.created_by=request.user
                instance.modified_by=request.user
                instance.save()
                form1.save_m2m()

                for image in formset1:
                    if image.is_valid():
                        image=image.save(commit=False)
                        image.product=instance
                        image.save()

                for data in formset2:
                    if data.is_valid():
                        data=data.save(commit=False)
                        data.product=instance
                        data.save()

                for attribute in formset3:
                    if attribute.is_valid() and attribute.has_changed():
                        attribute=attribute.save(commit=False)
                        attribute.product_id=instance
                        attribute.save()

                messages.success(request,"Product added successfully")
            return redirect("myapp:ProductList")
    else:
        form1 = ProductForm()
        formset1 = ProductImageFormSet()
        formset2 = ProductMetaFormset()
        formset3 = ProductAttributeFormset()
    return render(request,"myapp/product_add.html",{'form1':form1,
                                                    'formset1':formset1,
                                                    'formset2':formset2,
                                                    'formset3':formset3})

@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1)
    ProductAttributeFormset = inlineformset_factory(Product, ProductAttributeAssociation,
                                                    form=ProductAttributeAssociationForm, extra=1)
    ProductMetaFormset = inlineformset_factory(Product, ProductMeta, form=ProductMetaForm, extra=1)

    if request.method == 'POST':
        form1 = ProductForm(request.POST, instance=product)
        formset1 = ProductImageFormSet(request.POST, request.FILES, instance=product)
        formset2 = ProductMetaFormset(request.POST, instance=product)
        formset3 = ProductAttributeFormset(request.POST, instance=product)

        if form1.is_valid() and formset1.is_valid() and formset2.is_valid() and formset3.is_valid():
            with transaction.atomic():
                # import pdb
                # pdb.set_trace()
                instance = form1.save(commit=False)
                instance.modify_by = request.user
                instance.save()
                form1.save_m2m()
                formset3.save()

                for image in formset1:
                    if image.is_valid() and image.has_changed():
                        image = image.save(commit=False)
                        image.product = instance
                        image.save()

                instance2 = formset1.save(commit=False)
                for obj in formset1.deleted_objects:
                    obj.delete()

                instance3 = formset2.save(commit=False)
                for obj in formset2.deleted_objects:
                    obj.delete()

                instance4 = formset3.save(commit=False)
                for obj in formset3.deleted_objects:
                    obj.delete()

                messages.success(request, "product edited succesfully")
            return redirect('myapp:ProductList')

    else:
        form1 = ProductForm(request.GET or None, instance=product)
        formset1 = ProductImageFormSet(instance=product)
        formset2 = ProductMetaFormset(instance=product)
        formset3 = ProductAttributeFormset(instance=product)

    return render(request, 'myapp/product_edit.html',
                  {'form1': form1, 'formset1': formset1, 'formset2': formset2,'formset3':formset3, 'id': id})

# def load_product_attribute_value(request):
#     product_attribute_id = request.GET.get('product_attribute_id')
#     print(product_attribute_id)
#     product_attribute_value_ids = ProductAttributeValue.objects.filter(attribute_name=product_attribute_id)
#     return render(request, 'attribute/product_attribute_list_options.html',
#                   {'product_attribute_value_ids': product_attribute_value_ids})


@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    try:
        product.delete()
        messages.success(request, "Product deleted succesfully")
    except IntegrityError:
        messages.warning(request, "Product cannot be deleted because of integrity")
    return redirect('myapp:ProductList')


#________________________________________Banner__________________________________________#
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def banner_list(request):
    banner=Banner.objects.all()
    return render(request,'myapp/banner.html',{'banners':banner})

@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def new_banner(request):
    if request.method=='POST':
        form=BannerForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            messages.success(request,"Banner added successfully.")
            return redirect('myapp:BannerList')
    else:
        form=BannerForm()
    return render(request,'myapp/banner_add.html',{'form':form})

@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def edit_banner(request, id):
    banner = get_object_or_404(Banner, id=id)
    if request.method == "POST":
        form =BannerForm(request.POST, instance=banner)
        if form.is_valid():
            banner = form.save(commit=False)
            #instance.modify_by = request.user
            banner.save()  # add data to database
            messages.success(request, "banner updated successfuly")
            return redirect('myapp:BannerList')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'myapp/banner_edit.html', {'form': form,'id':id})

#delete
@login_required(login_url='myapp:login')
@allowed_users(allowed_roles=['admin'])
def delete_banner(request, id):
    instance = get_object_or_404(Banner, id=id)
    try:
        instance.delete()
        messages.success(request, "banner deleted succesfully")
    except IntegrityError:
        messages.warning(request, "banner cannot be deleted because of integrity")

    return redirect('myapp:BannerList')
