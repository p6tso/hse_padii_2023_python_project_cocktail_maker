import json
import string
import re


def read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


ings = set()
units = set()
samples = {'ром', 'водка', 'биттер', 'коньяк', 'текила', 'вермут', 'сыр', 'белое вино', 'мартинез', 'портвейн', 'виски',
           'бренди', 'бурбон', 'уксус', 'кордиал', 'лед', 'мёд', 'вода', 'содовая', 'джин'}
r = read('dataset.json')
data = r['coctails']
delet = 0
sht = set()
for i in range(len(data)):
    for j in range(len(data[i]['units'])):
        if data[i]['units'][j] == 'кл':
            delet = i
            break

data.remove(data[delet])

for i in range(len(data)):
    data[i]['name'] = data[i]['name'].replace("\xad", "")
    data[i]['name'] = data[i]['name'].replace("\xa0", " ")
    for j in range(len(data[i]['units'])):
        data[i]['ingredients'][j] = data[i]['ingredients'][j].replace("\xad", "")
        data[i]['ingredients'][j] = data[i]['ingredients'][j].replace("\xa0", " ")

        if data[i]['units'][j] == 'шт':
            sht.add(data[i]['ingredients'][j])
        if data[i]['units'][j] == 'г':
            data[i]['units'][j] = 'мл'
        if data[i]['units'][j] == 'кг':
            data[i]['units'][j] = 'мл'
            data[i]['amount'][j] = str(1000 * int(data[i]['amount'][j]))
        if data[i]['units'][j] == 'л':
            data[i]['units'][j] = 'мл'
            data[i]['amount'][j] = str(1000 * int(data[i]['amount'][j]))
        units.add(data[i]['units'][j])

    for j in range(len(data[i]['ingredients'])):
        data[i]['ingredients'][j] = data[i]['ingredients'][j].replace("\xad", "")
        data[i]['ingredients'][j] = data[i]['ingredients'][j].replace("\xa0", " ")
        data[i]['ingredients'][j] = re.sub("[q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|-]", "",
                                           data[i]['ingredients'][j])
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
print('\n\n')
for i in range(len(data)):
    print(data[i])
print('\nИнгредиенты:\n')
print(ings)
print(len(ings))
print(len(data))
print(units)
print(sht)
