# Generated by Django 2.2.3 on 2019-07-05 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='user_product',
        ),
    ]
