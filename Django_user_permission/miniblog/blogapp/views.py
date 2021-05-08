from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Post
from .forms import SignupForm, LoginForm, AddPostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

#from django.contrib.auth.forms import UserCreationForm
# Create your views here.

# home
def home(request):
    posts=Post.objects.all()
    return render(request, 'blogapp/home.html',{'posts':posts})

# about
def about(request):
    return render(request,'blogapp/about.html')

# contact
def contact(request):
    return render(request,'blogapp/contact.html')

# dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blogapp/dashboard.html',{'posts':posts,
                                                         'full_name':full_name,
                                                         'groups':gps})
    else:
        return redirect('blogapp:login')


# signup
def user_signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            # add user into author group
            group=Group.objects.get(name='Author')
            user.groups.add(group)
            messages.success(request,'signup successfully.')
            return redirect('blogapp:login')
    else:
        form=SignupForm()

    return render(request,'blogapp/signup.html',{'form':form})

# logout
def user_logout(request):
    logout(request)
    return redirect('blogapp:home')

# user_login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user=authenticate(username=uname, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(request,'Login successful')
                    return redirect('blogapp:dashboard')
                else:
                    messages.warning(request,'Enter right credentials')
        else:
            form=LoginForm()
        return render(request, 'blogapp/login.html', {'form': form})
    else:
        return redirect('blogapp:dashboard')

# add post
def add_post(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=AddPostForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'blog added successfully!')
                return redirect('blogapp:dashboard')
        else:
            form=AddPostForm()
        return render(request,'blogapp/addpost.html',{'form':form})
    else:
        return redirect('blogapp:login')

# update post
# def add_post(request):
#     if request.user.is_authenticated:
#         if request.method=='POST':
#             form=AddPostForm(request.POST)
#             if form.is_valid():
#                 title=form.cleaned_data['title']
#                 description=form.cleaned_data['description']
#                 post=Post(title=title,description=description)
#                 post.save()
#                 form=AddPostForm()
#         else:
#             form=AddPostForm()
#         return render(request,'blogapp/addpost.html',{'form':form})
#     else:
#         return redirect('blogapp:login')

def update_post(request,id):
    if request.user.is_authenticated:
        instance=Post.objects.get(id=id)
        if request.method=='POST':
            form=AddPostForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'blog updated successfully!')
                return redirect('blogapp:dashboard')
        else:
            form=AddPostForm(instance=instance)
        return render(request,'blogapp/update.html',{'form':form})
    else:
        return redirect('blogapp:login')

# delete
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(id=id)
            pi.delete()
            messages.success(request,'blog deleted successfully')
            return redirect('blogapp:dashboard')
        return redirect('blogapp:dashboard')
    else:
        return redirect('blogapp:login')