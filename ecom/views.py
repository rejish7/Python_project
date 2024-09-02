from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMessage,send_mail
from django.urls import reverse
from project_2 import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .tokens import activation_token
from django.db.models import F, Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required



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
def remove_from_cart(request,product_id):
    try:
            cart_item = CartItem.objects.get(user=request.user,product_id=product_id)
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
    except CartItem.DoesNotExist:
            messages.error(request, 'Item not found in cart.')
    return redirect('cart')

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



def about(request):
    testimonials = Testimonials.objects.all()
    data={
        'testimonials': testimonials
    }
    
    return render(request, 'pages/about/about.html',data)

def blog(request):
    return render(request,'pages/blog/blog.html')

def service (request):
    services = CompanyService.objects.all()
    data = {
        'serviceData': services, 
    }
    return render(request,'pages/service/service.html',data) 

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            phone=phone,
            message=message,
        )
        messages.success(request, 'We will contact you soon')
        return redirect("contact")
    else:
        data = {
            'contact': Contact.objects.first(),
        }
    
    return render(request, 'pages/contact/contact.html', data)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'pages/login/login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create password reset URL
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Send email with reset link
            subject = 'Password Reset Request'
            message = f'Please click the following link to reset your password: {reset_url}'
            recipient_list = [user.email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, message,from_email,recipient_list,fail_silently=True)
            
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('login')
        else:
            messages.error(request, 'No user found with that email address.')
    return render(request, 'pages/login/forgot.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'pages/login/password_reset_confirm.html')
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('login')



def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password: 
            messages.error(request, 'Passwords do not match.')
            return render(request, 'pages/login/signup.html')
        if User.objects.filter(name=name).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'pages/login/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'pages/login/signup.html')
        user = User.objects.create(name=name, email=email, password=password, phone=phone)
        user.is_active = False
        user.save()
        messages.success(request, 'You have successfully registered.')
        subject = 'Welcome to Our Site'
        message1 = f'''
        Dear {user.username},

        Welcome to TrendAura! We're thrilled to have you on board.

        Here are a few things you can do:
        1. Browse our wide range of products
        2. Check out our latest sales and discounts
        3. Update your profile for a personalized experience

        If you have any questions, feel free to contact our support team.

        Happy shopping!

        Best regards,
        The  TrendAura Team
        '''
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message1, from_email, recipient_list, fail_silently=True)

        current_site = get_current_site(request)
        email_subject = 'Activate your account.'
        message2 = render_to_string('login/activation_email.html',
        {
            'user1': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': activation_token.make_token(user),
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.send(fail_silently=True)

        return redirect('login')
    return render(request, 'pages/login/signup.html')
def activate(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Now you can login to your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')

def resend_activation_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
            current_site = get_current_site(request)
            email_subject = 'Activate your account.'
            message = render_to_string('pages/login/activation_email.html', {
                'user1': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': activation_token.make_token(user),
            })
            email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
            )
            email.send(fail_silently=True)
            messages.success(request, 'Activation email has been resent. Please check your email.')
        except User.DoesNotExist:
            messages.error(request, 'No inactive user found with this email address.')
        return redirect('login')
    return render(request, 'pages/login/signup.html')




# 


