from django.shortcuts import render
from .models import Destination
# Create your views here.

def index(request):
    dest1=Destination()
    dest1.name='Mumbai'
    dest1.descrip='The City that never sleeps.'
    dest1.price=600
    dest1.img='destination_1.jpg'
    dest1.offer=False

    dest2=Destination()
    dest2.name='Pune'
    dest2.descrip='The place for all educational instittues'
    dest2.price=700
    dest2.img='destination_2.jpg'
    dest1.offer=True

    dest3=Destination()
    dest3.name='Thane'
    dest3.descrip='Food Junction'
    dest3.price=150
    dest3.img='destination_3.jpg'
    dest1.offer=False


    dests=[dest1,dest2,dest3]
    return render(request,'index.html',{'dests':dests})