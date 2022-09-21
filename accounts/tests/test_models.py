from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelUserTests(TestCase):
    def setUp(self):
        self.email = "kim@salistech.com"
        self.first_name = "kim"
        self.last_name = "kim"
        self.password = "asj4hg@bvg123"
        self.gender = "male"
        self.phone = "09098765434"
        self.user = User.objects.create_user(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            gender=self.gender,
            phone=self.phone,
        )

    def test_user_model(self):
        """Test user instance is an object User"""
        user = self.user
        self.assertTrue(isinstance(user, User))

    def test_create_user_with_email(self):
        """Test creating new user with email not username"""

        self.assertEqual(self.user.email, self.email)

    def test_create_user(self):
        """Test creating new user was successfull. """

        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.last_name, self.last_name)
        self.assertEqual(self.user.gender, self.gender)
        self.assertEqual(self.user.phone, self.phone)
        self.assertTrue(self.user.check_password(self.password))

    def test_new_user_email_normalize(self):
        """Test new user email is normalize"""

        email = "john@SALISTECH.COM"
        user = User.objects.create_user(
            email=email, password="pass123", first_name="John", last_name="doe",
            gender="male", phone="09080987657"
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_no_email(self):
        """Test create new user with no email raises error"""

        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None, password="pass123", first_name="John", last_name="doe",
                gender="male", phone="09080987657"
            )

    def test_create_newsupersuer(self):
        """Test creating new superuser"""

        super_user = User.objects.create_superuser(
            email="super@email.com", password="admn123"
        )
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
