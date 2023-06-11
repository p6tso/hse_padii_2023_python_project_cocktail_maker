import requests
from bs4 import BeautifulSoup as bs
import json

if __name__ == '__main__':
    save_path = '../datasets/dataset_final.json'
    base_link = 'https://ru.inshaker.com'
    page_link = 'https://ru.inshaker.com/cocktails?random_page='
    data = {'coctails': []}
    r = requests.get(page_link + '50')
    soup = bs(r.text, "html.parser")
    vacancies_names = soup.find_all('a', class_='cocktail-item-preview')
    print(len(vacancies_names))
    c = 0
    for i in vacancies_names:
        if c % 10 == 0:
            print(c)
        c += 1
        try:
            t = requests.get(base_link + i['href'])
        except requests.exceptions.ConnectionError:
            continue
        if r.status_code != 200:
            continue
        temp = bs(t.text, "html.parser")
        tm3 = temp.find_all('a', class_='js-tracking-ingredient')
        tm4 = temp.find_all('td', class_='amount')
        tm5 = temp.find_all('td', class_='unit')
        tm = temp.find_all('ul', class_='steps')
        tm2 = temp.find_all('a', class_='tag')
        tm = bs(str(tm[0]), "html.parser").find_all('li')
        l1 = list(map(lambda x: x.text, tm))
        l2 = list(map(lambda x: x.text, tm2))
        l3 = list(map(lambda x: x.text.lower()[:-1], tm3))
        l4 = list(map(lambda x: x.text, tm4))
        l5 = list(map(lambda x: x.text.lower(), tm5))
        data['coctails'].append({'name': i.text.lower(), 'recipe': l1, 'tags': l2, 'ingredients': l3,
                                 'amount': l4[:len(l3)], 'units': l5[:len(l3)]})
    json_string = json.dumps(data)
    with open(save_path, 'w') as outfile:
        outfile.write(json_string)
