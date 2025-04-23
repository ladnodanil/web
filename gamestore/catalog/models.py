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
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class GameDetails(models.Model):
    game = models.OneToOneField('Game', on_delete=models.CASCADE, related_name='details')
    release_date = models.DateField()
    developer = models.CharField(max_length=255)
    
    def __str__(self):
        return self.game.title


class Game(models.Model):
    class Status(models.IntegerChoices):
        IN_STOCK = 1, 'В наличии'
        OUT_OF_STOCK = 0, 'Нет в наличии'
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    in_stock = models.BooleanField(
        choices=Status.choices, default=Status.IN_STOCK)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(TagGame, blank=True, related_name='tags')

    objects = models.Manager()
    stock = InStockModel()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'game_slug': self.slug})
