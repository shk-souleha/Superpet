# Generated by Django 5.1.1 on 2024-10-21 04:27

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_managers_product_product_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('category_slug', autoslug.fields.AutoSlugField(editable=False, populate_from='category_name', unique=True)),
            ],
        ),
    ]