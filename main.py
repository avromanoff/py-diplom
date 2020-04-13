from pprint import pprint
import requests
import time
import json

APP_ID = 7376843
BASE_URL = 'https://oauth.vk.com/authorize'
auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'response_type': 'token',
    'scope': 'status',
    'v': '5.95',
    'redirect_uri': 'https://example.com/'
}

TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


params = {
    'access_token': TOKEN,
    'v': '5.103'
}


class User:
    def __init__(self, token, user_id=None, first_name=None, last_name=None):
        self.token = token
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.95'
        )

    def get_friends(self):
        """
        инфа о друзьях main-пользователя - счетчик и список ID по возрастанию
        :return:
        """
        params = self.get_params()
        params['user_id'] = main_user_id
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params
        )
        self.friend_counter = response.json()['response']['count']  # кол-во друзей у пользователя
        self.friend_list = response.json()['response']['items']  # список друзей у main-пользователя
        print(f'Всего друзей: {self.friend_counter}')
        return response.json()

    def get_main_groups(self):
        """
        Инфа о группах main-пользователя
        :return:
        """
        params = self.get_params()
        params['user_id'] = main_user_id
        params['count'] = 1000
        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params
        )
        self.group_counter = response.json()['response']['count']  # кол-во групп у main-пользователя
        self.group_list = response.json()['response']['items']  # список групп main-пользователя
        print(f'В скольких группах состоит: {self.group_counter}')
        time.sleep(0.3)
        return response.json()

    def groups_is_member(self,group):
        """
        Проверка - друзья пользователя в указанной группе?
        :return:
        """
        params = self.get_params()
        params['group_id'] = group
        params['user_ids'] = list_to_string()
        response = requests.get(
            'https://api.vk.com/method/groups.isMember',
            params
        )

        print('-')
        time.sleep(0.4)
        return response.json()

    def groups_get_by_id(self, group):
        """
        инфо про группы (название)

        :return:
        """
        params = self.get_params()
        params['group_id'] = group
        params['fields'] = 'name'
        response = requests.get(
            'https://api.vk.com/method/groups.getById',
            params
        )
        print('-')
        time.sleep(0.4)
        return response.json()

    def groups_get_members(self, group):
        """
        метод возвращает список участников сообщества - отсюда берем их количество
        :return:
        """
        params = self.get_params()
        params['group_id'] = group
        response = requests.get(
            'https://api.vk.com/method/groups.getMembers',
            params
        )
        print('-')
        time.sleep(0.4)
        return response.json()


def get_group_list():
    # про вхождение в группу
    groups = list()
    for group in username.group_list:
        group_counter = 0
        group_return = username.groups_is_member(group)['response']
        for items in group_return:
            if items.get('member') == 1:
                group_counter += 1
                break
        if group_counter == 0:
            gid = group
            name = username.groups_get_by_id(group)['response'][0]['name']
            members_count = username.groups_get_members(group)['response']['count']
            group_info = {'name': name, 'gid': gid, 'members_count': members_count}
            groups.append(group_info)
    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(groups, f, ensure_ascii=False)
    print('Результат в файле groups.json')
    return


def list_to_string():
    """
    Делаем из списка строку
    :return:
    """
    user_friend_string = ''
    for f in username.friend_list:
        f = str(f)
        user_friend_string = user_friend_string + f + ','
    return user_friend_string


username = User(TOKEN)
main_username = 'eshmargunov'
main_user_id = 171691064


# друзья пользователя
username.get_friends()
# группы пользователя
username.get_main_groups()
get_group_list()
