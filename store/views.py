from django.shortcuts import render , get_object_or_404
from store.models import Category , Product , Cart , CartItem
from django.urls import reverse
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger


# Create your views here.

def index(request , category_slug=None):
    product = None
    category_page = None

    if category_slug != None:
        category_page = get_object_or_404(Category , slug = category_slug)
        product = Product.objects.all().filter(category=category_page)
    else : 
        product = Product.objects.all().filter()

    paginator = Paginator(product,8)
    page = request.GET.get('page')
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'product' :  product ,
        'category' : category_page
    })

def product(request):
    return render(request, 'product.html')

#สร้าง Session
def _cart_id(request):
   cart = request.session.session_key
   if not cart:
        cart = request.session.create()
        return cart()

def addCart(request , product_id):
    #มันส่งจะไอดีมาจากนั้น ไอดีจะเป็นตังดึงสินค้าออกมาตามรหัส
    product = Product.objects.get(id=product_id)
    #สร้างตะกร้าสินค้า
    try:
        cart = Cart.objects.get(cart_id = _cart_id (request) ) #เคยสร้างตะกร้าสินค้ามาแล้ว
    except  Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id (request)) #ไม่เคยสร้างตะกร้าสินค้ามาแล้ว
        cart.save() #บันทึกเข้าฐานข้อมูล

        
    try:
        #ซื้อรายการสินค้าซ้ำ
        cart_item = CartItem.objects.get(product = product , cart = cart)
        if cart_item.quantity < cart_item.product.stock : 
            #เปลี่ยนจำนวนรายการสินค้า
            cart_item.quantity+=1
            # บันทึก / อัพเดทค่า
            cart_item.save()
    except CartItem.DoesNotExist: 
        #ซื้อรายการสินค้าครั้งแรก
        cart_item = CartItem.create(
            product = product , 
            cart = cart,
            quantity = 1
        )
        cart_item.save()