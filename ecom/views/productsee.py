from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ecom.models import Category, Product,Review


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

def product_detail(request, id):
    products = get_object_or_404(Product, id=id)
    categories = Category.objects.all()
    review = Review.objects.filter(product=products).first()
    # size = products.size.first()  # Assuming there's a related field for size
    
    data = {
        'products': products,
        'categories': categories,
        'review': review,
        # 'size': size,
    }
    return render(request, 'pages/product/product_detail.html', data)

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


















