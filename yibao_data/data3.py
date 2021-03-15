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


def get_data(page):
    l=[]
    soup=get_soup(page)
    List=soup.select('.ui-widget-content.jqgrow.ui-row-ltr')
    for i in range(len(List)):
        text=List[i].get_text('|').strip()
        l.append(text.split('|'))
        # print(len(text.split('|')))
    return l





def main(n):
    n=524
    List = []
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    browser = webdriver.Chrome( options=options)
    browser.get('http://code.nhsa.gov.cn:8000/ylfw/stdMedicalService/toPublicStdMedicalServiceStandardList.html?batchNumber=')
    sleep(randint(1, 5) + random())
    click_ = browser.find_element_by_id('treeDemo1_1_span')  # next_gridpage
    # click_ = browser.find_element_by_link_text(index)
    ActionChains(browser).click(click_).perform()
    sleep(randint(1, 5) + random())
    page = browser.page_source
    i=1
    List.extend(get_data(page))
    while i<n:
        try:
            click_=browser.find_element_by_id('next_gridpage') #next_gridpage
            # click_ = browser.find_element_by_link_text(index)
            ActionChains(browser).click(click_).perform()
            sleep(randint(1, 5) + random())
            page = browser.page_source
            List.extend(get_data(page))
            i+=1
            print(i)
        except:
            break
    browser.close()
    browser.quit()
    data=DataFrame(List,columns=['id','code1','code2','code3','项目代码','项目名称','项目内涵'
        ,'除外内容','计量单位','说明'])
    data.to_csv('C:\\Users\epsoft\Desktop\\全国医疗服务项目.csv',header=True,encoding='utf-8',index=False)


if __name__ == '__main__':
    main(361)
    # main3(10000000)
