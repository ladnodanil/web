
from django import template
import catalog.views as views
from django.db.models import Count
from catalog.models import TagGame, Category
 
register = template.Library()
@register.simple_tag()
def get_categories():
    return views


@register.inclusion_tag('gamestore/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.annotate(
        total=Count("game")).filter(total__gt=0)
    return {"categories": cats, "cat_selected": cat_selected_id}

@register.inclusion_tag('gamestore/list_tags.html')
def show_all_tags():
    return {"tags": TagGame.objects.annotate(total=Count("tags"))
            .filter(total__gt=0)}
