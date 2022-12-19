from django.contrib import admin
from .models import Category , Product , Cart , CartItem

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id' , 'name' ]
    prepopulated_fields = {'slug' : ['name']}
    search_fields = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['barcode' , 'name' , 'category' , 'price' , 'stock' , 'show_image']
    search_fields = ['barcode' , 'name']
    prepopulated_fields = {'slug' : ['name']}
    list_editable=['price' , 'stock']
    list_per_page = 10

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)