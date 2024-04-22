import json


import requests
ans = []
sp_adr_kafe = [
    '37.597899,55.783266', '4.9', 'Tokpokki',
    '37.679278,55.767448', '4.8', 'Tokpokki',
    '37.671858,55.736235', '4.7', 'Моремэй',
    '37.642572,55.67889', '5.0', 'Lovely',
    '37.678343,55.776102', '4.7', 'Хондэ',
    '37.624957,55.760135', '105.0', 'Kitsune',
    '37.602148,55.863171', '5.0', 'Chiko(трц FORT)',
    '37.516449,55.681712', '4.9', 'IZAKAYA DANBAM',
]
for i in range(0, len(sp_adr_kafe), 3):
    # Готовим запрос.
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={sp_adr_kafe[i]}&format=json"

    # Выполняем запрос.
    response = requests.get(geocoder_request)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()

        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Полный адрес топонима:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        # Печатаем извлечённые из ответа поля:
        ans.append([f'{sp_adr_kafe[i + 2]}. Адрес:{toponym_address}. Оценка: {sp_adr_kafe[i + 1]}'])
print(ans)