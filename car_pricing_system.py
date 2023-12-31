import datetime
import sys
import time
from pprint import pprint
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn import tree
import pymongo
import requests
from bs4 import BeautifulSoup
from persian_tools import digits

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["carPricedb"]
mycol = mydb["cars"]

mycol.delete_many({})


class CarDataScraper:
    t_date = {
        'قیمت پایه': 'base_price',
        'کارکرد': 'usage',
        'مدل (سال تولید)': 'year',
        'رنگ': 'colors',
        'نوع آگهی': 'type',
        'برند و تیپ': 'brand_model',
        'نوع سوخت': 'fuel_type',
        'وضعیت موتور': 'motor_status',
        'وضعیت شاسیها': 'chassis_status',
        'وضعیت بدنه': 'body_status',
        'مهلت بیمهٔ شخص ثالث': 'third_party_insurance_deadline',
        'شاسی عقب': 'back_chassis_status',
        'شاسی جلو': 'front_chassis_status',
        'گیربکس': 'gearbox',
        'مایل به معاوضه': 'exchange'}
    data = {'آبی': '0001',
            'آلبالویی': '0002',
            'اتوماتیک': '0003',
            'اطلسی': '0004',
            'اوراقی': '0005',
            'بادمجانی': '0006',
            'برنز': '0007',
            'بنزینی': '0008',
            'بنفش': '0009',
            'بژ': '0010',
            'تصادفی': '0011',
            'تعویض شده': '0012',
            'تمامرنگ': '0013',
            'تیتانیوم': '0014',
            'رنگشده': '0015',
            'جلو ضربهخورده': '0016',
            'خاکستری': '0017',
            'خاکی': '0018',
            'خط و خش جزیی': '0019',
            'دلفینی': '0020',
            'دندهای': '0021',
            'دوررنگ': '0022',
            'دوگانهسوز دستی': '0023',
            'دوگانهسوز شرکتی': '0024',
            'ذغالی': '0025',
            'رنگشدگی': '0026',
            'زرد': '0027',
            'زرشکی': '0028',
            'زیتونی': '0029',
            'سالم': '0030',
            'سالم و بیخط و خش': '0031',
            'سبز': '0032',
            'سربی': '0033',
            'سرمهای': '0034',
            'سفید': '0035',
            'سفید صدفی': '0036',
            'صافکاری بیرنگ': '0037',
            'طلایی': '0038',
            'طوسی': '0039',
            'عدسی': '0040',
            'عقب رنگشده': '0041',
            'عقب رنگشده، جلو ضربهخورده': '0042',
            'عقب ضربهخورده': '0043',
            'عقب ضربهخورده، جلو رنگشده': '0044',
            'عنابی': '0045',
            'قرمز': '0046',
            'قهوهای': '0047',
            'مسی': '0048',
            'مشکی': '0049',
            'موکا': '0050',
            'نارنجی': '0051',
            'نقرآبی': '0052',
            'نقرهای': '0053',
            'نوک‌مدادی': '0054',
            'نیاز به تعمیر': '0055',
            'سالم و پلمپ': '0056',
            'هردو رنگشده': '0057',
            'ضربهخورده': '0058',
            'پوستپیازی': '0059',
            'کربنبلک': '0060',
            'کرم': '0061',
            'گازوئیل': '0062',
            'گیلاسی': '0063',
            'یشمی': '0064',
            'فروشی': '0065'}

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
                print(response)
            except requests.exceptions.ConnectionError as e:
                print("Connection error:", str(e))
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
            if not self.car_datas:
                continue
            print(self.car_datas)
            self.time = res['last_post_date']
            time.sleep(3)

        for url in self.car_datas:
            data_u = {}
            date = {
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
                'شاسی عقب': '',
                'شاسی جلو': '',
                'گیربکس': '',
                'مایل به معاوضه': '',
                'قیمت پایه': ''}
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

                for i, j in zip(thead, tbody):
                    for c, v in zip([x.text for x in i.find_all('span')], [x.text for x in j.find_all('td')]):
                        date[c] = digits.convert_to_en(v.replace('٬', ''))
                datas = res2.find_all('div', class_='kt-base-row kt-base-row--large kt-unexpandable-row')
                for x in datas:
                    key = x.find('div', class_='kt-base-row__start kt-unexpandable-row__title-box').text.replace(
                        '\u200c', '')
                    valus = digits.convert_to_en(
                        x.find('div', class_='kt-base-row__end kt-unexpandable-row__value-box').text.replace('٬',
                                                                                                             '').replace(
                            'تومان', '').replace('\u200c', '').replace('ماه', '').replace('هستم', '1').strip())
                    date[key] = valus
                data_u['average_price'] = kt_price['style'].split('(')[1].split('-')[0].split()[0].replace('%', '')
                data_u['date_time'] = datetime.datetime.now()
                for y, e in zip(date.keys(), date.values()):
                    data_u[self.t_date[y]] = e if e not in self.data.keys() else self.data[e]

                mycol.insert_one(data_u)
            except:
                print('error')
                pass
        time.sleep(3)

    def learning(self):
        X = []
        Y = []

        for i in mycol.find():
            for e, f in zip(i.keys(), i.values()):
                print(e, ':', f)
        #         if e in pr.keys():
        #             pr[e]=f
        #     X.append(list(pr.values()))
        #     Y.append(list(i.values())[-2])
        # pprint(X)
