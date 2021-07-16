from django.test import TestCase
from django.core.files import File
import mock
from django.conf import settings
import os

# Models to test
from .models import Brand, Product
# Create your tests here.

class BrandProductTestCase(TestCase):
    def test_brand_product(self):
        # Brand logo image mock
        logo_file = mock.MagicMock(spec=File)
        logo_file.name = 'logo.jpg'

        brand = Brand.objects.create(name="some_weird_brand_name_maybe", logo=logo_file)
        self.assertEqual(brand.logo.name, 'brandlogo/some_weird_brand_name_maybe.jpg')
        self.assertEqual(str(brand), 'some_weird_brand_name_maybe')

        product_image_file = mock.MagicMock(spec=File)
        product_image_file.name='product.jpg'
        product = Product.objects.create(brand=brand, grade='43', item_type='OPC', model='Weather Plus', weight=50, image=product_image_file)
        
        self.assertEqual(product.brand, brand)
    
        # removes the files after creation
        # remove logo
        os.remove(settings.MEDIA_ROOT / brand.logo.name)
        # remove product image
        os.remove(settings.MEDIA_ROOT / product.image.name)