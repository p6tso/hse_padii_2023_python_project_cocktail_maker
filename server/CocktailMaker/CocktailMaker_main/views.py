from django.shortcuts import render, redirect
from .models import Cocktail_recipe
from .forms import Cocktail_recipe_form, Cocktail_recipe_form1
from django.views.generic import UpdateView, DetailView
from django.urls import reverse
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
model_path = '/home/outcast/PycharmProjects/project/hse_padii_2023_python_project_cocktail_maker/server/CocktailMaker/CocktailMaker_main/model3'
tokenizer_path = '/home/outcast/PycharmProjects/project/hse_padii_2023_python_project_cocktail_maker/server/CocktailMaker/CocktailMaker_main/tokenizer'
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
bart_model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to("cuda:0")

def get_predict(recipe, tags):
    data = 'ингредиенты: ' + recipe.lower() + ' пожелания: ' + tags.lower()
    print(data)
    inputs = tokenizer(data, padding="max_length", truncation=True, max_length=50, return_tensors="pt")
    input_ids = inputs.input_ids.to("cuda:0")
    attention_mask = inputs.attention_mask.to("cuda:0")
    outputs = bart_model.generate(input_ids, attention_mask=attention_mask)
    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return output_str[0]

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
            print(form['title'].value())
            pole = Cocktail_recipe.objects.create(title = str(form['title'].value()),
                                                  string_tags = str(form['string_tags'].value()),
                                                  string_ings= str(form['string_ings'].value()),
                                                  recipe=get_predict(str(form['string_ings'].value()), str(form['string_tags'].value())))
            redirect('/')
        else:
            error = 'Ошибка'

    context = {
        'form': Cocktail_recipe_form(),
        'error': error
    }
    return render(request, 'CocktailMaker_main/main-page.html', context)


def recipe_delete(request, pk):
    get_recipe = Cocktail_recipe.objects.get(pk=pk)
    get_recipe.delete()
    return redirect(reverse('my-recipes'))


def my_recipes(request):
    recipes = Cocktail_recipe.objects.all()
    return render(request, 'CocktailMaker_main/my-recipes.html', {'recipes': recipes})


def dictionary(request):
    return render(request, 'CocktailMaker_main/dictionary.html')


def reference(request):
    return render(request, 'CocktailMaker_main/reference.html')


def about_us(request):
    return render(request, 'CocktailMaker_main/about-us.html')
