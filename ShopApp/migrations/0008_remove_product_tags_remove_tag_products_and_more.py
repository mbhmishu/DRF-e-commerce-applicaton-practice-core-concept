# Generated by Django 4.1.7 on 2023-04-04 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0007_tag_alter_product_options_remove_product_old_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='products',
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='productimg',
            name='mainimage',
            field=models.ImageField(upload_to='Imgs'),
        ),
    ]
