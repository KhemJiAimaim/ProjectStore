from django.urls import reverse
from django.db import models
from django.utils.html import format_html


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ['id'] #เรียงจากน้อยไปมาก ถ้า -id จะเป็นจากมากไปน้อย
        verbose_name = 'หมวดหมู่สินค้า'
        verbose_name_plural = 'ข้อมูลหมวดหมู่สินค้า'

    def get_url(self):
        return reverse('product_by_category' , args=[self.slug])

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category, null=True , blank=True , on_delete=models.CASCADE , unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product' , blank=True , unique=True)
    barcode = models.CharField(max_length=255,unique=True)
    created = models.DateTimeField(auto_now_add=True) #วัน-เวลาเพิ่มสินค้า
    updated = models.DateTimeField(auto_now = True) #วัน-เวลาที่แก้ไขสินค้า

    class Meta: 
        ordering = ['id'] #เรียงจากน้อยไปมาก ถ้า -id จะเป็นจากมากไปน้อย
        verbose_name = 'คลังสินค้า'
        verbose_name_plural = 'ข้อมูลสินค้า'

    def show_image(self):
        if self.image:
            return format_html('<img src= '+self.image.url+' height= "80px" >' )
        return ''
    show_image.allow_tags = True

    def __str__(self) :
        return self.name

class Cart(models.Model):
    cart_id = models.CharField(max_length=255,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True) #วัน-เวลาเพิ่มขุ้อมูลสินค้า

    def __str__(self):
        return str(self.cart_id)
    
    class Meta:
        db_table = 'cart'
        ordering = ['date_added']
        verbose_name = 'ตะกร้าสินค้า'
        verbose_name_plural = 'ข้อมูลตะกร้าสินค้า'

class CartItem(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'cartItem'
        verbose_name = 'รายการสินค้า'
        verbose_name_plural = 'ข้อมูลรายการสินค้า'
        
    #ผลรวมราคาขาย
    def sub_total(self):
        return self.product.price * self.quantity
    
    #ผลรวมต้นทุน
    def sub_cost(self):   
        return self.product.cost * self.quantity

    def __str__(self):
        return str(self.product.name)


class Order(models.Model):
    amount=models.DecimalField(max_digits=10,decimal_places=2) #เงินที่จ่าย
    total=models.DecimalField(max_digits=10,decimal_places=2)
    token=models.CharField(max_length=255,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta :
        db_table='Order'
        ordering=('id',)

    def __str__(self):
        return str(self.id)

    def sub_amount(self):
        return self.amount - (self.product.price * self.quantity)


class OrderItem(models.Model):
    product=models.CharField(max_length=250)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    

    class Meta :
        db_table='OrderItem'
        ordering=('order',)

    def sub_total(self):
        return self.quantity*self.price
    
    def __str__(self):
        return self.product
        
