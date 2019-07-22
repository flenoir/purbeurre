from django.test import TestCase
from search.models import Product


class TestModels(TestCase):

    def setUp(self):
        self.product1 = Product.objects.create(
            product_name="test product",
            product_code="12345656789",
            nutriscore="a"
            )

    def test_Product_is_capitalized(self):
        self.assertEquals(self.product1.__str__(), "Test product")

    def test_Product_is_created(self):
        self.assertEquals(Product.objects.all().count(), 1)