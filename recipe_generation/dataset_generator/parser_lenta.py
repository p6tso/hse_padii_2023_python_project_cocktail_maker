import requests
from bs4 import BeautifulSoup as bs
import json
import re

def processed_recipe(s):
    s = re.sub(r'\r', '', s)
    s = re.sub(r'\n', '', s)
    s = ' '.join(s.split())
    return s

if __name__ == '__main__':
    save_path = '../datasets/dataset_lenta.json'
    base_link = 'https://eda.ru'
    page_link = 'https://lenta.com/recepty/catalog-recepty/f/tip-blyuda=koktejjli/?page='
    data = {'coctails': []}
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        # 'keep_alive': False,
        'Connection': 'close'
    })
    for i in range(1, 19):
        addr = page_link + str(i)
        with requests.get(addr,headers=headers) as link:
            page = bs(link.text, "html.parser")
            cocktails = page.find_all('a', class_='recipe-card')
            for num, cocktail in enumerate(cocktails):
                with requests.get(cocktail['href'], headers=headers) as cocktail_page:
                    cocktail_page = bs(cocktail_page.text, 'html.parser')
                    recipe = cocktail_page.find_all('div', class_='recipe-step__description')
                    ingredients = cocktail_page.find_all('div', class_='recipe-checkbox__label')
                    ingredients = list(map(lambda x: x.text.lower(), ingredients))
                    recipe = list(map(lambda x: processed_recipe(x.text.lower()), recipe))
                    data['coctails'].append({'name': '', 'recipe': recipe, 'tags': [], 'ingredients': ingredients})
                    if num % 10 == 0:
                        print(data['coctails'][-1])
    with open(save_path, 'w') as f:
        json.dump(data, f)