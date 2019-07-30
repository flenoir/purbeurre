from django.test import TestCase
from search.models import Product


class TestModels(TestCase):
    # Setup variable
    def setUp(self):
        self.product1 = Product.objects.create(
            product_name="test product 1", product_code="12345656789", nutriscore="a"
        )
        self.product2 = Product.objects.create(
            product_name="test product 2", product_code="5678901234", nutriscore="d"
        )

    # test product name is capitalized
    def test_Product_is_capitalized(self):
        self.assertEquals(self.product1.__str__(), "Test product 1")

    # test product is created
    def test_Product_is_created(self):
        self.assertEquals(Product.objects.all().count(), 2)

