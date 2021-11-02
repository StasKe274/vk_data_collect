import json
from api_functions import*
import time
import os

def main():

    start_time = time.time()


    if os.path.exists('data/results'):
        print('Директория существует\n')
    else:
        os.makedirs('data/results')


    key_word = input('Введите ключевое слово поиска: ')
    count = input('Сколько групп надо собрать?\n>>> ')
    

    main_groups_list = search_groups(key_word, count)


    with open(f'data/{key_word}_groups.json', 'w', encoding='utf-8') as file:
        json.dump(main_groups_list, file, ensure_ascii=False, indent=4)


    print(main_groups_list)


    for group in main_groups_list:


        members = get_members_id(group)


        fin_list = []
        count = 0 
        for user in members:
            if count > 500: # Сейчас стоит ограничение, чтобы не перегружать комп, выдаются данные 500 пользователей
                break
            user_data = get_user_info(user) 
            if user_data != 0:
                fin_list.append(user_data)
            print(user_data)
            count += 1


        with open(f'data/results/{group}.json', 'w', encoding='utf-8') as file:
            json.dump(fin_list, file, ensure_ascii=False, indent=4)

        
    finish_time = time.time() - start_time


    print(f'\nЗатрачено времени: {finish_time} секунд')


if __name__ == '__main__':
    main()