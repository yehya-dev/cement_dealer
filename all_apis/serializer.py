from rest_framework import serializers
from products.models import Brand, Product, ProductOrder


class ProductSerializer(serializers.ModelSerializer):

    brand_name = serializers.SerializerMethodField('get_brand_name')

    class Meta:
        model = Product
        fields = ('id', 'brand', 'model', 'grade', 'weight', 'item_type', 'image', 'brand_name')

    def get_brand_name(self, product):
        return product.brand.name
        # TODO find an efficient way to get this done ?


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('get_product_full_name')

    class Meta:
        model = ProductOrder
        fields = ('id', 'product', 'quantity')

    def get_product_full_name(self, order):
        brand = order.product.brand.name
        grade = order.product.grade
        item_type = order.product.item_type
        return f"{brand} {item_type}{' ' + grade if grade else ''}"
