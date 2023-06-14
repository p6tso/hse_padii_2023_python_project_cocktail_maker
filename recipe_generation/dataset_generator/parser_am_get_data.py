import requests
import time
from bs4 import BeautifulSoup as bs
import json

if __name__ == '__main__':
    file_path = '../datasets/am_links.json'
    save_path = '../datasets/am_data.json'
    base_link = 'https://amwine.ru/'
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        # 'keep_alive': False,
        'Connection': 'close'
    })
    data = {'coctails': []}
    file = open(file_path)
    file = json.load(file)
    counter = 0

    for i, name in enumerate(file):
        with requests.get(base_link + str(name), headers=headers) as link:
            if link.status_code != 200:
                counter += 1
                continue
            page = bs(link.text, "html.parser")
            name = page.find_all('h1', itemprop='name')
            name = ' '.join(name[0].text.split()).lower()
            try:
                temp = page.find_all('ol')[0]
            except IndexError:
                counter += 1
                continue
            ingredients = page.find_all('a', class_='about-cocktail__param-title')
            recipe = bs(str(temp), "html.parser").find_all('li')
            ingredients = list(map(lambda x: x.text.lower()[:-1], ingredients))
            recipe = list(map(lambda x: x.text.lower()[1:-1] if x.text.lower()[0] == ' ' else x.text.lower()[:-1], recipe))
            data['coctails'].append({'name': name, 'recipe': recipe, 'tags': [], 'ingredients': ingredients})
            time.sleep(3)
        print('page_num: ', i)
    print(counter)
    with open(save_path, 'w') as f:
        json.dump(data, f)
