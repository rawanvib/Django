from django.shortcuts import render
from .documents import ProductDocument
from blog.models import Product

# Create your views here.
def search(request):
    q = request.GET.get('q')
    if q:
        products = ProductDocument.search().query('match', title=q)
    else:
        products=''

    return render(request, 'search/search.html', {'products':products})