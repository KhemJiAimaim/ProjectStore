from django.shortcuts import render , get_object_or_404
from store.models import Category , Product  
from django.urls import reverse

# Create your views here.

def index(request , category_slug=None):
    product = None
    category_page = None

    if category_slug != None:
        category_page = get_object_or_404(Category , slug = category_slug)
        product = Product.objects.all().filter(category=category_page)
    else : 
        product = Product.objects.all().filter()

    return render(request, 'index.html', {
        'product' :  product ,
        'category' : category_page
    })



def product(request):
    return render(request, 'product.html')