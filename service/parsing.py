import requests
from service import anonymity
from bs4 import BeautifulSoup as bs
from service.logger import logger
import lxml


def get_soup(url):
    html = get_html(url)
    soup = bs(html.text, 'lxml')
    return soup


def get_html(url):
    while True:
        random_proxy = anonymity.get_random_proxy()
        fake_user_agent = {'User-Agent': anonymity.get_fake_user_agent()}
        try:
            response = requests.get(url, headers=fake_user_agent, proxies=random_proxy)

            if response.status_code == 200:
                return response
            elif len(anonymity.PROXY_LIST) < 5:
                anonymity.PROXY_LIST = anonymity.update_proxy_list()
            else:
                response  = requests.get('https://anime-bit.ru', headers=fake_user_agent, proxies=random_proxy)
                if response.status_code == 200:
                    anonymity.update_proxy_list()
                    logger.warning("Закончились прокси сервера!")
                    return response
                else:
                    anonymity.PROXY_LIST.pop(anonymity.PROXY_LIST.index(random_proxy))
        except Exception:
            logger.warning(f'Не удалось получить данные с сайта -> {fake_user_agent} -> {Exception}')