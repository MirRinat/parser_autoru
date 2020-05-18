import requests
import json
import os
from variables import *
import pandas as pd


def get_car(mark,model,generation="", nameplate=""):
    result = []
    count_page = 99
    # a = 1
    for a in range(1, count_page+1):

        #Параметры запроса
        PARAMS = {
            'catalog_filter' : [{"mark": mark, "model": model, "nameplate_name": nameplate, "generation": generation}],
            "customs_state_group": "DOESNT_MATTER",
            'section': "all",
            'category': "cars",
            'sort': "fresh_relevance_1-desc",
            "geo_radius": 10000000,
            "geo_id": [213],
            'page': a
            }

        HEADERS = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Length': '137',
            'content-type': 'application/json',
            'Cookie': '_csrf_token=1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24; autoru_sid=a%3Ag5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270%7C1580931467355.604800.8HnYnADZ6dSuzP1gctE0Fw.cd59AHgDSjoJxSYHCHfDUoj-f2orbR5pKj6U0ddu1G4; autoruuid=g5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270; suid=48a075680eac323f3f9ad5304157467a.bc50c5bde34519f174ccdba0bd791787; from_lifetime=1580933172327; from=yandex; X-Vertis-DC=myt; crookie=bp+bI7U7P7sm6q0mpUwAgWZrbzx3jePMKp8OPHqMwu9FdPseXCTs3bUqyAjp1fRRTDJ9Z5RZEdQLKToDLIpc7dWxb90=; cmtchd=MTU4MDkzMTQ3MjU0NQ==; yandexuid=1758388111580931457; bltsr=1; ',
            'Host': 'auto.ru',
            'origin': 'https://auto.ru/cars/all/',
            'Referer': 'https://auto.ru/cars/all/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'x-client-app-version': '202002.03.092255',
            'x-client-date': '1580933207763',
            'x-csrf-token': '1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24',
            'x-page-request-id': '60142cd4f0c0edf51f96fd0134c6f02a',
            'x-requested-with': 'fetch'
        }

        response = requests.post(URL, json=PARAMS, headers=HEADERS)
        # print(response.json()['offers'])
        data = response.json()['offers']

        if (len(data) == 0):
            if (a == 1):
                print("NOT FOUND {}  {}".format(mark, model))
                with open('no_cars_one.txt', 'a') as file:
                    result.append(mark)
                    result.append(model)
                    file.write(str(result) + "\n")
            break
        i = 0
        while i <= len(data) -1:

            #Картинки автомобиля
            img_url = []
            for img in data[i]['state']['image_urls']:
                img_url.append(img['sizes']['1200x900'])

            #Марка автомобиля
            try: Marka_info = str(data[i]['vehicle_info']['mark_info']['name'])
            except: Marka_info = 'Not marka info'

            #Модель автомобиля
            try: Model_info = str(data[i]['vehicle_info']['model_info']['name'])
            except: Model_info = 'Not model info'

            #Поколение автомобиля
            try: Gen_info = str(data[i]['vehicle_info']['super_gen']['ru_name']).split()[0]
            except: Gen_info = ''

            # Перебираем ссылки из словаря img_url, и записываем их в одну переменную текстом
            for link_img_0 in img_url:
                link_img = "https:" + str(link_img_0)
                dict_copy = car.copy()
                dict_copy["mark"] = Marka_info
                dict_copy["model"] = Model_info
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
            print (response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

def main():


    df = pd.read_excel('1 список.xlsx')
    print(df)

    # result = []
    # for i, j in zip(df['Марка'],df['Модель']):
    #     print(str(i).upper(), str(j).upper())
    #
    #     # print(result)
    # result = get_car(str(i).upper(), str(j).upper())
    result = get_car("AUDI", "A3")
    # print(result)
    with open(result_txt, 'w', encoding='UTF-8') as file:
        json.dump(result, file,indent=2)

    with open(result_txt, 'r') as f:
        try: models = [DromCarModelOffer(m) for m in json.load(f)]
        except: exit(1)



    for k, m in enumerate(models):
        path = BASEPATH + "{}/{}/{}/".format(m.mark, m.model, m.generation)
        os.makedirs(path, exist_ok=True)
        download_image(path + '{}.jpg'.format(k), m.url)




if __name__ == "__main__":
    main()

