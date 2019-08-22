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
    product_code = models.BigIntegerField(null=False, primary_key=True)
    product_image = models.CharField(max_length=100, null=True)
    nutriscore = models.CharField(max_length=1, null=True)
    stores = models.CharField(max_length=150, null=True)
    quantity = models.CharField(max_length=40, null=True)
    nova_groups = models.CharField(max_length=5, null=True)
    categories = models.CharField(max_length=500, null=True)
    substitutes = models.ManyToManyField("self")
    fat_100g = models.CharField(max_length=20, null=True)
    saturated_fat_100g = models.CharField(max_length=20, null=True)
    sugars_100g = models.CharField(max_length=20, null=True)
    salt_100g = models.CharField(max_length=20, null=True)
    
