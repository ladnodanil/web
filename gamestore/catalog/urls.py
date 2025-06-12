from django.urls import path, register_converter
from catalog import views, converters
from django.conf.urls import handler404
register_converter(converters.GameSlugConverter, 'game')

urlpatterns = [
    path('', views.CatalogView.as_view(), name='index'),
    path('catalog', views.CatalogView.as_view(), name='catalog'),
    path('add-game/', views.AddGame.as_view(), name='add_game'),
    path('category/<slug:category_slug>/',
         views.CategoryViem.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.TagViem.as_view(), name='tag'),
    path('game/<slug:game_slug>/', views.ShowGame.as_view(), name='game_detail'),

    path('edit/<int:pk>/', views.UpdateGame.as_view(), name='edit_game'),

    path('delete/<int:pk>/', views.DeleteGame.as_view(), name='delete_game'),

    path('game/<slug:game_slug>/add-comment/',
         views.AddComment.as_view(), name='add_comment'),
    path('delete-comment/<int:comment_id>/',
         views.DeleteComment.as_view(), name='delete_comment'),
    path('edit-comment/<int:comment_id>/',
         views.EditComment.as_view(), name='edit_comment'),
    path('like-game/<slug:game_slug>/', views.like_game, name='like_game'),
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('delete-feedback/<int:feedback_id>/',
         views.DeleteFeedback.as_view(), name='delete_feedback'),
    path('edit-feedback/<int:feedback_id>/',
         views.EditFeedback.as_view(), name='edit_feedback'),
    path('top-sellers/', views.top_sellers, name='top_sellers'),
    path('discounts/', views.discounts, name='discounts'),
    path('contacts/', views.contacts, name='contacts'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
]
