import pandas as pd
import re


def processed(data):
    ings = set()
    tags = set()
    units = set()
    samples = {'ром', 'водка', 'биттер', 'коньяк', 'текила', 'вермут', 'сыр', 'белое вино', 'мартинез', 'портвейн',
               'виски',
               'бренди', 'бурбон', 'уксус', 'кордиал', 'лед', 'мёд', 'вода', 'содовая', 'джин'}
    base_words = {'ром', 'водка', 'биттер', 'коньяк', 'текила', 'вермут', 'сыр', 'белое вино', 'мартинез', 'портвейн',
                  'виски',
                  'бренди', 'бурбон', 'уксус', 'кордиал', 'лед', 'мёд', 'вода', 'содовая', 'джин', 'вино', 'вишня',
                  'груши',
                  'корица', 'джин', 'молоко', 'мускатный орех', 'сливки'}

    delet = 0
    sht = set()
    data.remove(data[delet])
    for i in range(len(data)):
        data[i]['name'] = data[i]['name'].replace("\xad", "")
        data[i]['name'] = data[i]['name'].replace("\xa0", " ")
        for j in range(len(data[i]['ingredients'])):
            data[i]['ingredients'][j] = data[i]['ingredients'][j].replace("\xad", "")
            data[i]['ingredients'][j] = data[i]['ingredients'][j].replace("\xa0", " ")
            if data[i]['ingredients'][j] == 'ситечко' or data[i]['ingredients'][j] == 'резинка':
                data[i]['ingredients'].remove(data[i]['ingredients'][j])
                continue
        for j in range(len(data[i]['ingredients'])):
            data[i]['ingredients'][j] = data[i]['ingredients'][j].replace("\xad", "")
            data[i]['ingredients'][j] = data[i]['ingredients'][j].replace("\xa0", " ")
            while "  " in data[i]['ingredients'][j]:
                data[i]['ingredients'][j] = data[i]['ingredients'][j].replace("  ", " ")
            if data[i]['ingredients'][j][len(data[i]['ingredients'][j]) - 1] == ' ':
                data[i]['ingredients'][j] = data[i]['ingredients'][j][:-1]
            for sample in samples:
                if data[i]['ingredients'][j].count('домашн') > 0:
                    words = data[i]['ingredients'][j].split(' ')
                    homemade = ""
                    for word in words:
                        if word.count('домашн') > 0:
                            homemade = word
                    data[i]['ingredients'][j] = ""
                    for word in words:
                        if word != homemade:
                            data[i]['ingredients'][j] += word + ' '
                    if data[i]['ingredients'][j][len(data[i]['ingredients'][j]) - 1] == ' ':
                        data[i]['ingredients'][j] = data[i]['ingredients'][j][:-1]

                if data[i]['ingredients'][j].count(sample) > 0:
                    data[i]['ingredients'][j] = sample
            ings.add(data[i]['ingredients'][j])
        for pos in range(len(data[i]['ingredients'])):
            for j in base_words:
                if data[i]['ingredients'][pos].find(j) != -1:
                    data[i]['ingredients'][pos] = j
                    break
        for j in range(len(data[i]['tags'])):
            tags.add(data[i]['tags'][j])
    # data1 - датасет, в котором всё переведено в мл, в нём 750 коктейлей, с ним всё хорошо
    # Все цветы посчитал за 1 грамм, а вообще их в коктейлях не будет. Убрал из ингредиентов ситечко, резинку и т.п.
    return data, ings, tags
