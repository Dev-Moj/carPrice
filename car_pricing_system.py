import datetime
import time
from pprint import pprint
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pymongo
import requests
from bs4 import BeautifulSoup
from persian_tools import digits
from sklearn import tree
import sys

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["carPricedb"]
mycol = mydb["cars"]

class CarDataScraper:
    def __init__(self, api_url, post_url):
        self.url = api_url
        self.post_url = post_url
        self.car_datas = []
        self.learning_datas = []
        self.time = int(str(round(time.time(), 6)).replace(".", ""))

    def scrape_data(self, count):
        while count >= len(self.car_datas):
            val = {"page": 1,
                   "json_schema": {"category": {"value": "cars"},
                                   "sort": {"value": "sort_date"},
                                   "cities": ["12"]},
                   "last-post-date": self.time}
            try:
                response = requests.post(self.url, json=val)
            except requests.exceptions.ConnectionError as e:
                print("Connection error:", str('internet error '))
                sys.exit(1)
            except requests.exceptions.Timeout:
                print("Request timeout")
                sys.exit(1)
            except requests.exceptions.RequestException as e:
                print("Error:", str(e))
                sys.exit(1)

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
                thead = km_moved.find_all('thead')
                tbody = km_moved.find_all('tbody')

                kt_price = res.find('div', class_='kt-price-evaluation-row__indicator')
                date['معقولیت قیمت'] = kt_price['style'].split('(')[1].split('-')[0].split()[0].replace('%', '')
                for i, j in zip(thead, tbody):
                    for c, v in zip([x.text for x in i.find_all('span')], [x.text for x in j.find_all('td')]):
                        date[c] = digits.convert_to_en(v.replace('٬', ''))
                datas = res2.find_all('div', class_='kt-base-row kt-base-row--large kt-unexpandable-row')
                for x in datas:
                    date[
                        x.find('div', class_='kt-base-row__start kt-unexpandable-row__title-box').text.replace('\u200c',
                                                                                                               '')] = digits.convert_to_en(
                        x.find('div', class_='kt-base-row__end kt-unexpandable-row__value-box').text.replace('٬',
                                                                                                             '').replace(
                            'تومان', '').replace('\u200c', '').replace('ماه', '').replace('هستم', True).strip())

                date['date_time'] = datetime.datetime.now()
                mycol.insert_one(date)
            except:
                pass

    def learning(self, prompt):
        X = []
        Y = []
        pr = {
            'معقولیت قیمت': "",
            'کارکرد': '',
            'مدل (سال تولید)': '',
            'رنگ': '',
            'نوع آگهی': '',
            'برند و تیپ': '',
            'نوع سوخت': '',
            'وضعیت موتور': '',
            'وضعیت شاسیها': '',
            'وضعیت بدنه': '',
            'مهلت بیمهٔ شخص ثالث': '',
            'گیربکس': '',
            'مایل به معاوضه': ''}
        for i in mycol.find():
            # print(i)
            for e, f in zip(i.keys(),i.values()):
                if e in pr.keys():
                    # print(e)
                    pr[e]=f
                    X.append(list(pr.values()))
            Y.append(list(i.values())[-2])





scraper = CarDataScraper()
scraper.scrape_data(1)
# scraper.learning()
