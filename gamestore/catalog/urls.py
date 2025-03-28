from django.urls import path, register_converter
from catalog import views, converters
register_converter(converters.GameSlugConverter, 'game')

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog',views.catalog,name='catalog'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('top-sellers/', views.top_sellers, name='top_sellers'),
    path('discounts/', views.discounts, name='discounts'),
    path('contacts/', views.contacts, name='contacts'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
    path('category/<int:cat_id>/', views.show_category,name='category'),
]
