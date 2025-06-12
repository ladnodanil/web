from django.db import models
from django.urls import reverse


class TagGame(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
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
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True, verbose_name='Изображение')
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


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at'] 
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='comments', verbose_name='Игра')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments', verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return self.text


class Like(models.Model):
    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'game')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='likes', verbose_name='Пользователь')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='likes', verbose_name='Игра')

    def __str__(self):
        return f'{self.user.username} likes {self.game.title}'


class Feedback(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='feedbacks', verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(verbose_name='Оценка', choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return self.text