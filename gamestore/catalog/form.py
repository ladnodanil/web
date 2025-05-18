from django import forms
from .models import Category, Game
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class RussianValidator:
    ALLOWED_CHARS ="АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'
    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."
    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise forms.ValidationError(self.message, code=self.code, params={"value": value})



class AddGameForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="Категория не выбрана",
                                      label='Категория')
    class Meta:
        model = Game
        fields = ['title', 'description','image', 'price', 'slug', 'in_stock', 
                  'category', 'tags',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}), 
            'tags': forms.CheckboxSelectMultiple, }
        
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        return price



class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")


