from django.urls import path, register_converter
from catalog import views, converters
register_converter(converters.GameSlugConverter, 'game')

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog', views.CatalogView.as_view(), name='catalog'),
    path('add-game/', views.AddGame.as_view(), name='add_game'),
    path('category/<slug:category_slug>/', views.CategoryViem.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.TagViem.as_view(), name='tag'),
    path('game/<slug:game_slug>/', views.ShowGame.as_view(), name='game_detail'),

    path('edit/<int:pk>/', views.UpdateGame.as_view(), name='edit_game'),

    path('delete/<int:pk>/', views.DeleteGame.as_view(), name='delete_game'),


    path('top-sellers/', views.top_sellers, name='top_sellers'),
    path('discounts/', views.discounts, name='discounts'),
    path('contacts/', views.contacts, name='contacts'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
]
