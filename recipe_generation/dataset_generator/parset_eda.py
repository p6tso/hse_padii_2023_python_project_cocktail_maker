import requests
from bs4 import BeautifulSoup as bs
import json
import re

def processed_recipe(s):
    s = re.sub(r'\xa0', ' ', s)
    return s

if __name__ == '__main__':
    save_path = '../datasets/dataset_eda_ru.json'
    base_link = 'https://eda.ru'
    page_link = 'https://eda.ru/recepty/koktejli-alkogoljnije?page='
    data = {'coctails': []}
    for i in range(1, 21):
        addr = page_link + str(i)
        with requests.get(addr) as link:
            page = bs(link.text, "html.parser")
            cocktails = page.find_all('a', class_='emotion-18hxz5k')
            for num, cocktail in enumerate(cocktails):
                with requests.get(base_link + cocktail['href']) as cocktail_page:
                    cocktail_page = bs(cocktail_page.text, 'html.parser')
                    recipe = cocktail_page.find_all('span', itemprop='text')
                    ingredients = cocktail_page.find_all('span', itemprop='recipeIngredient')
                    ingredients = list(map(lambda x: x.text.lower(), ingredients))
                    recipe = list(map(lambda x: processed_recipe(x.text.lower()), recipe))
                    data['coctails'].append({'name': '', 'recipe': recipe, 'tags': [], 'ingredients': ingredients})
                    if num % 10 == 0:
                        print(data['coctails'][-1])
    with open(save_path, 'w') as f:
        json.dump(data, f)