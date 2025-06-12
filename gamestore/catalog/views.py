from django.contrib import messages
from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from catalog.models import Category, Feedback, Game, Like, TagGame, UploadFiles, Comment
from catalog.utils import DataMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import uuid

from catalog.form import CommentForm
# Create your views here.
menu = [
    {'title': "Каталог игр", 'url_name': 'catalog'},

]


class AddComment(LoginRequiredMixin, View):
    def post(self, request, game_slug):
        game = get_object_or_404(Game.stock, slug=game_slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.game = game
            comment.user = request.user
            comment.save()
        return redirect('game_detail', game_slug=game_slug)


class AddGame(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    permission_required = 'catalog.add_game'
    model = Game
    template_name = 'gamestore/add_game.html'
    success_url = reverse_lazy('catalog')
    fields = '__all__'
    title_page = 'Добавление игры'


class UpdateGame(PermissionRequiredMixin, DataMixin, UpdateView):
    permission_required = 'catalog.change_game'
    model = Game
    fields = ['title', 'description', 'image', 'price', 'slug', 'in_stock',
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


class CategoryViem(DataMixin, ListView):
    template_name = 'gamestore/catalog.html'
    context_object_name = 'catalog'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['catalog'][0].category
        return self.get_mixin_context(context,
                                      title=f'Игры из категории: {category.name}',
                                      cat_selected=category.id)

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


@login_required
def contacts(request):
    contact_list = Game.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gamestore/contacts.html', {'title': 'Контакты', 'menu': menu, 'page_obj': page_obj})


def shopping_cart(request):
    return render(request, 'gamestore/shopping_cart.html', {'title': 'Корзина', 'menu': menu})


@login_required
def like_game(request, game_slug):
    game = get_object_or_404(Game.stock, slug=game_slug)
    like, created = Like.objects.get_or_create(user=request.user, game=game)

    if not created:
        like.delete()

    return redirect('game_detail', game_slug=game_slug)


class ShowGame(DataMixin, DetailView):
    model = Game
    template_name = 'gamestore/game.html'
    slug_url_kwarg = 'game_slug'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        if self.request.user.is_authenticated:
            context['user_liked'] = self.object.likes.filter(
                user=self.request.user).exists()
        context['likes_count'] = self.object.likes.count()
        return self.get_mixin_context(context, title=context['game'])


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


class FeedbackView(DataMixin, View):
    template_name = 'gamestore/feedback.html'

    def get(self, request):
        feedbacks = Feedback.objects.all().select_related('user')
        context = self.get_mixin_context({
            'title': 'Отзывы',
            'feedbacks': feedbacks,
        })
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')

        if text and rating:
            Feedback.objects.create(
                user=request.user,
                text=text,
                rating=int(rating)
            )
            messages.success(request, 'Спасибо за ваш отзыв!')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')

        return redirect('feedback')


class DeleteComment(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        # Check if the user is the author of the comment
        if comment.user == request.user:
            game_slug = comment.game.slug
            comment.delete()
            return redirect('game_detail', game_slug=game_slug)
        return HttpResponseNotFound()


class EditComment(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        # Check if the user is the author of the comment
        if comment.user == request.user:
            text = request.POST.get('text')
            if text:
                comment.text = text
                comment.save()
                return JsonResponse({'status': 'success', 'text': comment.text})
        return JsonResponse({'status': 'error'}, status=400)


class DeleteFeedback(LoginRequiredMixin, View):
    def post(self, request, feedback_id):
        feedback = get_object_or_404(Feedback, id=feedback_id)
        # Check if the user is the author of the feedback
        if feedback.user == request.user:
            feedback.delete()
            return redirect('feedback')
        return HttpResponseNotFound()


class EditFeedback(LoginRequiredMixin, View):
    def post(self, request, feedback_id):
        feedback = get_object_or_404(Feedback, id=feedback_id)
        # Check if the user is the author of the feedback
        if feedback.user == request.user:
            text = request.POST.get('text')
            rating = request.POST.get('rating')
            if text and rating:
                feedback.text = text
                feedback.rating = rating
                feedback.save()
                return JsonResponse({
                    'status': 'success',
                    'text': feedback.text,
                    'rating': feedback.rating
                })
        return JsonResponse({'status': 'error'}, status=400)
