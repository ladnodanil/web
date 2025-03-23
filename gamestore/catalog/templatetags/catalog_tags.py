from django import template
import catalog.views as views
 
register = template.Library()
@register.simple_tag()
def get_categories():
    return views.cats_dv


@register.inclusion_tag('gamestore/list_categories.html')
def show_categories(cat_selected=0):
    cats = views.cats_dv
    return {"cats": cats, "cat_selected": cat_selected}
