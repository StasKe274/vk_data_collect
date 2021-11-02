import requests
from time import sleep
from fake_useragent import UserAgent
import random

token = 'токен'

#===========================================================================================================


def get_user_info(user_id):
    """Возвращает подробную информацию о пользователе, поля fields редактируются"""

    ua = UserAgent(verify_ssl=False)
    headers = {'user-agent': ua.random}


    params = {
        'user_ids': user_id,
        'fields': 'id, first_name, last_name, sex, dbith, city, country, deactivated, relation, \
            contacts, about, activities, career, interests, personal, connections',
        'access_token': random.choice(token),
        'v': 5.81
    }


    response = requests.get('https://api.vk.com/method/users.get', params=params, headers=headers)
    sleep(0.15)


    try:
        data = response.json()['response'][0]
        try:
            if data['deactivated'] == 'deleted' or data['deactivated'] == 'banned':
                print('Данный пользователь удален или забанен')
                return 0
        except KeyError:
            return data
    except KeyError:
        print('Данные пользователя не извлечены')
        return 0


#===========================================================================================================


def get_max_offset(group):
    """Возвращает максимальный offset, для сбора информации об id пользователей группы"""

    ua = UserAgent(verify_ssl=False)
    headers = {'user-agent': ua.random}


    params = {
        'group_id': group,
        'sort': 'id_desc',
        'offset': 0,
        'fields': 'last_seen, activity',
        'access_token': random.choice(token),
        'v': 5.81
    }
    response = requests.get('https://api.vk.com/method/groups.getMembers', params=params, headers=headers)


    try:
        data = response.json()['response']['count']
        print(data)
    except KeyError:
        return 0


    return data // 1000


#===========================================================================================================


def get_members_id(group):
    """Возвращает кортеж с id всех пользователей группы"""
    
    ua = UserAgent(verify_ssl=False)
    headers = {'user-agent': ua.random}


    count = 1000
    offset = 0
    max_offset = get_max_offset(group)


    result = []
    while offset < max_offset:
        params = {
            'group_id': group,
            'count': count,
            'fields': '',
            'offset': offset,
            'access_token': token,
            'v': 5.81
        }
        response = requests.get('https://api.vk.com/method/groups.getMembers', params=params, headers=headers)


        try:
            data = response.json()['response']['items']
            for user_id in data:
                result.append(user_id)
            sleep(0.15)
            offset += 1
        except KeyError:
            print('Данные не извлечены')


    return tuple(result)


#===========================================================================================================


def get_group_info(groun_name):
    """Возвращает информацию о группе"""

    ua = UserAgent(verify_ssl=False)
    headers = {'user-agent': ua.random}


    params = {
        'group_id': groun_name,
        'fields': 'activity',
        'access_token': random.choice(token),
        'v': 5.81
    }
    response = requests.get('https://api.vk.com/method/groups.getById', params=params, headers=headers)


    try:
        data = response.json()['response'][0]['activity']
    except KeyError:
        return 'Даннные не извлечены'


    return data


#===========================================================================================================


def search_groups(key_word, count):
    """Возвращает список со словарями групп, подходящих под введенную категорию"""

    ua = UserAgent(verify_ssl=False)
    headers = {'user-agent': ua.random}


    params = {
        'q': key_word,
        'count': count,
        'access_token': random.choice(token),
        'v': 5.81
    }
    response = requests.get('https://api.vk.com/method/groups.search', params=params, headers=headers)


    main_groups_dict = {}
    try:
        data = response.json()['response']['items']


        for group in range(len(data)):
            if data[group]['is_closed'] == 1:
                continue
            else:
                id = data[group]['id']
                name = data[group]['name']
                screen_name = data[group]['screen_name']
                activity = get_group_info(data[group]['id'])
                main_groups_dict[id] = [name, screen_name, activity, key_word]
        
        
        return main_groups_dict


    except KeyError:
        print('Данные о сообществе не извлечены')
        return 0


#===========================================================================================================


def get_users_subscriptions(user_id):
    """Возвращает информацию о подписках пользователя"""

    ua = UserAgent(verify_ssl=False)
    headers = {'user-agent': ua.random}


    params = {
        'user_id': user_id,
        'access_token': random.choice(token),
        'v': 5.81
    }
    response = requests.get('https://api.vk.com/method/groups.get', params=params, headers=headers)
    

    data = response.json()['response']['items']
    groups_activity = {}
    for group_id in data:
        try:
            group_type = get_group_info(group_id)
            if group_type not in groups_activity:
                groups_activity[group_type] = 1
            else:
                groups_activity[group_type] += 1
        except KeyError:
            continue


    result = []
    max_value = 0
    for key, value in groups_activity.items():
        if key == 'Открытая группа' or key == 'Даннные не извлечены':
            continue
        else:
            if max_value < value:
                max_value = value
                max_key = key
                res_dict = {max_key: max_value}
                result.insert(0, res_dict)
            else:
                continue


    return result
        

#===========================================================================================================
