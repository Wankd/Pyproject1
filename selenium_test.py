#coding:utf-8

import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 引入 ActionChains 类
from bs4 import BeautifulSoup
import json,re
from datetime import datetime,timedelta
from time import sleep
def get_browser(proxies):
    '''
    从新获取ip地址
    :param ip:
    :return:
    '''
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    chromeOptions = webdriver.ChromeOptions()
    str_ = '--proxy-server=%s' % proxies['http']  # 设置代理
    chromeOptions.add_argument(str_)
    # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
    browser = webdriver.Chrome(chrome_options=chromeOptions,options=options)
    browser.set_page_load_timeout(60)
    return browser


def get_browser2():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    browser = webdriver.Chrome(options=options)
    return browser

def get_url_page(url,browser):
    '''
    获取url网页源代码
    :param url:
    :param browser:
    :return:
    '''
    browser.get(url)
    return browser.page_source


if __name__ == '__main__':
    browser=get_browser2()
    while 0<1:
        page=get_url_page('https://mp.weixin.qq.com/s/jTXF4KUMMi3j-rk6QR8dfw',browser)
        sleep(5)
    browser.close()