import time
import json
import requests
from bs4 import BeautifulSoup
from peewee import SqliteDatabase, Model, CharField, IntegerField, DateField
from pprint import pprint

db = SqliteDatabase('car.db')


class Car(Model):
    production_year = DateField()
    color = CharField()
    function = IntegerField()
    brand_type = CharField()
    engine = IntegerField()
    chassi = IntegerField()
    body = IntegerField()
    insurance = IntegerField
    gearbox = CharField()
    price = IntegerField()

    class Meta:
        database = db


class CarDataScraper:
    def __init__(self, url, path):
        self.url = url
        self.path = path
        self.data = []
        self.time = int(str(round(time.time(), 6)).replace(".", ""))

    def scrape_data(self):
        print(self.time)
        val = {"page": 1,
               "json_schema": {"category": {"value": "cars"},
                               "sort": {"value": "sort_date"},
                               "cities": ["12"]},
               "last-post-date": self.time}
        response = requests.post(self.url + self.path, json=val)
        res = response.json()
        for car in res['web_widgets']['post_list']:
            print(car)



scraper = CarDataScraper('https://api.divar.ir', '/v8/web-search/12/cars')
scraper.scrape_data()
