from api_functions import *
import json

key_word = input('Введите ключевое слово поиска: ')
number_of_groups = int(input('Сколько групп нужно проанализировать?\n>>>> '))


groups = search_groups(key_word, number_of_groups)
with open(f'data/groups_{key_word}.json', 'w', encoding='utf-8') as file:
    json.dump(groups, file, ensure_ascii=False, indent=3)


fin_groups_dict = {}
for group in groups:
    if group['is_closed'] == 1:
        continue
    else:
        fin_groups_dict[group['id']] = group['name']
        print(group['name'])
with open(f'data/groups_{key_word}_fin.json', 'w', encoding='utf-8') as file:
    json.dump(fin_groups_dict, file, ensure_ascii=False, indent=3)


for key, value in fin_groups_dict.items():
    try:
        mean_dict = {value: get_members(int(key))}
    except KeyError:
        continue
    with open(f'data/results/{value}_users.json', 'w', encoding='utf-8') as file:
        json.dump(mean_dict, file, ensure_ascii=False, indent=3)


# Банки-Бум | Банки финансы деньги заработок