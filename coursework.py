import json
from tqdm import tqdm
import requests
# Необходимо задать ВК токен
# Файл info.json хранит информацию последнего запуска с тестовым id: 'begemot_korovin'


class VK:
    vk_token = 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd'

    def __init__(self):
        self.vk_id = input('Введите id пользователя Вконтакте: ')

    def get_id_number(self):
        url_get_id = 'https://api.vk.com/method/users.get'
        params_vk_id = {'user_ids': self.vk_id, 'access_token': self.vk_token, 'v': '5.131'}
        result = requests.get(url_get_id, params=params_vk_id)
        print()
        if 'error' in result.json():
            return print(f'Возникла ошибка при работе с API ВКонтакте. '
                         f'Код ошибки: {result.json()["error"]["error_code"]}')
        if 'deactivated' in result.json()['response'][0]:
            return print('Профиль удален.')
        return result.json()['response'][0]['id']

    def get_url_upload(self):
        vk_id = self.get_id_number()
        url_api_vk = 'https://api.vk.com/method/photos.get'
        params_vk = {'access_token': self.vk_token, 'v': '5.131', 'owner_id': vk_id, 'album_id': 'profile',
                     'extended': '1', 'photo_sizes': '1'}
        names = []
        urls = []
        info = []
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
        return [names, urls, info]


class YaDisk:
    url_newfolder = 'https://cloud-api.yandex.net:443/v1/disk/resources/'
    url_upload = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload/'

    def __init__(self):
        self.token = input('Введите токен пользователя ЯДиска: ')

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def new_folder(self):
        headers = self.get_headers()
        params_new_folder = {'path': '/Photo_VK'}
        response_new_folder = requests.put(self.url_newfolder, params=params_new_folder, headers=headers)
        return response_new_folder

    def upload(self):
        names, urls, info = VK().get_url_upload()
        headers = self.get_headers()
        error_test = self.new_folder().json()
        with open('info.json', 'w') as inf:
            json.dump(info, inf, ensure_ascii=False, indent=2)
        if 'error' in error_test:
            if error_test['error'] == 'DiskPathPointsToExistentDirectoryError':
                print('Папка "Photo_VK" уже существует, все фотографии будут загружены в нее.')
                print()
        for i in tqdm(range(len(names)), desc='Upload photo', unit=' poto'):
            params_upload = {'path': f'/Photo_VK/{names[i]}.jpg', 'url': urls[i]}
            response = requests.post(self.url_upload, params=params_upload, headers=headers)
            if 'error' in response.json():
                return print(f'Возникла ошибка при работе с API Яндекс.Диск. Код ошибки: {response}')
        print()
        print(f'Фотографии в количестве {len(names)}шт. загружены на ЯДиск')


test = YaDisk()
test.upload()
