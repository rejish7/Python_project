from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ecom.models import Order, WishlistItem, UserProfile
from ecom.forms import UserProfileForm
from django.core.mail import EmailMessage, send_mail
from django.urls import reverse
from project_2 import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from ecom.tokens import activation_token
from django.db.models import F, Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required
User = get_user_model()
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.', extra_tags='timeout-5000')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.', extra_tags='timeout-5000')
    return render(request, 'pages/account/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.', extra_tags='timeout-5000')
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            subject = 'Password Reset Request'
            message = f'Please click the following link to reset your password: {reset_url}'
            recipient_list = [user.email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            
            messages.success(request, 'Password reset link has been sent to your email.', extra_tags='timeout-5000')
            return redirect('login')
        else:
            messages.error(request, 'No user found with that email address.')
    return render(request, 'pages/account/forgot.html')

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
                messages.success(request, 'Your password has been reset successfully.', extra_tags='timeout-5000')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'pages/account/password_reset_confirm.html')
    else:
        messages.error(request, 'The password reset link is invalid or has expired.', extra_tags='timeout-5000')
        return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'pages/account/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'pages/account/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'pages/account/signup.html')
        
        if UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already exists.')
            return render(request, 'pages/account/signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()
        UserProfile.objects.create(user=user, phone=phone)
        
        messages.success(request, 'You have successfully registered.', extra_tags='timeout-5000')
        
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
        The TrendAura Team
        '''
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message1, from_email, recipient_list, fail_silently=True)

        current_site = get_current_site(request)
        email_subject = 'Activate your account.'
        message2 = render_to_string('pages/account/activation_email.html', {
            'user': user,
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
    return render(request, 'pages/account/signup.html')

def activate(request, uid, token):
    user = get_object_or_404(User, pk=force_str(urlsafe_base64_decode(uid)))
    if activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Thank you for your email confirmation. Now you can login to your account.', extra_tags='timeout-5000')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!', extra_tags='timeout-5000')
        return redirect('home')

def resend_activation_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
            current_site = get_current_site(request)
            email_subject = 'Activate your account.'
            message = render_to_string('pages/account/activation_email.html', {
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
            messages.success(request, 'Activation email has been resent. Please check your email.', extra_tags='timeout-5000')
        except User.DoesNotExist:
            messages.error(request, 'No inactive user found with this email address.', extra_tags='timeout-5000')
        return redirect('login')
    return render(request, 'pages/account/signup.html')

@login_required
def dashboard(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    wishlist_items = WishlistItem.objects.filter(user=user)
    
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.', extra_tags='timeout-5000')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'user': user,
        'orders': orders,
        'wishlist_items': wishlist_items,
        'form': form,
    }
    return render(request, 'pages/account/dashboard.html', context)

@login_required
def update_account(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('display_name')
        user.email = request.POST.get('email')

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if current_password and new_password and confirm_new_password:
            if user.check_password(current_password):
                if new_password == confirm_new_password:
                    user.set_password(new_password)
                    messages.success(request, 'Your password has been updated.', extra_tags='timeout-5000')
                    user.save()
                else:
                    messages.error(request, 'New passwords do not match.', extra_tags='timeout-5000')
            else:
                messages.error(request, 'Current password is incorrect.', extra_tags='timeout-5000')
    return redirect('dashboard')

@login_required
def edit_address(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your address has been updated.', extra_tags='timeout-5000')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
    }
    return render(request, 'pages/account/edit_address.html', context)
