# Generated by Django 4.1.7 on 2023-04-05 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0011_alter_product_discount_amount_alter_product_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imgconnector',
            old_name='image',
            new_name='img',
        ),
    ]
