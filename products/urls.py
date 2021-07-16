from . import views
from django.urls import path

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('', views.index, name="products")
]
