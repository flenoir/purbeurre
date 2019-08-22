# Generated by Django 2.2.3 on 2019-07-04 09:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('brands', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('product_url', models.CharField(max_length=150, null=True)),
                ('product_code', models.CharField(max_length=20, null=True)),
                ('product_image', models.CharField(max_length=100, null=True)),
                ('nutriscore', models.CharField(max_length=1, null=True)),
                ('stores', models.CharField(max_length=150, null=True)),
                ('quantity', models.CharField(max_length=40, null=True)),
                ('nova_groups', models.CharField(max_length=5, null=True)),
                ('categories', models.CharField(max_length=500, null=True)),
                ('substitutes', models.ManyToManyField(related_name='_product_substitutes_+', to='search.Product')),
                ('user_product', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
