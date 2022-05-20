"""
Integration tests for auth API endpoints.

each test simulates an API call to one endpoint and checks if the response data and status code are correct
these tests test serializers.py and views.py and the API endpoints as a whole
"""
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from osoc.common.tests import AdminFactory
from osoc.common.models import Coach


class RegisterTests(APITestCase):
    """
    test class for testing register functionality
    """
    def setUp(self):
        """
        test setup
        """
        self.admin = AdminFactory()
        self.client.force_authenticate(self.admin)

    def test_register(self):
        """
        test POST /auth/register
        """
        url = reverse("register")
        data = {
            "email": "test.user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "password*&^%",
            "password2": "password*&^%"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_passwords_dont_match(self):
        """
        test POST /auth/register with two different passwords
        """
        url = reverse("register")
        data = {
            "email": "test.user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "password*&^%",
            "password2": "wrong"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_email_exists(self):
        """
        test POST /auth/register with an existing email
        """
        url = reverse("register")
        data = {
            "email": self.admin.email,
            "first_name": "John",
            "last_name": "Doe",
            "password1": "password*&^%",
            "password2": "password*&^%"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    """
    test class for testing login functionality
    """
    def setUp(self):
        """
        test setup
        """
        admin = AdminFactory()
        self.client.force_authenticate(admin)
        # create user with register endpoint so that the password is hashed and can be used to log in
        self.user_data = {
            "email": "test.user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "password*&^%",
            "password2": "password*&^%"
        }
        url = reverse("register")
        self.client.post(url, self.user_data, format="json")
        # set coach active to be able to log in
        coach = Coach.objects.get(email=self.user_data["email"])
        coach.is_active = True
        coach.save()

    def test_login(self):
        """
        test POST /api-auth/login/
        """
        url = reverse("rest_login")
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password1"]
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_doenst_exist(self):
        """
        test POST /api-auth/login/ with a non-existing user
        """
        url = reverse("rest_login")
        data = {
            "email": "non_existing_email",
            "password": "password"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password(self):
        """
        test POST /api-auth/login/ with a wrong password
        """
        url = reverse("rest_login")
        data = {
            "email": self.user_data["email"],
            "password": "wrong_password"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_bad_request(self):
        """
        test POST /api-auth/login/ with data missing
        """
        url = reverse("rest_login")
        data = {
            "email": self.user_data["email"],
            "password": ""
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
