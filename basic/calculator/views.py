from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'home.html')

def calc(request):
    val1=int(request.POST['num1'])
    val2=int(request.POST['num2'])
    add=val1+val2
    sub=val1-val2
    mul=val1*val2
    div=val1/val2

    return render(request,'result.html',{'addition':add,'subtraction':sub,'multiply':mul,'division':div})