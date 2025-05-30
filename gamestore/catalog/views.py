from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from catalog.models import Category, Game, TagGame, UploadFiles
from catalog.form import AddGameForm, UploadFileForm
from catalog.utils import DataMixin
from django.core.paginator import Paginator
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




class AddGame(DataMixin, CreateView):
    #form_class = AddGameForm
    model = Game
    template_name = 'gamestore/add_game.html'
    success_url = reverse_lazy('catalog')
    fields = '__all__'
    title_page = 'Добавление игры'

class UpdateGame(DataMixin, UpdateView):
    model = Game
    fields = ['title', 'description','image', 'price', 'slug', 'in_stock', 
                  'category', 'tags',]
    template_name = 'gamestore/add_game.html'
    success_url = reverse_lazy('catalog')
    title_page = 'Редактирование игры'


class DeleteGame(DataMixin, DeleteView):
    model = Game
    template_name = 'gamestore/delete_game.html'
    success_url = reverse_lazy('catalog')
    title_page = 'Удаление игры'

class CatalogView(DataMixin, ListView):
    model = Game
    template_name = 'gamestore/catalog.html'
    context_object_name = 'catalog'
    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                       title='Каталог игр',
                                       cat_selected=0,)
    def get_queryset(self):
        return Game.stock.all()
    
class CategoryViem(DataMixin,ListView):
    template_name = 'gamestore/catalog.html'
    context_object_name = 'catalog'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['catalog'][0].category
        return self.get_mixin_context(context,
                                      title=f'Игры из категории: {category.name}',
                                      cat_selected = category.id)
    
    def get_queryset(self):
        return Game.stock.filter(category__slug=self.kwargs['category_slug']).select_related('category')









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
    contact_list = Game.objects.all()
    paginator = Paginator(contact_list, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    return render(request, 'gamestore/contacts.html', {'title': 'Контакты', 'menu':menu,'page_obj':page_obj})


def shopping_cart(request):
    return render(request, 'gamestore/shopping_cart.html', {'title': 'Корзина', 'menu': menu})

class ShowGame(DataMixin, DetailView):
    model = Game
    template_name = 'gamestore/game.html'
    slug_url_kwarg = 'game_slug'
    context_object_name = 'game'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['game'])
    
    

    def get_object(self, queryset=None):
        return get_object_or_404(Game.stock, slug=self.kwargs[self.slug_url_kwarg])


def index():
    pass

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена 404</h1>')


class TagViem(DataMixin, ListView):
    template_name = 'gamestore/catalog.html'
    context_object_name = 'catalog'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagGame, slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=f'Игры по тегу: {tag.name}')
    
    def get_queryset(self):
        return Game.stock.filter(tags__slug=self.kwargs['tag_slug']).select_related('category')

