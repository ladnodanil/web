from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Category, Game, TagGame, UploadFiles
from catalog.form import AddGameForm, UploadFileForm
import uuid
# Create your views here.
menu = [
    {'title': "Каталог игр", 'url_name': 'catalog'},
    {'title': 'Добавить игру', 'url_name': 'add_game'},
    # {'title': "Лидеры продаж", 'url_name': 'top_sellers'},
    # {'title': "Скидки", 'url_name': 'discounts'},
    {'title': "Контакты", 'url_name': 'contacts'},
    {'title': "Корзина", 'url_name': 'shopping_cart'}
]


data = {
    'title': 'Каталог',
    'menu': menu,
    'catalog': Game.objects.all()
}


def add_game(request):
    if request.method == 'POST':
        form = AddGameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = AddGameForm()
    return render(request, 'gamestore/add_game.html',
                  {'menu': menu, 'title': 'Добавление десерта', 'form': form})


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'catalog': Game.stock.all(),
        'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'gamestore/index.html', context=data)


def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    game = Game.stock.filter(category_id=category.pk)
    data = {
        'title': f'Игры из категории: {category.name}',
        'menu': menu,
        'catalog': game,
        'cat_selected': category.pk,
    }
    return render(request, 'gamestore/catalog.html', context=data)


def catalog(request):
    return render(request, 'gamestore/catalog.html', context=data)


def top_sellers(request):
    return render(request, 'gamestore/top_sellers.html', {'title': 'Лидеры продаж', 'menu': menu})


def discounts(request):
    return render(request, 'gamestore/discounts.html', {'title': 'Скидки', 'menu': menu})


def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)





def contacts(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'gamestore/contacts.html', {'title': 'Контакты', 'menu': menu, 'form': form})


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


def show_tag_gamelist(request, tag_slug):
    tag = get_object_or_404(TagGame, slug=tag_slug)
    games = tag.tags.filter(in_stock=Game.Status.IN_STOCK)
    data = {
        'title': f'Тег: {tag.name}',
        'menu': menu,
        'catalog': games,
        'cat_selected': None,

    }
    return render(request, 'gamestore/catalog.html', context=data)
