from django.contrib import admin
from .models import Category , Product  

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id' , 'name' ]
    prepopulated_fields = {'slug' : ['name']}
    search_fields = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['barcode' , 'name' , 'price' , 'category' , 'stock' , 'show_image']
    search_fields = ['barcode' , 'name']
    prepopulated_fields = {'slug' : ['name']}


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
