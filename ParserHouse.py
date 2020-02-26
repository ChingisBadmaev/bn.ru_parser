import requests
from bs4 import BeautifulSoup
import csv

URL ='https://www.bn.ru/kvartiry-vtorichka-petergof/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36', 'accept': '*/*'}
FILE = 'house.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('ul', class_='pagination')
    i = int(0)
    if pagination:
        return pagination[0].get_text()[-1]
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='catalog-item__container')
    houses = []
    for item in items:
        many_characteristic = item.find_all('span', class_='catalog-item__param-value')
        i = int(0)
        j = int(0)
        for characteristic in many_characteristic:
            j = j + 1
        if j == 5:
            for characteristic in many_characteristic:
                if i == 0:
                    living_space = characteristic.get_text()
                if i == 2:
                    height = characteristic.get_text()
                if i == 3:
                    floor = characteristic.get_text()
                i = i + 1
        if j == 4:
            for characteristic in many_characteristic:
                if i == 0:
                    living_space = characteristic.get_text()
                if i == 2:
                    floor = characteristic.get_text()
                height = 'Не известно'
                i = i + 1
        if j == 3:
            for characteristic in many_characteristic:
                if i == 0:
                    living_space = characteristic.get_text()
                if i == 1:
                    floor = characteristic.get_text()
                height = 'не известен'
                i = i + 1
        title = item.find('div', class_='catalog-item__headline').get_text().replace('                            м2', ' м2')
        area = title.split(' ')[-2]
        type_of_housing = title.replace(area, '')
        if len(type_of_housing.split(' ')) > 1:
            type_of_housing = type_of_housing.split(' ')[-3]
        else:
            type_of_housing = 'Студия'
        houses.append({
            'title': title,
            'type_of_housing': type_of_housing,
            'area': area,
            'rub_price': item.find('div', class_='catalog-item__price').get_text().replace('                                тыс. руб.\n                            ', ' тыс. руб'),
            'metro': item.find('span', class_='catalog-item__metro-name').get_text().replace('\xa0', ''),
            'metro_distance': item.find('span', class_='catalog-item__metro-distance').get_text(strip=True),
            'living_space': living_space,
            'height': height,
            'floor': floor,
        })
    return houses


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([
            'Тип жилья', 'общая площадь', 'цена в рублях', 'ближайшее метро', 'расстояние до метро', 'жилая площадь',
            'высота потолков', 'этаж'])
        for item in items:
            writer.writerow([item['type_of_housing'], item['area'], item['rub_price'], item['metro'],
                             item['metro_distance'], item['living_space'], item['height'], item['floor']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        houses = []
        pages_count = get_pages_count(html.text)
        for page in range(1, int(pages_count) + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            houses.extend(get_content(html.text))
        save_file(houses, FILE)
        print(houses)
    else:
        print('Error')


parse()







