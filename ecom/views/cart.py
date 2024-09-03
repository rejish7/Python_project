from django.shortcuts import render,redirect
from django.views import View
from ecom.models import CartItem,Order
from django.contrib import messages
from django.db.models import F, Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = cart_items.aggregate(
        total=Sum(F('quantity') * F('product__price'))
    )['total'] or Decimal('0')
    tax = cart_total * Decimal('0.10')
    total = cart_total + tax

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tax': tax,
        'total': total
    }
    return render(request, 'pages/cart/cart.html', context)


@login_required
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        
        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            messages.success(request, 'Cart updated successfully.')
        except CartItem.DoesNotExist:
            messages.error(request, 'Item not found in cart.')
    
    return redirect('cart')

@login_required
def remove_cart(request, product_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        except CartItem.DoesNotExist:
            messages.error(request, 'Item not found in cart.')
    return render(request, 'pages/cart/remove_cart.html')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = cart_items.aggregate(
        total=Sum(F('quantity') * F('product__price'))
    )['total'] or Decimal('0')
    tax = cart_total * Decimal('0.10')
    total = cart_total + tax

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_amount=total
        )
        for item in cart_items:
            Order.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        cart_items.delete()
        
        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_confirmation', order_id=order.user)

    data = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tax': tax,
        'total': total,
    }
    return render(request, 'pages/cart/checkout.html', data)

