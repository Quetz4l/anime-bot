from local_fake_useragent import UserAgent
from Proxy_List_Scrapper import Scrapper
from random import randint
from loguru import logger

PROXY_LIST = []


def update_proxy_list():
    scrapper = Scrapper(category='US', print_err_trace=False)
    data = scrapper.getProxies()
    proxy_list = []
    for proxy in data.proxies:
        proxy_list.append({'http://': 'http://' + proxy.ip + ':' + proxy.port})

    logger.success('Loaded ' + str(len(proxy_list)) + ' proxies')

    global PROXY_LIST
    PROXY_LIST = proxy_list

    # return [{'http://': 'http://74.205.128.200:80'}, {'http://': 'http://13.66.222.94:80'}]


def get_fake_user_agent():
    fake_user_agent = UserAgent()
    return fake_user_agent.rget


def get_random_proxy():
    return PROXY_LIST[randint(0, len(PROXY_LIST)-1)]


update_proxy_list()
