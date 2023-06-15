import requests
import time
from bs4 import BeautifulSoup as bs
import json

if __name__ == '__main__':
    save_path = '../datasets/am_links.json'
    base_link = 'https://amwine.ru/cocktails/'
    page_link = 'https://amwine.ru/cocktails/?PAGEN_1='
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        # 'keep_alive': False,
        'Connection': 'close'
    })
    links = []
    for page in range(1, 16):
        with requests.get(page_link + str(page), headers=headers) as link:
            content = bs(link.content)
            cocktails = content.find_all('a', class_='head')
            for i in cocktails:
                links.append(i['href'])
            link.close()
            print(page)
            time.sleep(3)
    with open(save_path, 'w') as f:
        json.dump(links, f)