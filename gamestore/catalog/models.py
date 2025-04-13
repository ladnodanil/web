from django.db import models
from django.urls import reverse

class InStockModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_stock=Game.Status.IN_STOCK)
    
class Game(models.Model):
    class Status(models.IntegerChoices):
        IN_STOCK = 1, 'В наличии'
        OUT_OF_STOCK = 0, 'Нет в наличии'
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    in_stock = models.BooleanField(choices=Status.choices, default=Status.IN_STOCK)

    objects = models.Manager()
    stock = InStockModel()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'game_slug': self.slug})



