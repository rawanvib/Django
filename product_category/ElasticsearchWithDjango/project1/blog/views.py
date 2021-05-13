from django.shortcuts import render
from .models import Product
# Create your views here.
def home(request):
    data=Product.objects.all()
    return render(request,'blog/home.html',{"data":data})