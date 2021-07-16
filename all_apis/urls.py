from django.urls import path
from .views import ProductList, orderProduct, OrderList, updateOrder, deleteOrder

app_name = 'api'
urlpatterns = [
    path('productlist/<int:pk>/', ProductList.as_view(), name="productsList"),
    path('orderlist/', OrderList.as_view(), name="orderView"),
    path('updateorder/', updateOrder, name="updateOrder"),
    path('deleteorder/', deleteOrder, name="deletOrder"),
    path('orderproduct/', orderProduct, name='orderProduct')
]
