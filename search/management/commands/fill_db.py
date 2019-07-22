import requests
import re
import os

from django.core.management.base import BaseCommand, CommandError
from search.models import Product


class Command(BaseCommand):  

    # get id and name from categories to populate products table
    
    def handle(self, *args, **options):

        CATEGORIES_ARRAY = ['petit-dejeuners', 'plats-prepares', 'snacks-sales', 'biscuits-et-gateaux', 'snacks-sucres', 'produits-laitiers', 'epicerie', 'desserts', 'charcuteries', 'cereales-et-derives', 'produits-a-la-viande']

        for index, value in enumerate(CATEGORIES_ARRAY):

            temp_var = "var" + str(index)

            temp_var = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=labels&tag_contains_0=contains&tag_0=sans%20gluten&tagtype_1=categories&tag_contains_1=contains&tag_1={}&sort_by=unique_scans_n&page_size=100&axis_x=energy&axis_y=products_n&action=display&json=1".format(value)).json()
        
            for x, i in enumerate(temp_var['products']):

                try:
                    single_brand = re.findall("^([^,]*)", str(i['brands']))
                except KeyError:
                    single_brand = "none"

                
                try:
                    x = Product(product_name=i['product_name_fr'].casefold(), brands=str(single_brand), description=i['generic_name_fr'].casefold(), product_url=i['url'] ,product_code=i['code'], product_image=i['image_front_url'] , nutriscore=i['nutrition_grades'], stores=i['stores_tags'], quantity=i['quantity'], nova_groups=i['nova_groups'], categories=i['categories'], fat_100g=i['nutriments']['fat_100g'], saturated_fat_100g=i['nutriments']['saturated-fat_100g'], sugars_100g=i['nutriments']['sugars_100g'], salt_100g=i['nutriments']['salt_100g']) 
                    x.save()
                    self.stdout.write(str(x.id))
                except KeyError as e:
                    print(e)
                    self.stdout.write(str(e))
