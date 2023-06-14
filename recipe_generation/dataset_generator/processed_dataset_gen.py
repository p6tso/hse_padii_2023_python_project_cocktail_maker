import json
import re
import csv
import pandas as pd
from processed_dataset_base_gen import processed


def read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


file_name = '../datasets/dataset_lenta.json'
save_path = '../datasets/dataset_for_generation.csv'
try:
    base_frame = pd.read_csv(save_path)
except:
    base_frame = pd.DataFrame({'name': [], 'input': [], 'label': []})
r = read(file_name)
data, _, _ = processed(r['coctails'])

for i in range(len(data)):
    name = data[i]['name']
    ingredients = 'ингредиенты: ' + ' '.join(data[i]['ingredients']) + ' пожелания: ' + ' '.join(data[i]['tags'])
    recipe = '. '.join(data[i]['recipe'])
    data_final = pd.DataFrame({'name': name, 'input': ingredients, 'label': recipe}, index=[0])
    base_frame = pd.concat([base_frame, data_final])
try:
    base_frame = base_frame.drop(['Unnamed: 0'], axis=1)
except KeyError:
    pass
base_frame.to_csv(save_path, index=False)


