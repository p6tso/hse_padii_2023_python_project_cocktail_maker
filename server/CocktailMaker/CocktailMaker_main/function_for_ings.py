from .dictionary_all_ings_and_tags import all_ings, all_tags

ings_in_dataset = all_ings
tags_in_dataset = all_tags


def make_hash_ings(string_ings):
    dict_ings = dict()
    for ing in ings_in_dataset:
        dict_ings[ing] = 0
    words = str(string_ings).split()
    ing_now = ''
    for word in words:
        if len(ing_now) == 0:
            ing_now = word
        else:
            ing_now = ing_now + ' ' + word
        if ing_now in dict_ings:
            dict_ings[ing_now] = 1
            ing_now = ''
    hash_ings = []
    for value in dict_ings.values():
        hash_ings.append(float(value))
    return hash_ings


def make_hash_tags(string_tags):
    dict_tags = dict()
    for tag in tags_in_dataset:
        dict_tags[tag] = 0
    words = str(string_tags).split()
    tag_now = ''
    for word in words:
        if len(tag_now) == 0:
            tag_now = word
        else:
            tag_now = tag_now + ' ' + word
        if tag_now in dict_tags:
            dict_tags[tag_now] = 1
            tag_now = ''
    hash_tags = []
    for value in dict_tags.values():
        hash_tags.append(float(value))
    return hash_tags

# print(make_hash_ings('авокадо абсент абрикосовый джем'))