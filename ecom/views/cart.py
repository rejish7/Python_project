from django.shortcuts import render,redirect
from django.views import View
from ecom.models import CartItem ,Order ,Checkout ,Notification
from django.contrib import messages
from ecom.utils import send_order_confirmation_email
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
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, 'Item quantity updated in cart.')
        except CartItem.DoesNotExist:
            CartItem.objects.create(
                user=request.user,
                product_id=product_id,
                quantity=quantity
            )
            messages.success(request, 'Item added to cart successfully.')
    
    return redirect('cart')

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
def remove_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        except CartItem.DoesNotExist:
            messages.error(request, 'Item not found in cart.')
    return redirect('cart')


@login_required
def order_confirmation(request, order_id):
    try:
        order = Checkout.objects.get(id=order_id, user=request.user)
        
        context = {
                'order': order,
        }
        
        return render(request, 'pages/cart/order_confirmation.html', context)
    except Checkout.DoesNotExist:
        messages.error(request, 'Order not found.')
    return redirect('home')



@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = cart_items.aggregate(
        total=Sum(F('quantity') * F('product__price'))
    )['total'] or Decimal('0')
    tax = cart_total * Decimal('0.10')
    total = cart_total + tax

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        street_address = request.POST.get('street_address')
        apartment = request.POST.get('apartment')
        town_city = request.POST.get('town_city')
        state_county = request.POST.get('state_county')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        order_notes = request.POST.get('order_notes')

        order = Checkout.objects.create(
            user=request.user,
            total_amount=total,
            first_name=first_name,
            last_name=last_name,
            country=country,
            street_address=street_address,
            apartment=apartment,
            town_city=town_city,
            state_county=state_county,
            postcode=postcode,
            phone=phone,
            email=email,
            order_notes=order_notes,
        )

        for item in cart_items:
            Order.objects.create(
                checkout=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()
        return redirect('payment_process', order_id=order.id)  

    data = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tax': tax,
        'total': total,
    }
    return render(request, 'pages/cart/checkout.html', data)

def payment_process(request, order_id):
    try:
        order = Checkout.objects.get(id=order_id, user=request.user)
    except Checkout.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('cart')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        # Redirect based on the selected payment method
        if payment_method in ['credit_card', 'debit_card']:
            return redirect('credit_card', order_id=order_id)
        elif payment_method == 'esewa':
            return redirect('esewa', order_id=order_id)
        elif payment_method == 'khalti':
            return redirect('khalti', order_id=order_id)
        elif payment_method == 'cash_on_delivery':
            order.status = 'pending'  # Set status to 'pending'
            order.save()
            send_order_confirmation_email(order)
            Notification.objects.create(
                user=order.user,
                order=order,
                message=f"New Cash on Delivery order #{order.id} has been placed."
            )
            messages.success(request, 'Your order has been placed successfully. You will pay upon delivery.')
            return redirect('order_confirmation', order_id=order.id)
        else:
            messages.error(request, 'Invalid payment method selected.')
            return redirect('payment_process', order_id=order_id)

    context = {
        'order': order,
    }
    return render(request, 'pages/cart/payment_process.html', context)  
