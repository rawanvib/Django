from django.shortcuts import render

# Create your views here.
def home(request):
   ct= request.session.get('count',0) # if no value to count then assign zero
   newcount=ct+1
   request.session['count']=newcount
   return render(request,'webpagecount/home.html',
                 {'c':newcount})