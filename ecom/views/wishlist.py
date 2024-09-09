from django.shortcuts import render,redirect
from django.views import View
from ecom.models import WishlistItem, Product, CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def wishlist(request):
        wishlist_items = WishlistItem.objects.filter(user=request.user) 
        
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
def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        try:
            wishlist_item = WishlistItem.objects.get(user=request.user, product_id=product_id)
            wishlist_item .save()
        except WishlistItem.DoesNotExist:
            WishlistItem.objects.create(
                user=request.user,
                product_id=product_id,
            )
            messages.success(request, 'Product added to Wishlist')
    
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            wishlist_item = WishlistItem.objects.get(user=request.user, product_id=product_id)
            wishlist_item .delete()
            messages.success(request, 'Item removed from cart.')
        except WishlistItem.DoesNotExist:
            messages.error(request, 'Item not found in cart.')
    return redirect('wishlist')