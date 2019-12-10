"""writing some test cases"""

from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestLogin(APITestCase):
    """ login test cases"""

    def setUp(self):
        """overriding setup method"""
        self.username = "ravi"
        self.email = "ravi@ravi.com"
        self.password = "admin@123"

        self.user = User.objects.create_user(
            self.username, self.email, self.password
        )
        self.url = reverse("apiblog:loginView")

    def test_login(self):
        """test with correct username and password"""
        data = {
            "username": self.username,
            "password": self.password,
        }
        result = self.client.post(self.url, data=data)
        self.assertEqual(200, result.status_code, "login successful")

    def test_login_empty_username(self):
        """test with empty username and password"""
        data = {
            "username": "",
            "password": self.password,
        }
        result = self.client.post(self.url, data=data)
        self.assertEqual(400, result.status_code, "empty username")

    def test_login_empty_password(self):
        """test with empty password"""
        data = {
            "username": self.username,
            "password": ""
        }
        result = self.client.post(self.url, data=data)
        self.assertEqual(400, result.status_code, "empty password")

    def test_login_invalid_username(self):
        """test with invalid username"""
        data = {
            "username": "fgdfg",
            "password": self.password
        }
        result = self.client.post(self.url, data=data)
        self.assertEqual(400, result.status_code, "invalid username")

    def test_login_invalid_password(self):
        """test with invalid password"""
        data = {
            "username": self.username,
            "password": "fgdfgdfs"
        }
        result = self.client.post(self.url, data=data)
        self.assertEqual(400, result.status_code, "invalid password")


class TestSignup(APITestCase):
    """
     Test cases for user registration
    """

    def setUp(self):
        """overriding setup method"""
        super().setUp()
        self.data = {
            "username": "sss",
            "email": "sss@sss.com",
            "password": "admin@123"
        }

    def test_registration_works(self):
        """
        test case for valid form data
        """
        url = reverse('apiblog:SignupView')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 201, "signup successful")

    def test_registration_empty_name(self):
        """
        test case for name with blank
        """
        self.data["username"] = ""
        url = reverse('apiblog:SignupView')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 400, "empty username")

    def test_registration__name(self):
        """
        test case for name with exceeding limits of character
        """
        name_length = 'k' * 400
        self.data["username"] = name_length
        url = reverse('apiblog:SignupView')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 400, "username length is too long")

    def test_registration_empty_email(self):
        """
        test for user email
        """
        self.data["email"] = ""
        url = reverse('apiblog:SignupView')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 400, "empty email")

    def test_registration_invalid_email(self):
        """
        test for invalid email of user
        """
        self.data["email"] = "kiwitech"
        url = reverse('apiblog:SignupView')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 400, "invalid email")

    def test_registration_empty_pwd(self):
        """
        test case for user password
        """
        self.data["password"] = ""
        url = reverse('apiblog:SignupView')
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 400, "empty password")

    def tearDown(self):
        """
        deleting all users created during test case run.
        :return: None
        """
        User.objects.all().delete()
