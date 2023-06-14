from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_page, name='main-page'),
    path("my-recipes", views.my_recipes, name='my-recipes'),
    path("dictionary", views.dictionary, name='dictionary'),
    path("reference", views.reference, name='reference'),
    path("about-us", views.about_us, name='about-us'),
    path('<int:pk>', views.RecipeDetailView.as_view(), name="recipe"),
    path('<int:pk>/update', views.RecipeUpdateView.as_view(), name="recipe-rename"),
    path('recipe-delete/<int:pk>', views.recipe_delete, name="recipe-delete"),
]
