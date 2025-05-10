from django.db import models
from django.urls import reverse


class TagGame(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class InStockModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_stock=Game.Status.IN_STOCK)


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='Слаг')
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class GameDetails(models.Model):
    class Meta:
        verbose_name = 'Игровые детали'
        verbose_name_plural = 'Игровые детали'
    game = models.OneToOneField('Game', on_delete=models.CASCADE, related_name='details', verbose_name='Игра')
    release_date = models.DateField(verbose_name='Дата релиза')
    developer = models.CharField(max_length=255, verbose_name='Разработчик')
    
    def __str__(self):
        return self.game.title




class Game(models.Model):
    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
    class Status(models.IntegerChoices):
        IN_STOCK = 1, 'В наличии'
        OUT_OF_STOCK = 0, 'Нет в наличии'
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='Слаг')
    in_stock = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.IN_STOCK, verbose_name='Статус')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    tags = models.ManyToManyField(TagGame, blank=True, related_name='tags', verbose_name='Теги')
    objects = models.Manager()
    stock = InStockModel()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'game_slug': self.slug})
