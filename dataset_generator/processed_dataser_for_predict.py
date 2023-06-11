import json
import re
import csv
from processed_dataset import processed


def read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


file_name = '../datasets/dataset_final.json'
save_path = '../datasets/dataset_for_predict.csv'

r = read(file_name)
data, ings, tags = processed(r['coctails'])
data_final = [[]]
data_final[0].append('name')
for i in ings:
    data_final[0].append(i)
for i in tags:
    data_final[0].append(i)
data_final[0].append('recipe')

for i in range(len(data)):
    data_final.append([0 for x in range(len(data_final[0]))])
    data_final[i + 1][0] = data[i]['name']
    for j in range(len(data[i]['ingredients'])):
        for k in range(len(data_final[0])):
            if data_final[0][k] == data[i]['ingredients'][j]:
                x = k
                break
        data_final[i + 1][x] = data[i]['amount'][j]
    for j in range(len(data[i]['tags'])):
        for k in range(len(data_final[0])):
            if data_final[0][k] == data[i]['tags'][j]:
                x = k
                break
        data_final[i + 1][x] = 1
    data_final[i + 1][-1] = data[i]['recipe']
#     теперь для каждого коктейля, чего сколько + пропорции вместо мл
with open(save_path, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(data_final)
