from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber
from phonenumber_field.phonenumber import to_python as PhoneNumber
# Create your models here.

class Address(models.Model):
    class Meta:
        verbose_name_plural = 'Addresses'
        
    DISTRICT_OPTIONS = [
        ('KN', 'Kannur'),
        ('KS', 'Kasaragod'),
        ('KZ', 'Kozhikode'),
        ('MA', 'Malappuram'),
        ('WA', 'Wayanad'),
        ('TS', 'Thrissur'),
        ('ER', 'Ernakulam'),
        ('ID', 'Idukki'),
        ('KT', 'Kottayam'),
        ('AL', 'Alappuzha'),
        ('TV', 'Thiruvananthapuram'),
        ('KL', 'Kollam'),
        ('PL', 'Palakkad'),
        ('PT', 'Pathanamthitta'),
    ]

    landmark = models.CharField(max_length=100)
    town = models.CharField(max_length=50)
    district = models.CharField(max_length=20, choices=DISTRICT_OPTIONS)
    pincode = models.CharField(max_length=6)
    # implement choices for state and district using https://docs.djangoproject.com/en/3.1/ref/models/fields/#choices

    def __str__(self) -> str:
        return f"{self.town}, {self.district}, {self.pincode}"

 
class CustomAccountManager(BaseUserManager):

    def create_user(self, phone, first_name, last_name, password, **other_fields):
        if not phone:
            raise ValueError('You must provide a valid phone number')

        validate_international_phonenumber(phone)

        # Remove below three line to allow international phone numbers
        phoneNumberObj = PhoneNumber(phone)
        if phoneNumberObj.country_code != 91:
            raise ValueError('Please enter a valid Indian Phone Number')
        # App indented to be used only in India
            
        if other_fields.get('is_superuser') or other_fields.get('is_staff'):
            user = self.model(phone=phone, first_name=first_name, last_name=last_name, **other_fields)
        else:
            if not all((
                other_fields.get('landmark'),
                other_fields.get('town'),
                other_fields.get('district'),
                other_fields.get('pincode')
                )
            ):
                raise ValueError('You must provide landmark, town, district, pincode for a user')

            user_address = Address(
                landmark=other_fields.get('landmark'),
                town=other_fields.get('town'),
                district=other_fields.get('district'),
                pincode=other_fields.get('pincode')
            )
            user_address.save()
            user = self.model(phone=phone, first_name=first_name, last_name=last_name, address=user_address, gstin=other_fields.get('gstin'))

        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, phone, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned is_superuser=True.')
        return self.create_user(phone, first_name, last_name, password, **other_fields)     


class User(AbstractBaseUser, PermissionsMixin):
    phone = PhoneNumberField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, null=True)
    # TODO Currently User is Deleted we we delete an address, make that the other way around
    account_created = models.DateTimeField(auto_now_add=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomAccountManager()

    def __str__(self) -> str:
        return f"{self.first_name} - {self.phone}"

    def fullname(self):
        return f"{self.first_name} {self.last_name}"
