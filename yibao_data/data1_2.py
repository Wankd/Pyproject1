#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\haodafu")
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains  # 引入 ActionChains 类
import os
from bs4 import BeautifulSoup
from get_hos import get_hos_msg
from time import sleep
from random import random,randint
from pandas import DataFrame
import pandas as pd


def get_soup(page):
    '''
    传入数据，css解析http
    :param page:
    :return:
    '''
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def get_data3(str_,page):
    l = []
    soup = get_soup(page)
    List = soup.select('.form-table.form-table-2.form-table-info #content tr')
    for i in range(len(List)):
        text = str_+'|'+List[i].get_text('|').strip()
        l.append(text.split('|'))
    return l


def main3(n):
    List = []
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    browser = webdriver.Chrome(options=options)
    file=open('C:\\Users\epsoft\Desktop\\耗材公示公布.csv',encoding='utf-8')
    lines=file.readlines()
    i=0
    for line in lines:
        list_=line.split(',')
        str_=list_[1]+list_[2]
        if i>=1 and i<=n:
            print(str_)
            browser.get('http://code.nhsa.gov.cn:8000/hc/stdPublishData/toGgxhDetailDialog.html?specificationCode=%s' %str_)
            sleep(randint(1, 5) + random())
            page=browser.page_source
            List.extend(get_data3(str_,page))
        i+=1
    file.close()
    browser.close()
    browser.quit()
    new_data = DataFrame(List, columns=['医用耗材代码','注册证号','单件产品名称','规格型号数'])
    new_data.to_csv('C:\\Users\epsoft\Desktop\\详情.csv', header=True, encoding='utf-8', index=False)


if __name__ == '__main__':
    # main2(607)
    main3(10000000)


# self.url = url
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
# self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
# self.wait = WebDriverWait(self.browser, 10) #超时时长为10s
# self.browser.get(self.url) # 这次返回的是 521 相关的防爬js代码
# self.browser.get(self.url) # 调用2次 self.browser.get 解决 521 问题
# html = self.browser.page_source