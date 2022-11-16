import os
import requests
import json
import urllib.parse

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        file_name = os.path.basename(file_path)

        data_for_upload = self.get_data_for_upload(file_name)
        self.upload_file(data_for_upload, file_path)


    def get_data_for_upload(self, path):
        params = urllib.parse.urlencode({"path": path, "overwrite": True })

        try:
            res = requests.put(
                'https://cloud-api.yandex.net/v1/disk/resources/upload',
                params=params,
                headers={'Authorization': self.token})
        except IOError:
            print('some error')

        return json.loads(res.text)

    def upload_file(self, upload_info, file_path):
        path = os.path.basename(file_path)

        if "href" not in upload_info: raise ValueError('bad request')

        try:
            requests.put(upload_info["href"], data=open(path, 'rb'))
        except IOError:
            print('some error')

if __name__ == '__main__':
    path_to_file = input('Введите путь к файлу: ')
    token = input('Введите токен: ')
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)
