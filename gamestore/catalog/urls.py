from django.urls import path, register_converter
from catalog import views, converters
register_converter(converters.GameSlugConverter, 'game')

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog', views.catalog, name='catalog'),
    path('top-sellers/', views.top_sellers, name='top_sellers'),
    path('add-game/', views.add_game, name='add_game'),
    path('discounts/', views.discounts, name='discounts'),
    path('contacts/', views.contacts, name='contacts'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
    path('category/<slug:category_slug>/', views.show_category, name='category'),
    path('game/<slug:game_slug>/', views.game_detail, name='game_detail'),
    path('tag/<slug:tag_slug>', views.show_tag_gamelist, name='tag')
]
