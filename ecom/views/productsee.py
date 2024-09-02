from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ecom.models import Category, Product


def product(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    product = products.first()
    
    data = {
        'categories': categories,
        'product': product,
        'products':products
    }
    return render(request, 'pages/product/product.html', data)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    
    data = {
        'product': product,
        'categories': categories
    }
    return render(request, 'pages/product/product.html', data)

def product_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    
    data = {
        'category': category,
        'products': products,
        'categories': categories
    }
    return render(request, 'pages/product/product.html', data)


















