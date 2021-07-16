from django.test import TestCase
from django.contrib.auth import get_user_model
from phonenumber_field.validators import ValidationError
# Create your tests here.

class UserAccountTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            '+919856347610', 'John', 'Doe', 'shibu123'
        )
        self.assertEqual(super_user.phone, '+919856347610')
        self.assertEqual(super_user.first_name, 'John')
        self.assertEqual(super_user.last_name, 'Doe')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), 'John - +919856347610')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            phone='+919856347610', first_name='John', last_name='Doe', password='nginxisokay', is_staff=False
        )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            phone='', first_name='John', last_name='Doe', password='nginxisokay', is_staff=False
        )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            phone='', first_name='John', last_name='Doe', password='nginxisokay', is_superuser=False
        )

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            '+919856347610', 'John', 'Doe', 'nginxisokay',gstin= '32AAEFA0584F1ZY', landmark='sahara', town='senpai', district='Cochin', pincode='643271'
        )
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.gstin, '32AAEFA0584F1ZY')
        self.assertEqual(user.phone, '+919856347610')
        self.assertEqual(str(user.address), 'senpai, Cochin, 643271')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                phone='', first_name='a', last_name='b', password='password'
            )

        with self.assertRaises(ValueError):
            db.objects.create_user(
                phone='+919856347610', first_name='John', last_name='Doe', password='nginxisokay'
            )

        with self.assertRaises(ValidationError):
            db.objects.create_user(
                phone='ithenth_phone_number', first_name='John', last_name='Doe', password='nginxisokay', landmark='sahara'
            )


        with self.assertRaises(ValueError):
            user = db.objects.create_user(
                '+19856347610', 'John', 'Doe', 'nginxisokay',gstin= '32AAEFA0584F1ZY', landmark='sahara', town='kalpetta', district='Wayanad', pincode='643271'
        )