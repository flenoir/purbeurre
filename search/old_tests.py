from django.test import TestCase
from django.urls import reverse
from .models import Product
from search.views import get_substitutes
from django.shortcuts import get_object_or_404
from core.models import CustomUser

# Create your tests here.


class IndexPageTestCase(TestCase):
    # test that index page returns 200
    def test_index_page(self):
        response = self.client.get(reverse("search:index"))
        self.assertEquals(response.status_code, 200)


class DetailPageTestCase(TestCase):
    # Setup variable
    def setUp(self):
        self.product = Product.objects.create(
            product_name="test_product", nutriscore="a"
        )
        self.product_id = Product.objects.get(product_name="test_product").id

    # test that DetailPage returns 200
    def test_detail_page(self):
        response = self.client.get(reverse("search:detail", args=(self.product_id,)))
        self.assertEqual(response.status_code, 200)


class LegalPageTestCase(TestCase):
    # test that mention legales returns 200
    def test_legal_page(self):
        response = self.client.get(reverse("search:mentions"))
        self.assertEquals(response.status_code, 200)


class SwapPageTestCase(TestCase):
    # Setup variable
    def setUp(self):
        self.product = Product.objects.create(
            product_name="test_product",
            nutriscore="a",
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product_id = Product.objects.get(product_name="test_product").id

    # test that Swap page returns 200
    def test_swap_page(self):
        response = self.client.get(reverse("search:swap", args=(self.product_id,)))
        self.assertEquals(response.status_code, 200)


class ListProductsPageTestCase(TestCase):
    # Setup variable
    def setUp(self):
        self.product = Product.objects.create(
            product_name="test_product",
            nutriscore="a",
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.substitute = Product.objects.create(
            product_name="test_product2",
            nutriscore="a",
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product_id = Product.objects.get(product_name="test_product").id
        self.user = CustomUser.objects.create(email="toto@gmail.com", username="toto")
        self.user.set_password("12345")
        self.user.save()
        self.user.user_substitutes.add(self.product_id)

    # test that list_products returns 200
    def test_listProducts_page(self):
        # log user to comply with @login_required decorator
        self.client.login(email="toto@gmail.com", password="12345")
        response = self.client.get(reverse("search:list_products"))
        self.assertEquals(response.status_code, 200)


# test that list_products is only available to connecter user

