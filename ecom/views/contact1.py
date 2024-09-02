from django.shortcuts import render,redirect
from django.views import View
from ecom.models import Contact
from django.contrib import messages

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