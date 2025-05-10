from django.contrib import admin, messages
from .models import Game, Category, GameDetails

class DeveloperFilter(admin.SimpleListFilter):
    title = 'Разработчик'  # Название фильтра
    parameter_name = 'developer'  # Параметр для фильтрации в URL

    def lookups(self, request, model_admin):
        developers = GameDetails.objects.values_list('developer', flat=True).distinct()
        return [(dev, dev) for dev in developers if dev]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(details__developer=self.value())
        return queryset
    
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    fields = ('title','price','slug', 'category', 'tags')
    filter_horizontal = ['tags']
    prepopulated_fields = {"slug":("title",)}
    list_display = ('id', 'title', 'price', 'category',
                    'count_tags', 'in_stock', 'has_image')
    list_display_links = ('id', )
    ordering = ['in_stock', 'title']
    list_editable = ('title', 'price', 'category', 'in_stock')
    list_per_page = 3
    actions = ['set_in_stock', 'set_out_of_stock']
    search_fields = ['title__startswith', 'category__name']
    list_filter = [DeveloperFilter, 'category__name', 'in_stock']

    @admin.display(description='Количество тэгов')
    def count_tags(self, game: Game):
        return game.tags.count()

    @admin.display(description='Изображение', boolean=True)
    def has_image(self, game: Game):
        return bool(game.image)
    @admin.action(description="Отметить выбранные игры как 'В наличии'")
    def set_in_stock(self, request, queryset):
        count = queryset.update(in_stock=Game.Status.IN_STOCK)
        self.message_user(request, f'Изменено {count} записи(ей)')
    @admin.action(description="Отметить выбранные игры как 'Нет в наличии'")
    def set_out_of_stock(self, request, queryset):
        count = queryset.update(in_stock=Game.Status.OUT_OF_STOCK)
        self.message_user(request, f'Изменено {count} записи(ей)', messages.WARNING)
    



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

@admin.register(GameDetails)
class GameDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'game')
    list_display_links = ('id', 'game')
