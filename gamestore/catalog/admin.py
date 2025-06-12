from django.contrib import admin, messages
from .models import Game, Category, GameDetails, Comment, Like, Feedback, TagGame
from django.utils.safestring import mark_safe


class DeveloperFilter(admin.SimpleListFilter):
    title = 'Разработчик'
    parameter_name = 'developer'

    def lookups(self, request, model_admin):
        developers = GameDetails.objects.values_list(
            'developer', flat=True).distinct()
        return [(dev, dev) for dev in developers if dev]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(details__developer=self.value())
        return queryset


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'price', 'image', 'has_image',
              'slug', 'category', 'tags')
    filter_horizontal = ['tags']
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'has_image', 'price', 'category',
                    'count_tags', 'in_stock')
    list_display_links = ('id', )
    ordering = ['in_stock', 'title']
    list_editable = ('title', 'price', 'category', 'in_stock')
    list_per_page = 3
    actions = ['set_in_stock', 'set_out_of_stock']
    search_fields = ['title__startswith', 'category__name']
    list_filter = [DeveloperFilter, 'category__name', 'in_stock']
    readonly_fields = ['has_image']

    @admin.display(description='Количество тэгов')
    def count_tags(self, game: Game):
        return game.tags.count()

    @admin.display(description='Изображение')
    def has_image(self, game: Game):
        if game.image:
            return mark_safe(f"<img src='{game.image.url}' width=50>")
        return "Без фото"

    @admin.action(description="Отметить выбранные игры как 'В наличии'")
    def set_in_stock(self, request, queryset):
        count = queryset.update(in_stock=Game.Status.IN_STOCK)
        self.message_user(request, f'Изменено {count} записи(ей)')

    @admin.action(description="Отметить выбранные игры как 'Нет в наличии'")
    def set_out_of_stock(self, request, queryset):
        count = queryset.update(in_stock=Game.Status.OUT_OF_STOCK)
        self.message_user(
            request, f'Изменено {count} записи(ей)', messages.WARNING)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'user', 'text')
    list_display_links = ('id', 'game', 'user', 'text')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'user')
    list_display_links = ('id', 'game', 'user')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(GameDetails)
class GameDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'game')
    list_display_links = ('id', 'game')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'text', 'created_at')
    list_display_links = ('id', 'user')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'text')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(TagGame)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
    ordering = ('name',)
