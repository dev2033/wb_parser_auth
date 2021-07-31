""" Сервисы
"""
import random
import time

import requests
from selenium import webdriver
from fake_useragent import UserAgent
from config import path_chromedriver, login


def write_state_parser(_state: str):
    with open('state_parsing.json', 'w') as state:
        st = '{' + f'"parser_state": {_state}' + '}'
        state.write(st)


def get_new_json(product_id):
    """Получает новые данные в формате json по артикулу товара """
    headers = {
        'User-Agent': user_agent(),
    }
    url = f'https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?' \
          f'spp=12&pricemarginCoeff=1.0&reg=1&appType=1&' \
          f'offlineBonus=0&onlineBonus=0&emp=0&locale=ru&' \
          f'lang=ru&curr=rub&nm={product_id}'
    r = requests.get(url, headers)
    return r.text


def user_agent() -> any:
    """Возвращает рандомный user-agent"""
    ua = UserAgent()
    return ua.random


def get_web_driver_options() -> any:
    """Возвращает опции веб драйвера"""
    option = webdriver.ChromeOptions()
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument('--disable-notifications')
    option.add_argument('--no-sandbox')
    option.add_argument(f'--user-agent={user_agent()}')
    option.add_argument('--disable-extensions')
    option.add_argument('--disable-gpu')
    option.add_argument('--headless')
    option.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(path_chromedriver, options=option)
    return driver


def delay() -> None:
    """Засыпает"""
    time.sleep(random.randint(2, 4))
