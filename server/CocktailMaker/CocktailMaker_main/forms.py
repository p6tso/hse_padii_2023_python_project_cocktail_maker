from .models import Cocktail_recipe
from django.forms import ModelForm, TextInput, Textarea


class Cocktail_recipe_form(ModelForm):
    class Meta:
        model = Cocktail_recipe
        fields = ["title", "string_ings", "string_tags"]
        widgets = {"title": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введи название'
        }), "string_ings": Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введи ингредиенты'
        }), "string_tags": Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введи пожелания'
        })}


class Cocktail_recipe_form1(ModelForm):
    class Meta:
        model = Cocktail_recipe
        fields = ["title"]
        widgets = {"title": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введи название'
        })}
