"""DjangoPOS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.urls import re_path
from store import views 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', views.product),
    path('index/', views.index),
    path('', views.pos , name="pos"),
    path('category/<slug:category_slug>' , views.pos, name="product_by_category"),
    path('cart/add/<int:product_id>', views.addCart , name="addCart"),
    path('cart/remove/<int:product_id>', views.removeCart , name="removeCart"),
    path('account/login',views.signInView,name="signIn"),
    path('account/logout',views.signOutView,name="signOut"),
    path('checkout/',views.Checkout,name='checkout'),
    #path('cartdetail/',views.cartdetail,name="cartdetail"),
]

if settings.DEBUG :
    #media/product
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #static/
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #static//media/product
