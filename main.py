import datetime
import time
from pprint import pprint

import pymongo
import requests
from bs4 import BeautifulSoup
from persian_tools import digits

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["carPricedb"]
mycol = mydb["cars"]

mycol.delete_many({})


class CarDataScraper:
    def __init__(self, api_url, post_url):
        self.url = api_url
        self.post_url = post_url
        self.car_datas = []
        self.time = int(str(round(time.time(), 6)).replace(".", ""))

    def scrape_data(self, count):
        while count >= len(self.car_datas):
            val = {"page": 1,
                   "json_schema": {"category": {"value": "cars"},
                                   "sort": {"value": "sort_date"},
                                   "cities": ["12"]},
                   "last-post-date": self.time}
            response = requests.post(self.url, json=val)
            res = response.json()
            for car in res['web_widgets']['post_list']:
                x = f"/v/{str(car['data']['title']).replace(' ', '-').replace('،', '')}/{car['data']['token']}"
                self.car_datas.append(x)

            print(self.car_datas)
            self.time = res['last_post_date']
            time.sleep(3)

        for url in self.car_datas:
            date = {}
            print(self.post_url + url)
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'}
                response = requests.get(self.post_url + url, headers=headers)
                print(response)
                res = BeautifulSoup(response.content, 'html.parser')

                res2 = res.find('div', class_='post-page__section--padded')
                km_moved = res2.find('table', class_='kt-group-row')
                ttt = km_moved.find_all('thead')
                ttt1 = km_moved.find_all('tbody')

                ttt3 = res.find('div', class_='kt-price-evaluation-row__indicator')
                date['معقولیت قیمت'] = ttt3['style'].split('(')[1].split('-')[0].split()[0]
                for i, j in zip(ttt, ttt1):
                    for c, v in zip([x.text for x in i.find_all('span')], [x.text for x in j.find_all('td')]):
                        date[c] = digits.convert_to_en(v.replace('٬', ''))
                brand = res2.find_all('div', class_='kt-base-row kt-base-row--large kt-unexpandable-row')
                for x in brand:
                    date[
                        x.find('div', class_='kt-base-row__start kt-unexpandable-row__title-box').text.replace('\u200c',
                                                                                                               '')] = digits.convert_to_en(
                        x.find('div', class_='kt-base-row__end kt-unexpandable-row__value-box').text.replace('٬',
                                                                                                             '').replace(
                            'تومان', '').replace('\u200c', '').replace('ماه', '').strip())

                # pprint(date)
                date['date_time'] = datetime.datetime.now()
                mycol.insert_one(date)
            except:
                pass


#
scraper = CarDataScraper('https://api.divar.ir/v8/web-search/12/cars', 'https://divar.ir')
scraper.scrape_data(5)

for x in mycol.find():
    pprint(x)
