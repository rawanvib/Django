# Generated by Django 3.2 on 2021-05-04 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_categories',
            field=models.ManyToManyField(to='myapp.Categories'),
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
    ]
