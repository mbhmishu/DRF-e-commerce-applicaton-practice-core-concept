# Generated by Django 4.1.7 on 2023-04-07 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0014_color_material_size_remove_product_discount_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='ShopApp.product'),
        ),
    ]
