import requests
import json
import os
from variables import *
import pandas as pd


def get_car(mark, model, nameplt=""):
    result = []
    count_page = 80
    for a in range(1, count_page + 1):

        #Параметры запроса
        PARAMS = {
            'catalog_filter' : [{"mark": mark, "model": model, "nameplate_name": nameplt}],
            "customs_state_group": "DOESNT_MATTER",
            'section': "all",
            'category': "cars",
            'sort': "fresh_relevance_1-desc",
            "geo_radius": 10000000,
            "geo_id": [213],
            'page': a
            }

        try:response = requests.post(URL, json=PARAMS, headers=HEADERS)
        except: print("!!!!!!!!!!CANT POST!!!!!!!!")

        data = response.json()['offers']

        if (len(data) == 0):
            if (a == 1):
                print("NOT FOUND {}  {} {}".format(mark, model, nameplt))
                with open('no_cars.txt', 'a') as file:
                    result.append(mark)
                    result.append(model)
                    result.append(nameplt)
                    file.write(str(result) + "\n")
                    result = []
            break
        i = 0
        while i <= len(data) - 1:

            #Картинки автомобиля
            img_url = []
            for img in data[i]['state']['image_urls']:
                img_url.append(img['sizes']['1200x900'])
            # print('a')
            #Марка автомобиля
            try: Marka_info = str(data[i]['vehicle_info']['mark_info']['name'])
            except: Marka_info = 'Not marka info'

            #Модель автомобиля
            try: Model_info = str(data[i]['vehicle_info']['model_info']['name'])
            except: Model_info = 'Not model info'

            #Подназвание модели автомобиля
            try: Name_plt = str(data[i]['vehicle_info']['model_info']['nameplate']['name'])
            except: Name_plt = ""

            #Поколение автомобиля
            try: Gen_info = str(data[i]['vehicle_info']['super_gen']['ru_name']).split()[0]
            except: Gen_info = '1'

            # Перебираем ссылки из словаря img_url
            for link_img_0 in img_url:
                link_img = "https:" + str(link_img_0)
                dict_copy = car.copy()
                dict_copy["mark"] = Marka_info
                dict_copy["model"] = Model_info
                dict_copy["nameplt"] = Name_plt
                dict_copy["generation"] = Gen_info
                dict_copy["url"] = link_img
                result.append(dict_copy)
            i += 1
        print('Page: ' + str(a))
    return result


def download_image(path, url):
    with open(path, 'wb+') as handle:
        print("Download from {} to {}".format(url, path))
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

def main():
    df = pd.read_excel('список.xlsx')
    df['Плт'].fillna("", inplace=True)
    print(df)

    for mark, model, name_plt in zip(df['Марка'],df['Модель'],df['Плт']):
        # result = []
        mark, model, name_plt = str(mark).upper(), str(model).upper(), str(name_plt).lower()
        print(mark, model, name_plt)
        result = get_car(mark, model, name_plt)

        if result == []:
            continue

        with open(result_txt, 'w', encoding='UTF-8') as file:
            json.dump(result, file,indent=2)

        with open(result_txt, 'r') as f:
            models = [DromCarModelOffer(t) for t in json.load(f)]

        for k, m in enumerate(models):
            path = BASEPATH + "{}/{}/{}/{}/".format(m.mark, m.model, m.nameplt, m.generation)
            os.makedirs(path, exist_ok=True)
            download_image(path + '{}.jpg'.format(k), m.url)


if __name__ == "__main__":
    main()

