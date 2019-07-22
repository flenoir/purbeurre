from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):

    def __str__(self):
        return self.product_name.capitalize()

    # We specify the model fields
    product_name = models.CharField(max_length=100)
    brands = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)
    product_url = models.CharField(max_length=150, null=True)
    product_code = models.CharField(max_length=20, null=True)
    product_image = models.CharField(max_length=100, null=True)
    nutriscore = models.CharField(max_length=1, null=True)
    stores = models.CharField(max_length=150, null=True)
    quantity = models.CharField(max_length=40, null=True)
    nova_groups = models.CharField(max_length=5, null=True)
    categories = models.CharField(max_length=500, null=True)
    substitutes = models.ManyToManyField("self")
    # user_product = models.ManyToManyField(settings.AUTH_USER_MODEL)

    # @classmethod
    # def associate(cls, current_product_id, substitute_product):
    #     subs_product = cls.objects.get(id=current_product_id)
    #     subs_product.substitutes.add(substitute_product)

    def associate(self, substitute_product):
        self.substitutes.add(substitute_product)
