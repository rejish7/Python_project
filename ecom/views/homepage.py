from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from ecom.models import Category,CompanyService,Banner,Product,Bestselling,WishlistItem,FAQ

def home(request):
    category = Category.objects.all()[:4]
    services = CompanyService.objects.all()[:4]
    banner = Banner.objects.all()
    products = Product.objects.all()[:6]
    bestselling = Bestselling.objects.all()
    wishlist_items = WishlistItem.objects.all()

    data = {
        'serviceData': services,
        'categories': category,
        'products': products,
        'banners': banner,
        'bestselling': bestselling,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'pages/home/index.html', data)

def blog(request):
    return render(request,'pages/blog/blog.html')

def service (request):
    services = CompanyService.objects.all()
    data = {
        'serviceData': services, 
    }
    return render(request,'pages/service/service.html',data) 

def payment (request):
    return render(request,'pages/extra/payment.html')

def faq (request):
    faq = FAQ.objects.all()
    data={
        'faq':faq,
    }
    return render(request,'pages/faq/faq.html',data)