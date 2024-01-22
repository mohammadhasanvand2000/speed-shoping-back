# Generated by Django 4.2.8 on 2024-01-02 10:02

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grouping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.IntegerField(blank=True, default='1000', null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='assets\\img\\poducts')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('grouping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grouping', to='product.grouping', verbose_name='grouping')),
            ],
        ),
        migrations.CreateModel(
            name='Product_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='assets\\img\\poducts')),
                ('producti', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productimage', to='product.product', verbose_name='producti')),
            ],
        ),
        migrations.CreateModel(
            name='Product_color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', colorfield.fields.ColorField(blank=True, default='#FF0000', image_field=None, max_length=25, null=True, samples=None)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('producti', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productcolor', to='product.product', verbose_name='producti')),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discribtion', models.CharField(blank=True, max_length=1000, null=True)),
                ('introduction', models.CharField(blank=True, max_length=2000, null=True)),
                ('Alloy', models.CharField(blank=True, max_length=200, null=True)),
                ('warranty', models.IntegerField(blank=True, null=True)),
                ('made_in', models.CharField(blank=True, max_length=50, null=True)),
                ('dimensions', models.FloatField(blank=True, null=True)),
                ('in_dimensions', models.FloatField(blank=True, null=True)),
                ('Weight', models.IntegerField(blank=True, null=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='productdetail', to='product.product', verbose_name='product')),
            ],
        ),
        migrations.CreateModel(
            name='Client_Coments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coment', models.CharField(blank=True, max_length=10000, null=True)),
                ('img', models.ImageField(blank=True, help_text='plase enter images your product ', null=True, upload_to='')),
                ('product', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cproduct', to='product.product', verbose_name='cproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_from_avalable', models.IntegerField(blank=True, null=True)),
                ('avalable', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productcart', to='product.product', verbose_name='product')),
            ],
        ),
    ]
