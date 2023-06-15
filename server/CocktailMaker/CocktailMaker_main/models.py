from django.db import models


class Cocktail_recipe(models.Model):
    title = models.CharField('Название', max_length=50)
    recipe = models.TextField('Рецепт')
    proportions = models.TextField('Пропорции', blank="true")
    string_ings = models.TextField('Ингредиенты')
    string_tags = models.TextField('Пожелания')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/my-recipes'

    class Meta:
        verbose_name = 'Коктейль'
        verbose_name_plural = 'Коктейли'
