from django.urls import path, register_converter
from catalog import views, converters
register_converter(converters.GameSlugConverter, 'game')

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/<int:game_id>/', views.categories, name='categories_by_id'),
    path('catalog/<slug:game_slug>/', views.categories_by_slug, name='categories_by_slug'),
    path('game/<game:name>/', views.game_detail, name='game_detail'),
]
