import json
import requests
from tqdm import tqdm
VK_TOKEN = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'
ya_token = 'AQAAAAAOdaVYAADLW7HyelRxwk3qkqNx3ta8F8k'


def get_foto_vk_to_yadisk():
    # ya_token = input('Введите токен пользователя ЯДиска: ')
    vk_id = input('Введите id пользователя Вконтакте: ')
    params_vk_id = {'user_ids': vk_id, 'access_token': VK_TOKEN, 'v': '5.131'}
    res = requests.get('https://api.vk.com/method/users.get', params=params_vk_id)
    print()
    if 'error' in res.json():
        return print(f'Возникла ошибка при работе с API ВКонтакте. Код ошибки: {res.json()["error"]["error_code"]}')
    vk_id = res.json()['response'][0]['id']
    if 'deactivated' in res.json()['response'][0]:
        return print('Профиль удален.')
    names = []
    urls = []
    info = []
    url_api_vk = 'https://api.vk.com/method/photos.get'
    params_vk = {'access_token': VK_TOKEN, 'v': '5.131', 'owner_id': vk_id, 'album_id': 'profile',
                 'extended': '1', 'photo_sizes': '1'}
    result = requests.get(url_api_vk, params=params_vk).json()
    if 'error' in result:
        return print(f'Возникла ошибка при работе с API ВКонтакте. Код ошибки: {result["error"]["error_code"]}')
    for item in result['response']['items']:
        urls.append(item['sizes'][-1]['url'])
        if str(item['likes']['count']) in names:
            names.append(str(item['likes']['count']) + ' ' + str(item['date']))
        else:
            names.append(str(item['likes']['count']))
        info.append({'name': names[-1], 'size': item['sizes'][-1]['type']})
    with open('info.json', 'w') as inf:
        json.dump(info, inf, ensure_ascii=False, indent=2)
    headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {ya_token}'}
    params_newfolder = {'path': '/Photo_VK'}
    url_newfolder = 'https://cloud-api.yandex.net:443/v1/disk/resources/'
    url_upload = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload/'
    response_newfolder = requests.put(url_newfolder, params=params_newfolder, headers=headers)
    if 'error' in response_newfolder.json():
        if response_newfolder.json()['error'] == 'DiskPathPointsToExistentDirectoryError':
            print('Папка "Photo_VK" уже существует, все фотографии будут загружены в нее.')
            print()
        else:
            return print(f'Возникла ошибка при работе с API Яндекс.Диск. Код ошибки: {response_newfolder}')
    for i in tqdm(range(len(names)), desc='Upload photo', unit=' poto'):
        params_upload = {'path': f'/Photo_VK/{names[i]}.jpg', 'url': urls[i]}
        response = requests.post(url_upload, params=params_upload, headers=headers)
        if 'error' in response.json():
            return print(f'Возникла ошибка при работе с API Яндекс.Диск. Код ошибки: {response_newfolder}')
    print()
    print(f'Фотографии в количестве {len(names)}шт. загружены на ЯДиск')


get_foto_vk_to_yadisk()
