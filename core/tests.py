from django.test import TestCase
from django.urls import reverse
from core.models import CustomUser


# Create your tests here.


class SignupPageTestCase(TestCase):

    # test that get on signup page returns 200
    def test_Signup_page(self):
        response = self.client.get(reverse("core:signup"))
        self.assertEquals(response.status_code, 200)

    #  s'enregistrer et verifier que l'utilisateur est bien enregistré

class LoginPageTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="toto@gmail.com", username="toto")
        self.user.set_password("12345")
        self.user.save()

    # test that get on login page returns 200
    def test_Login_page(self):
        response = self.client.get(reverse("account_login"))
        self.assertEquals(response.status_code, 200)

    # test that existing user is logged in returns 200
    def test_Existing_User_Can_Login(self):
        response = self.client.post(
            reverse("account_login"),
            kwargs={"email": "toto@gmail.com", "password": "12345"},
        )
        self.assertEquals(response.status_code, 200)

    # test user has been created
    def test_User_Has_Been_Created(self):
        dbrequest = CustomUser.objects.all().count()
        self.assertEquals(dbrequest, 1)


class logoutPageTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="toto@gmail.com", username="toto")
        self.user.set_password("12345")
        self.user.save()

    # test that get on logout page returns to index
    def test_Logout_page(self):
        self.client.login(email="toto@gmail.com", password="12345")
        response = self.client.post(reverse("account_logout"))
        self.assertEquals(response.url, "/")
