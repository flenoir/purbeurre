from django.test import TestCase
from django.urls import reverse
from .models import Product

# Create your tests here.

class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('search:index'))
        self.assertEquals(response.status_code, 200)


class DetailPageTestCase(TestCase):
    def test_detail_page(self):
        product = Product.objects.create(product_name="test_product", nutriscore="a")
        product_id = Product.objects.get(product_name="test_product").id 
        response = self.client.get(reverse('search:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 200)