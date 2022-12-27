from django.shortcuts import render, get_object_or_404, redirect
from store.models import Category, Product, Cart, CartItem , Order
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login , authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required (login_url='signIn')
def pos(request, category_slug=None):
    product = None
    category_page = None

    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        product = Product.objects.all().filter(category=category_page)
    else:
        product = Product.objects.all().filter()

    paginator = Paginator(product, 12)
    page = request.GET.get('page')
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

    total = 0
    cost = 0
    counter = 0
    cart_items = None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # ดึงตะกร้าสินค้ามา
        cart_items = CartItem.objects.filter(
            cart=cart, active=True)  # ดึงข้อมูลสินต้าในตะกร้า
        
        for item in cart_items:
            total += (item.product.price*item.quantity)
            cost += (item.product.cost*item.quantity)
            counter += item.quantity
        product = Product.objects.filter(name__contains=request.GET ['title'])
    except Exception as e:
        pass
    
    
    
    return render(request, 'pos.html', {
        'product':  product,
        'category': category_page,
        'cart_items': cart_items,
        'total': total,
        'cost': cost,
        'counter': counter
    })

def Checkout(request):
    return render(request, 'checkout.html')


def product(request):
    return render(request, 'product.html')


def index(request):
    return render(request, 'index.html')




# สร้าง Session
def _cart_id(request):
   cart = request.session.session_key
   if not cart:
       cart = request.session.create()
       return cart


def addCart(request, product_id):
    # มันส่งจะไอดีมาจากนั้น ไอดีจะเป็นตังดึงสินค้าออกมาตามรหัส
    product = Product.objects.get(id=product_id)
    # สร้างตะกร้าสินค้า
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        # บันทึกเข้าฐานข้อมูล

    try:
        # ซื้อรายการสินค้าซ้ำ
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            # เปลี่ยนจำนวนรายการสินค้า
            cart_item.quantity += 1
            # บันทึก / อัพเดทค่า
            cart_item.save()
    except CartItem.DoesNotExist:
        # ซื้อรายการสินค้าครั้งแรก
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    return redirect('/')

    


def removeCart(request, product_id):
    # ทำงานกับตะกร้าสินค้า
    cart = Cart.objects.get(cart_id=_cart_id(request))  # ดึงตะกร้าสินค้ามา
    # ทำงานกับสินค้าที่จะลบ
    product = get_object_or_404(Product, id=product_id)
    cartItem = CartItem.objects.get(product=product, cart=cart)
    # ลบรายการสินค้า 1 ออกจากตะกร้า A โดยลบจาก รายการสินค้าในตะกร้า (CartItem)
    cartItem.delete()
    return redirect('/')

def signInView(request):
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None :
                login(request,user)
                return redirect('pos')
            else :
                messages.error(request,"Invalid username or password.")
    else:
        messages.error(request,"Invalid username or password.")
        form=AuthenticationForm()
    return render(request,'signIn.html',{'form':form})

def signOutView(request):
    logout(request)
    return redirect('signIn')


