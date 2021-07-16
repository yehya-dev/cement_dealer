from django.shortcuts import render
from .models import Brand
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Create your views here.
def index(request):
    brands = Brand.objects.all()
    return render(request, 'products/index.html', {
        'brands': brands,
    })

@login_required
def cart(request):
    return render(request, 'cart/index.html')