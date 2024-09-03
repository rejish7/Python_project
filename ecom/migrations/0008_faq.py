# Generated by Django 5.1 on 2024-09-03 04:38

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0007_product_category_product_shipping_info_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', ckeditor.fields.RichTextField()),
                ('answer', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'faq',
                'verbose_name_plural': 'faq',
            },
        ),
    ]
