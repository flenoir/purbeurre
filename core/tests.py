from django.test import TestCase

# Create your tests here.

class SignupPageTestCase(TestCase):

    # test that get on signup page returns 200
    def test_Signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)

    # # test that post on home page returns 200
    # def test_Signup_post(self):        
    #     response = self.client.post(reverse('signup'), kwargs={'email': 'toto@gmail.com', 'username': 'toto@gmail.com','password': '12345'})
    #     self.assertEquals(response.status_code, 200)

class LoginPageTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="toto@gmail.com", username="toto")
        self.user.set_password('12345')
        self.user.save()

    # test that get on login page returns 200
    def test_Login_page(self):
        response = self.client.get(reverse('account_login'))
        self.assertEquals(response.status_code, 200)

    # test that existing user is logged in returns 200
    def test_Existing_User_Can_Login(self):
        response = self.client.post(reverse('account_login'), kwargs={'email': 'toto@gmail.com', 'password': '12345'})
        self.assertEquals(response.status_code, 200)