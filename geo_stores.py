import json


import requests
ans = []
sp_adr_store = [
    '37.580184,55.867541', '4.9',
    '37.576861,55.838', '4.8',
    '37.634524,55.824258', '4.6',
    '37.708257,55.785837', '4.7',
    '37.602615,55.765194', '5.0',
    '37.710395,55.903317', '5.0',
    '37.444907,55.827439', '4.5',
    '37.545581,55.863833', '105.0',
    '43.979342,56.285958', '4.8',
    '43.987292,56.308975', '4.7',
]
for i in range(0, len(sp_adr_store), 2):
    # Готовим запрос.
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={sp_adr_store[i]}&format=json"

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
        ans.append([f'{toponym_address}. Оценка: {sp_adr_store[i + 1]}'])
print(ans)
