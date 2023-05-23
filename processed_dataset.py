import json
import string
import re
import csv


def read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


ings = set()
tags = set()
units = set()
samples = {'ром', 'водка', 'биттер', 'коньяк', 'текила', 'вермут', 'сыр', 'белое вино', 'мартинез', 'портвейн', 'виски',
           'бренди', 'бурбон', 'уксус', 'кордиал', 'лед', 'мёд', 'вода', 'содовая', 'джин'}
r = read('dataset_final.json')
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
        if data[i]['ingredients'][j] == 'ситечко' or data[i]['ingredients'][j] == 'резинка':
            data[i]['ingredients'].remove(data[i]['ingredients'][j])
            data[i]['amount'].remove(data[i]['amount'][j])
            data[i]['units'].remove(data[i]['units'][j])
            continue
        if data[i]['ingredients'][j] == 'орхидея':
            data[i]['units'][j] = 'мл'
            data[i]['amount'][j] = str(50 * int(data[i]['amount'][j]))
        if data[i]['ingredients'][j] == 'орео':
            data[i]['units'][j] = 'мл'
            data[i]['amount'][j] = str(9.5 * int(data[i]['amount'][j]))
        if data[i]['ingredients'][j] == 'маршмэллоу':
            data[i]['units'][j] = 'мл'
            data[i]['amount'][j] = str(3.5 * int(data[i]['amount'][j]))
        if data[i]['ingredients'][j] == 'карамельный попкорн':
            data[i]['units'][j] = 'мл'
            data[i]['amount'][j] = str(0.7 * int(data[i]['amount'][j]))
        if data[i]['ingredients'][j] == 'цветы фиалки' or data[i]['ingredients'][j] == 'цветы фиалки' or \
                data[i]['ingredients'][j] == 'сухие цветки для чая' or data[i]['ingredients'][j] == 'цветы яблони' or \
                data[i]['ingredients'][j] == 'лепестки роз' or data[i]['ingredients'][
            j] == 'ростки гороха с приправами' or data[i]['ingredients'][j] == 'цветы ромашки' or \
                data[i]['ingredients'][j] == 'хризантема' or data[i]['ingredients'][j] == 'пшеничный колос' or \
                data[i]['ingredients'][j] == 'цветок карнивора' or data[i]['ingredients'][j] == 'сычуаньский бутон':
            data[i]['units'][j] = 'мл'
        if data[i]['ingredients'][j] == 'изюм' or data[i]['ingredients'][j] == 'леденцы':
            data[i]['units'][j] = 'мл'
            data[i]['amount'][j] = str(2.5 * int(data[i]['amount'][j]))
        if data[i]['ingredients'][j] == 'апельсиновая цедра' or data[i]['ingredients'][j] == 'лимонная цедра' or \
                data[i]['ingredients'][j] == 'лаймовая цедра' or data[i]['ingredients'][j] == 'грейпфрутовая цедра':
            data[i]['units'][j] = 'мл'
            data[i]['amount'][j] = str(20 * int(data[i]['amount'][j]))
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
    for j in range(len(data[i]['tags'])):
        tags.add(data[i]['tags'][j])
    # тут пропорции делаем из мл, можно и мл оставить, просто удалить следующие 5 строк
    sum_amount = 0
    for j in range(len(data[i]['amount'])):
        sum_amount += float(data[i]['amount'][j])
    for j in range(len(data[i]['amount'])):
        data[i]['amount'][j] = float(data[i]['amount'][j]) / float(sum_amount)

# print('\n\n')
# print('Изначальный обработаный датасет, с шт и мл')
for i in range(len(data)):
    print(data[i])
# print(len(data))

data1 = []
flag = 0
for i in range(len(data)):
    for j in range(len(data[i]['units'])):
        if data[i]['units'][j] == 'шт':
            flag = 1
    if flag == 0:
        data1.append(data[i])
    else:
        flag = 0

# data1 - датасет, в котором всё переведено в мл, в нём 750 коктейлей, с ним всё хорошо

# print('\n\n')
# print('Обработаный датасет, только мл')
# for i in range(len(data1)):
#     print(data1[i])
# print(len(data1))

# Все цветы посчитал за 1 грамм, а вообще их в коктейлях не будет. Убрал из ингредиентов ситечко, резинку и т.п.
# TODO обработать оставшиеся шт, но как будто не имеет смысла

# print('\nИнгредиенты с шт:')
# print(len(ings))
# print(ings)
# print('\nСами шт:')
# print(len(sht))
# print(sht)

data_final = [[]]

# print(len(tags))
# print(tags)

data_final[0].append('name')
for i in ings:
    data_final[0].append(i)
for i in tags:
    data_final[0].append(i)
data_final[0].append('recipe')

for i in range(len(data1)):
    data_final.append([0 for x in range(len(data_final[0]))])
    data_final[i + 1][0] = data1[i]['name']
    for j in range(len(data1[i]['ingredients'])):
        for k in range(len(data_final[0])):
            if data_final[0][k] == data1[i]['ingredients'][j]:
                x = k
                break
        data_final[i + 1][x] = data1[i]['amount'][j]
    for j in range(len(data1[i]['tags'])):
        for k in range(len(data_final[0])):
            if data_final[0][k] == data1[i]['tags'][j]:
                x = k
                break
        data_final[i + 1][x] = 1
    data_final[i + 1][-1] = data1[i]['recipe']
#     теперь для каждого коктейля, чего сколько + пропорции вместо мл

# print(data_final)
with open('data.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(data_final)
