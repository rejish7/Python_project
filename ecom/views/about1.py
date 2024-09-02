from django.shortcuts import render
from ecom.models import Testimonials
from django.views import View



def about(request):
    testimonials = Testimonials.objects.all()
    data={
        'testimonials': testimonials
    }
    
    return render(request, 'pages/about/about.html',data)
