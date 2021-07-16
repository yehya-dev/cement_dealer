from django.db import models
from userprofiles.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ColorOverlay

# Create your models here.

def get_brandlogo_filename(instance, filename):
    file_ext = filename.split('.')[-1]
    return f'brandlogo/{instance.name.lower()}.{file_ext}'

def get_productimage_filename(instance, filename):
    file_ext = filename.split('.')[-1]
    return f'productimage/{str(instance).lower()}.{file_ext}'

class Brand(models.Model):
    name = models.CharField(max_length=30)
    logo = models.ImageField(upload_to=get_brandlogo_filename)

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    GRADE_OPTIONS = [
        ('43', '43'),
        ('53', '53'),
        ('', None)
    ]
    TYPE_OPTIONS = [
        ('OPC', 'OPC'),
        ('PPC', 'PPC')
    ]
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, null=True, blank=True, choices=GRADE_OPTIONS, default=None)
    item_type = models.CharField(max_length=3, choices=TYPE_OPTIONS)
    model = models.CharField(max_length=50, null=True, blank=True)
    weight = models.FloatField(default=50.0)
    image = models.ImageField(upload_to=get_productimage_filename)

    def __str__(self) -> str:
        return f"{self.brand}-{self.grade}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='ProductOrder')
    submitted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Order created by {self.user}"

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.order.user} added {self.product}"
