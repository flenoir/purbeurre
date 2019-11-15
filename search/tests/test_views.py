from django.test import TestCase
from django.urls import reverse
from search.models import Product
from search.views import (
    get_substitutes,
    add_substitute,
    remove_substitute,
    list_products,
    compare_products,
)
from django.shortcuts import get_object_or_404
from core.models import CustomUser


class IndexPageTestCase(TestCase):

    # test that post on index page returns 200
    def test_index_page(self):
        response = self.client.post(reverse("search:index"), kwargs={"post": "poulet aux brocolis"})
        self.assertEquals(response.status_code, 200)

    # test that get on index page returns 200
    def test_index_get(self):
        response = self.client.get(
            reverse("search:index"), kwargs={"get": "poulet aux brocolis"}
        )
        self.assertEquals(response.status_code, 200)


class DetailPageTestCase(TestCase):
    # Setup variable
    def setUp(self):
        self.product = Product.objects.create(
            product_name="test_product", nutriscore="a",product_code=7840022838378488, stores="auchan, leclerc, super U"
        )
        # self.product_id = Product.objects.get(product_name="test_product").id

    # test that DetailPage returns 200 None
    def test_detail_page(self):
        response = self.client.get(reverse("search:detail", args=(self.product.product_code,)))
        self.assertEqual(response.status_code, 200)

    # test that DetailPage displays stores
    def test_display_store(self):
        response = self.client.get(reverse("search:detail", args=(self.product.product_code,)))
        # print(response.content)
        self.assertEquals(response.context['stores'][0], 'auchan')



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
            product_code=7840022838378488,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product_id = Product.objects.get(product_name="test_product").product_code

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
            product_code=7840022838378488,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.substitute = Product.objects.create(
            product_name="test_product2",
            nutriscore="a",
            product_code=40022838378488765,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product_id = Product.objects.get(product_name="test_product").product_code
        self.user = CustomUser.objects.create(email="toto@gmail.com", username="toto")
        self.user.set_password("12345")
        self.user.save()
        self.user.user_substitutes.add(self.product_id)

    # test that list_products returns 200
    def test_listProducts_page(self):
        # log user to comply with @login_required decorator
        self.client.login(email="toto@gmail.com", password="12345")
        listprod = list_products(self)
        # response = self.client.get(reverse('search:list_products'))
        self.assertEquals(listprod.status_code, 200)


class WordsFilter_TestCase(TestCase):
    # Setup variable
    def setUp(self):
        self.product1 = Product.objects.create(
            product_name="filet saumon brocolis frites",
            nutriscore="a",
            product_code=378293020882773,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product2 = Product.objects.create(
            product_name="filet saumon navet",
            nutriscore="a",
            product_code=78293020992773,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )

    # test input is splited
    def test_resulting_search(self):
        self.words = self.product1.product_name.split(" ")
        self.assertEquals(self.words, ["filet", "saumon", "brocolis", "frites"])

    # test that words filter returns the filtered products
    def test_words_filtering(self):
        resulting_search = ["filet", "saumon", "frites"]
        result = (
            Product.objects.filter(product_name__contains=resulting_search[0])
            .filter(product_name__contains=resulting_search[1])
            .filter(product_name__contains=resulting_search[2])
        )
        self.assertEquals(result[0], self.product1)


class Compare_Products_TestCase(TestCase):
    # Setup variable
    def setUp(self):
        self.product1 = Product.objects.create(
            product_name="filet saumon brocolis frites",
            nutriscore="a",
            product_code=378293020882773,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product2 = Product.objects.create(
            product_name="filet saumon navet",
            nutriscore="d",
            product_code=3782968900065,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )

    # test compare products
    def test_compare_products(self):
        compared = compare_products(self.product1, self.product2)
        self.assertEquals(compared, (self.product1, 378293020882773))


class Get_Substitutes_TestCase(TestCase):
    # Setup variable
    def setUp(self):
        self.product1 = Product.objects.create(
            product_name="filet saumon brocolis frites",
            nutriscore="a",
            product_code=37829302088999,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.user1 = CustomUser.objects.create(email="toto@gmail.com", password="12345")
        self.user_to_associate = CustomUser.objects.get(email=self.user1.email)
        self.user_to_associate.user_substitutes.add(self.product1.product_code)

    # test substitute list is filled
    def test_get_substitute_exists(self):
        self.client.login(email="toto@gmail.com", password="12345")
        getsubs = get_substitutes(self.user1)
        self.assertEquals(getsubs["full_list"][0], self.product1)

    # test substitute_list returns None when empty
    def test_get_substitute_returns_none(self):
        self.client.login(email="toto@gmail.com", password="12345")
        substitutes_list = CustomUser.objects.filter(
            user_substitutes__isnull=True
        ).filter(email=self.user1.email)
        self.assertFalse(substitutes_list)


class Add_Substitutes_TestCase(TestCase):
    # Setup variable
    def setUp(self):
        self.product1 = Product.objects.create(
            product_name="filet saumon brocolis frites",
            nutriscore="a",
            product_code=378293020882773,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product2 = Product.objects.create(
            product_name="filet saumon navet",
            nutriscore="d",
            product_code=57296820882789,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.user = CustomUser.objects.create(email="toto@gmail.com", password="12345")

    # test add substitute returns 200
    def test_add_substitute_to_user_returns_200(self):
        self.client.login(email="toto@gmail.com", password="12345")
        addsubs = add_substitute(self, self.product2.product_code, self.product1.product_code)
        self.assertEquals(addsubs.status_code, 200)


class Remove_Substitutes_TestCase(TestCase):

    # Setup variable
    def setUp(self):
        self.product1 = Product.objects.create(
            product_name="filet saumon brocolis frites",
            nutriscore="a",
            product_code=378293020882773,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product2 = Product.objects.create(
            product_name="filet saumon navet",
            nutriscore="d",
            product_code=57296820882789,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.user = CustomUser.objects.create(email="toto@gmail.com", password="12345")
        self.user.set_password("12345")
        self.user.save()

    # test remove substitute returns 200
    def test_remove_substitutes_returns_200(self):
        self.client.login(email="toto@gmail.com", password="12345")
        removesubs = self.client.get(reverse("search:remove", args=(self.product2.product_code,)))
        # removesubs = remove_substitute(self, self.product2)
        self.assertEquals(removesubs.status_code, 200)


class PaginationTestCase(TestCase):

        # Setup variable
    def setUp(self):
        self.product1 = Product.objects.create(
            product_name="filet saumon brocolis frites",
            nutriscore="a",
            stores="auchan, leclerc, super U",
            product_code=378293020882771,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product2 = Product.objects.create(
            product_name="filet saumon navet",
            nutriscore="d",
            product_code=57296820882782,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product3 = Product.objects.create(
            product_name="filet saumon haricots",
            nutriscore="a",
            product_code=378293020882773,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product4 = Product.objects.create(
            product_name="filet saumon pmme de terre",
            nutriscore="d",
            product_code=57296820882784,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product5 = Product.objects.create(
            product_name="filet saumon chou",
            nutriscore="a",
            product_code=378293020882775,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product6 = Product.objects.create(
            product_name="filet pulet frites",
            nutriscore="d",
            product_code=57296820882786,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product7 = Product.objects.create(
            product_name="filet poulet tomate",
            nutriscore="a",
            product_code=378293020882777,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product8 = Product.objects.create(
            product_name="filet dinde champignons",
            nutriscore="d",
            product_code=57296820882788,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product9 = Product.objects.create(
            product_name="filet dinde navet",
            nutriscore="a",
            product_code=378293020882779,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product10 = Product.objects.create(
            product_name="filet saumon tomates",
            nutriscore="d",
            product_code=57296820882710,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product11 = Product.objects.create(
            product_name="filet saumon creme",
            nutriscore="a",
            product_code=378293020882711,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product12 = Product.objects.create(
            product_name="filet poulet creme champignons",
            nutriscore="d",
            product_code=57296820882712,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product13 = Product.objects.create(
            product_name="filet poulet miel",
            nutriscore="a",
            product_code=378293020882713,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )
        self.product14 = Product.objects.create(
            product_name="filet poulet pommes",
            nutriscore="d",
            product_code=57296820882714,
            categories="Plats préparés,Produits à la viande,Plats préparés à la viande,Plats au bœuf",
        )

    # test that page are more than one if search retunr more than 12 products
    def test_index_pagination(self):
        response=self.client.get(
            reverse("search:index"), {"post": "filet"}
        )
        # print(response.context['res'])
        self.assertEquals(response.context['res'].next_page_number(), 2)

        
        