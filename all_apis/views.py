from rest_framework import generics
from products.models import Brand, Product, ProductOrder
from .serializer import ProductSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Temporary TODO REMOVE 
import time

@api_view(['POST'])
def orderProduct(request):
        try:
            if not request.user.is_authenticated:
                raise ValueError('User Not Authenticated')

            product_id = str(request.data.get('product_id'))
            quantity = str(request.data.get('quantity'))

            product = Product.objects.get(id=product_id)

            if not (product_id and quantity and product and product_id.isdecimal() and quantity.isdecimal()):
                raise ValueError('Invalid Data Passed')
            
            product_id = int(product_id)
            quantity = int(quantity)

            userOrder = request.user.order_set.filter(submitted=False).first()
            if not userOrder:
                userOrder = request.user.order_set.create()
            
            newProduct = ProductOrder(product=product, order=userOrder, quantity=quantity)
            newProduct.save()

            return Response({
                'status': True
            })
        except ValueError as e:
            return Response({
                'status': False,
                'message': str(e)
            })


class OrderList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        userOrder = self.request.user.order_set.filter(submitted=False).first()
        if userOrder:
            return ProductOrder.objects.filter(order=userOrder).all()
        else:
            return ProductOrder.objects.none()

    serializer_class = OrderSerializer

@api_view(['PUT'])
def updateOrder(request):
    try:
        if not request.user.is_authenticated:
            raise ValueError("User is not authenticated")

        order_id = request.data.get('order_id')
        quantity = int(request.data.get('quantity'))
        if not (order_id and quantity and type(quantity) == int and type(order_id) == int and quantity > 0):
            raise ValueError("invalid values passed")

        orderItem = ProductOrder.objects.get(pk=order_id)
        orderItem.quantity = quantity
        orderItem.save()
        return Response({
            'status': True
        })
    except (ValueError, ProductOrder.DoesNotExist) as e:
        return Response({
            'status': False,
            'message': str(e)
        })

@api_view(['POST'])
def deleteOrder(request):
    try:
        if not request.user.is_authenticated:
            raise ValueError("User is not authenticated")

        order_id = request.data.get('order_id')
        if not (order_id and type(order_id) == int):
            raise ValueError("Invalid values passed")

        orderItem = ProductOrder.objects.get(pk=order_id)
        if orderItem:
            orderItem.delete()
        return Response({
            'status': True
        })

    except (ValueError, ProductOrder.DoesNotExist) as e:
        return Response({
            'status': False,
            'message': str(e)
        })

class ProductList(generics.ListAPIView):
    def get_queryset(self):
        # time.sleep(1) # TODO Remove this on production 
        # raise ValueError # To simulate a server error on api call
        brand_id = self.kwargs['pk']
        brand = Brand.objects.get(pk=brand_id)
        return brand.product_set.all()
    serializer_class = ProductSerializer
