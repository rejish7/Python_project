from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from ecom.models import WishlistItem, Product, CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def wishlist(request):
        wishlist_items = WishlistItem.objects.filter(user=request.user)
    
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            if product_id:
                try:
                    product = Product.objects.get(id=product_id)
                    WishlistItem.objects.get_or_create(user=request.user, product=product)
                    messages.success(request, 'Item added to wishlist.')
                except Product.DoesNotExist:
                    messages.error(request, 'Product not found.')
            else:
                messages.error(request, 'Invalid request.')
    
        data = {
            'wishlist_items': wishlist_items
        }
        return render(request, 'pages/wishlist/wishlist.html', data)

@login_required
def add_to_cart_from_wishlist(request, product_id):
        try:
            wishlist_item = WishlistItem.objects.get(user=request.user, product_id=product_id)
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=wishlist_item.product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            wishlist_item.delete()
            messages.success(request, 'Item moved from wishlist to cart.')
        except WishlistItem.DoesNotExist:
            messages.error(request, 'Item not found in wishlist.')
        return redirect('wishlist')

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, 'Item added to wishlist.')
    else:
        messages.info(request, 'Item is already in your wishlist.')
    
    return redirect('product_detail', product_id=product_id)

@login_required
def remove_from_wishlist(request, product_id):
    try:
        wishlist_item = WishlistItem.objects.get(user=request.user, product_id=product_id)
        wishlist_item.delete()
        messages.success(request, 'Item removed from wishlist.')
    except WishlistItem.DoesNotExist:
        messages.error(request, 'Item not found in wishlist.')
    
    return redirect('wishlist')