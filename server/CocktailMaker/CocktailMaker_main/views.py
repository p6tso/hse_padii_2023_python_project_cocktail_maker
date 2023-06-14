from django.shortcuts import render, redirect
from .models import Cocktail_recipe
from .forms import Cocktail_recipe_form, Cocktail_recipe_form1
from django.views.generic import UpdateView, DeleteView, DetailView


class RecipeDeleteView(DeleteView):
    model = Cocktail_recipe
    success_url = '/my-recipes'
    template_name = 'CocktailMaker_main/recipe-delete.html'


class RecipeUpdateView(UpdateView):
    model = Cocktail_recipe
    template_name = 'CocktailMaker_main/recipe-rename.html'
    form_class = Cocktail_recipe_form1


class RecipeDetailView(DetailView):
    model = Cocktail_recipe
    template_name = 'CocktailMaker_main/recipe-view.html'
    context_object_name = 'recipe'


def main_page(request):
    error = ''
    if request.method == 'POST':
        form = Cocktail_recipe_form(request.POST)
        if form.is_valid():
            form.save()
            redirect('/')
        else:
            error = 'Ошибка'

    context = {
        'form': Cocktail_recipe_form(),
        'error': error
    }
    return render(request, 'CocktailMaker_main/main-page.html', context)


def my_recipes(request):
    recipes = Cocktail_recipe.objects.all()
    return render(request, 'CocktailMaker_main/my-recipes.html', {'recipes': recipes})


def dictionary(request):
    return render(request, 'CocktailMaker_main/dictionary.html')


def reference(request):
    return render(request, 'CocktailMaker_main/reference.html')


def about_us(request):
    return render(request, 'CocktailMaker_main/about-us.html')
