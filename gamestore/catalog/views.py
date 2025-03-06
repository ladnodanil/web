from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    
    return HttpResponse("Страница приложения catalog")

def categories(request,game_id):
    if request.GET:
       print(request.GET)
    if game_id > 100:
       return HttpResponseRedirect('/')
    return HttpResponse(f"<h1>Игры по категориям</h1><p >id:{game_id}</p>")

def categories_by_slug(request, game_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Игры по категориям</h1><p >slug:{game_slug}</p>")

def game_detail(request,name):
   return HttpResponse(f"<h1>Игра {name}</h1>")

def page_not_found(request, exception):
 return HttpResponseNotFound('<h1>Страница не найдена 404</h1>')
