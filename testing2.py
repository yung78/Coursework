import json
import requests
from pprint import pprint

vk_id = input('Введите id пользователя: ')
VK_TOKEN = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
params_vk_id = {'user_ids': vk_id, 'access_token': VK_TOKEN, 'v': '5.131'}
res = requests.get('https://api.vk.com/method/users.get', params=params_vk_id)
print(res.json())

if 'deactivated' in res.json()['response'][0]:
    print('Профиль удален')
