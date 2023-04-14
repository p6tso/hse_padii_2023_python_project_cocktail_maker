import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd

if __name__ == '__main__':
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
        t = requests.get(base_link + i['href'])
        if r.status_code != 200:
            continue
        temp = bs(t.text, "html.parser")
        tm = temp.find_all('a', class_='js-tracking-ingredient')
        tm2 = temp.find_all('td', class_='amount')
        tm3 = temp.find_all('td', class_='unit')
        l1 = []
        l2 = []
        l3 = []
        for j in range(len(tm)):
            l1.append(tm[j].text.lower()[:-1])
            l2.append(tm2[j].text)
            l3.append(tm3[j].text.lower())
        data['coctails'].append({'name' : i.text.lower(), 'ingredients': l1, 'amount' : l2, 'units': l3})
    json_string = json.dumps(data)
    with open('json_data.json', 'w') as outfile:
        outfile.write(json_string)