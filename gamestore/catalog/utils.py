menu = [
    {'title': "Каталог игр", 'url_name': 'catalog'},
    #{'title': 'Добавить игру', 'url_name': 'add_game'},
    {'title': 'Отзывы', 'url_name': 'feedback'}
    # {'title': "Лидеры продаж", 'url_name': 'top_sellers'},
    # {'title': "Скидки", 'url_name': 'discounts'},
    #{'title': "Контакты", 'url_name': 'contacts'},
    # {'title': "Корзина", 'url_name': 'shopping_cart'}
    ]

class DataMixin:
    title_page = None
    extra_context = {}

    paginate_by = 2

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page
        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context
