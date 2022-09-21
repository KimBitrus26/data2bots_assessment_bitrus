from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User


def create_user(**params):
    return User.objects.create_user(**params)


class PublicRegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test register user API is successfull"""

        payload = {
            "email": "john@gmail.com",
            "first_name": "john",
            "last_name": "doe",
            "password": "johnpassword123",
            "gender": "male",
            "phone": "09080987657",
        }
        res = self.client.post("/api/v1/auth/registration/", payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertIn("access_token", res.data)
        self.assertEqual(res.data['user']['first_name'], payload['first_name'])
        self.assertEqual(res.data['user']['last_name'], payload['last_name'])
        self.assertEqual(res.data['user']['email'], payload['email'])
        self.assertEqual(res.data['user']['gender'], payload['gender'])

    def test_create_user_already_exist(self):
        """Test email already exists"""

        payload = {
            "email": "john@gmail.com",
            "first_name": "john",
            "last_name": "doe",
            "password": "johnpassword123",
            "gender": "male",
            "phone": "09080987657",
        }
        payload1 = {
            "email": "john@gmail.com",
            "first_name": "john",
            "last_name": "doe",
            "password": "johnpassword123",
            "gender": "male",
            "phone": "09080987657",
        }
        create_user(**payload)
        res = self.client.post("/api/v1/auth/registration/", payload1)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logged_in(self):
        """Test user login is successfull"""

        payload = {
            "email": "john@gmail.com",
            "first_name": "john",
            "last_name": "doe",
            "password": "password@1234"
        }
        create_user(**payload)
        payload1 = {
            "email": payload["email"],
            "password": payload["password"]
        }
        res = self.client.post("/api/v1/auth/login/", payload1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", res.data)
        self.assertEqual(res.data['user']['email'], payload['email'])


class PrivateTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
                                email="john@gmailcom",
                                password="johnpassword123",
                                first_name="John",
                                last_name="Doe",
                                gender="male",
                                phone="09087987876"
                            )
        self.client.force_authenticate(user=self.user)

    def test_update_user(self):
        """Test update user information"""

        payload = {
            "first_name": "David",
            "last_name": "Mary",
            "gender": "female",
        }
        res = self.client.patch(f"/api/v1/update-user/{self.user.id}/", payload)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        user = User.objects.get(pk=self.user.id)
        self.assertEqual(res.data['data']['first_name'], user.first_name)
        self.assertEqual(res.data['data']['last_name'], user.last_name)
        self.assertEqual(res.data['data']['email'], user.email)
        self.assertEqual(res.data['data']['gender'], user.gender)
        self.assertEqual(res.data['status'], "User updated successfully")
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(user, key))
