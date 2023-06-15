import requests
from bs4 import BeautifulSoup as bs
import json
import re

def process_ingrefient(s):
    s = s.split(',')[0]
    s = s.split('–')[0]
    if s[-1] == ' ':
        s = s[:-1]
    return s
if __name__ == '__main__':
    save_path = '../datasets/dataset_russian_food.json'
    base_link = 'https://www.russianfood.com/'
    page_link = 'https://www.russianfood.com/recipes/bytype/?fid=23&page='
    suff = '#rcp_list'
    data = {'coctails': []}
    for i in range(1, 8):
        print(i)
        addr = page_link + str(i) + suff
        with requests.get(addr) as link:
            page = bs(link.text, "html.parser")
            cocktails = page.find_all('div', class_='recipe_l')
            for num, cocktail in enumerate(cocktails):
                cocktail = bs(str(cocktail), "html.parser")
                cocktail_link = cocktail.find_all('a')[0]['href']
                with requests.get(base_link + cocktail_link) as cocktail_page:
                    cocktail_page = bs(cocktail_page.text, 'html.parser')
                    recipe = cocktail_page.find_all('div', id='how')
                    prods = cocktail_page.find_all('table', class_='ingr')[0]
                    ingredients = bs(str(prods), 'html.parser').find_all('td')[1:]
                    name = cocktail_page.find_all('h1', class_='title')[0].text.lower()
                    ingredients = list(map(lambda x: process_ingrefient(x.text.lower()[:-1]), ingredients))
                    recipe = list(map(lambda x: x.text.lower(), recipe))
                    data['coctails'].append({'name': name, 'recipe': recipe, 'tags': [], 'ingredients': ingredients})
                    if num % 10 == 0:
                        print(data['coctails'][-1])
    with open(save_path, 'w') as f:
        json.dump(data, f)