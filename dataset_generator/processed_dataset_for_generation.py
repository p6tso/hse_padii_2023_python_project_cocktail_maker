import json
import re
import csv
from processed_dataset import processed


def read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


file_name = '../datasets/dataset_final.json'
save_path = '../datasets/dataset_for_generation.csv'

r = read(file_name)
data, _, _ = processed(r['coctails'])
data_final = [[]]
data_final[0].append('name')
data_final[0].append('input')
data_final[0].append('label')
for i in range(len(data)):
    data_final.append([0 for x in range(len(data_final[0]))])
    data_final[i + 1][0] = data[i]['name']
    data_final[i + 1][1] = 'ингредиенты: ' + ' '.join(data[i]['ingredients']) + ' пожелания: ' + ' '.join(data[i]['tags'])
    data_final[i + 1][2] = '. '.join(data[i]['recipe'])
with open(save_path, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(data_final)
