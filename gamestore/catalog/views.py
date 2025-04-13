from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Game
# Create your views here.
menu = [
    {'title': "Каталог игр", 'url_name': 'catalog'},
    {'title': "Лидеры продаж", 'url_name': 'top_sellers'},
    {'title': "Скидки", 'url_name': 'discounts'},
    {'title': "Контакты", 'url_name': 'contacts'},
    {'title': "Корзина", 'url_name': 'shopping_cart'}
]


data = {
    'title': 'Каталог',
    'menu': menu,
    'catalog': Game.stock.all()
}
cats_dv = [
    {'id': 1, 'name': 'Открытый мир'},
    {'id': 2, 'name': 'Ролевая игра в жанре «экшн»'},
    {'id': 3, 'name': 'Вестерн'},
]


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'catalog': Game.stock.all(),
        'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'gamestore/index.html', context=data)


def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'catalog': Game.stock.all(),
        'cat_selected': cat_id,
    }
    return render(request, 'gamestore/index.html', context=data)


def catalog(request):
    return render(request, 'gamestore/catalog.html', context=data)


def top_sellers(request):
    return render(request, 'gamestore/top_sellers.html', {'title': 'Лидеры продаж', 'menu': menu})


def discounts(request):
    return render(request, 'gamestore/discounts.html', {'title': 'Скидки', 'menu': menu})


def contacts(request):
    return render(request, 'gamestore/contacts.html', {'title': 'Контакты', 'menu': menu})


def shopping_cart(request):
    return render(request, 'gamestore/shopping_cart.html', {'title': 'Корзина', 'menu': menu})


def game_detail(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)

    context = {
        'title': game.title,
        'menu': menu,
        'game': game
    }
    return render(request, 'gamestore/game.html', context)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена 404</h1>')
