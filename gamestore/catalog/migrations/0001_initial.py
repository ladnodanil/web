# Generated by Django 5.2.1 on 2025-05-31 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='TagGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UploadFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads_model')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Изображение')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Слаг')),
                ('in_stock', models.BooleanField(choices=[(True, 'В наличии'), (False, 'Нет в наличии')], default=1, verbose_name='Статус')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.category', verbose_name='Категория')),
                ('tags', models.ManyToManyField(blank=True, related_name='tags', to='catalog.taggame', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Игра',
                'verbose_name_plural': 'Игры',
            },
        ),
        migrations.CreateModel(
            name='GameDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_date', models.DateField(verbose_name='Дата релиза')),
                ('developer', models.CharField(max_length=255, verbose_name='Разработчик')),
                ('game', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='catalog.game', verbose_name='Игра')),
            ],
            options={
                'verbose_name': 'Игровые детали',
                'verbose_name_plural': 'Игровые детали',
            },
        ),
    ]
