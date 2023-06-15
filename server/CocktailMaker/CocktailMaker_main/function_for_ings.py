from dictionary_all_ings_and_tags import all_ings

ings_in_dataset = all_ings

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
            ing_now =''
    hash_ings = []
    for value in dict_ings.values():
        hash_ings.append(float(value))
    return hash_ings



# print(make_hash_ings('авокадо абсент абрикосовый джем'))
