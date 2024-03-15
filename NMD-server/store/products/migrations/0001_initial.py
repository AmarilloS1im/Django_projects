# Generated by Django 4.2 on 2024-03-12 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('name', models.CharField(max_length=12, primary_key=True, serialize=False, unique=True)),
                ('discription', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('article_size', models.CharField(max_length=12, primary_key=True, serialize=False, unique=True)),
                ('size_name', models.CharField(max_length=12)),
                ('qty', models.SmallIntegerField()),
                ('to_article', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='SizeSelected',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True)),
                ('is_selected', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('article', models.CharField(max_length=12, primary_key=True, serialize=False, unique=True)),
                ('model_name', models.CharField(max_length=12)),
                ('model_type', models.CharField(max_length=12)),
                ('img', models.ImageField(upload_to='products_images')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('description', models.TextField(blank=True, null=True)),
                ('gender', models.CharField(max_length=12)),
                ('is_child', models.BooleanField()),
                ('season', models.CharField(max_length=12)),
                ('color', models.CharField(max_length=24)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productcategory')),
                ('sizes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.size')),
            ],
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveSmallIntegerField(default=0)),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True)),
                ('is_favorite', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveSmallIntegerField(default=0)),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.size')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
