from django.shortcuts import render
from .models import Address, User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from phonenumber_field.validators import validate_international_phonenumber
from phonenumber_field.phonenumber import to_python as PhoneNumber
import re
from django.contrib import messages
from django.db import IntegrityError
from twilio.rest import Client
import json
from django.contrib import auth

# TODO Replace with os.environ! Important
# Twilo Service Keys
account_sid = ''
auth_token = ''
service_id = ''


# Validation Helper Functions 
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def isValidGST(number):
    regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}" + "[A-Z]{1}[1-9A-Z]{1}" + "Z[0-9A-Z]{1}$"
    regComp = re.compile(regex)
    if re.search(regComp, number):
        return True
    else:
        return False

def verifyOTP(phoneNumber, code):
    try:
        client = Client(account_sid, auth_token)
        verification_check = client.verify \
                            .services(service_id) \
                            .verification_checks \
                            .create(to=str(phoneNumber), code=str(code))
    except:
        raise ValueError("Couldn't verify the entered OTP")
    else:
        if verification_check.status != 'approved':
            raise ValueError('The entered OTP is incorrect')

def validateFormData(formData):
    firstName = formData.get('firstName')
    lastName = formData.get('lastName')
    phoneNumber = formData.get('phoneNumber')
    password1 = formData.get('password1')
    password2 = formData.get('password2')
    landmark = formData.get('landmark')
    town = formData.get('town')
    district = formData.get('district')
    pincode = formData.get('pincode')
    phoneOTP = formData.get('phoneOTP')
    GSTIN = formData.get('GSTIN') # Can be empty
    if not (firstName and
        lastName and
        phoneNumber and
        password1 and
        password2 and
        landmark and
        town and
        phoneOTP and
        district and
        pincode):
        raise ValueError("Some required values are not present")
    if len(firstName) >= 30 or hasNumbers(firstName) or len(lastName) >= 30 or hasNumbers(lastName):
        raise ValueError("Name is invalid")

    validate_international_phonenumber(phoneNumber)

    phoneNumberObj = PhoneNumber(phoneNumber)
    if phoneNumberObj.country_code != 91:
        raise ValueError('Phone number is not Indian')

    verifyOTP(phoneNumberObj, phoneOTP)

    if password1 != password2:
        raise ValueError('Passwords does not match')

    if district not in [value[0] for value in Address.DISTRICT_OPTIONS]:
        raise ValueError('Invalid district')

    if len(pincode) != 6 or not pincode.isdigit():
        raise ValueError('Pincode is invalid')

    if GSTIN:
        if not isValidGST(GSTIN):
            raise ValueError('Invaid GST')

    return {
        'first_name': firstName,
        'last_name': lastName,
        'phone': phoneNumber,
        'password': password1,
        'landmark': landmark,
        'town': town,
        'district': district,
        'pincode': pincode,
        'GSTIN': GSTIN
    }

# Create your views here.
def login(request):
    if request.method == 'POST':
        phone = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        user = auth.authenticate(phone=phone, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
            
        else:
            messages.warning(request, 'Incorrect Credentials Provided')
            return HttpResponseRedirect(reverse('login'))

    elif request.method == 'GET':
        return render(request, 'userprofiles/login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))

def signup(request):
    if request.method == 'GET':
        return render(request, 'userprofiles/signup.html', {
            'districts': Address.DISTRICT_OPTIONS
        })
    elif request.method == 'POST':
        try:
            formData = validateFormData(request.POST)
        except ValueError as e:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('signup'))
        else:
            # If execution reaches this point, the form is valid. data can be access using the formData variable
            try:
                user = User.objects.create_user(**formData)
            except IntegrityError:
                messages.error(request, 'A user with this phone number already exists.')
                return HttpResponseRedirect(reverse('signup'))
            else:
                return HttpResponseRedirect(reverse('login'))


def sentOTP(request):
    if request.method == "POST":
        try:
            number = json.loads(request.body).get('phoneNumber')
            number = PhoneNumber(number)
            client = Client(account_sid, auth_token)
            verification = client.verify \
            .services(service_id) \
            .verifications \
            .create(to=str(number), channel="sms")
        except:
            return HttpResponse(json.dumps({
                'status': 'ERROR'
            }))
        else: 
            return HttpResponse(json.dumps({
                'status': verification.status
            }))

