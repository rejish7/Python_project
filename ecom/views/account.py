from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
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
from ecom.tokens import activation_token
from django.db.models import F, Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required

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