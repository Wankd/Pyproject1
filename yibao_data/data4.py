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
    List[0]
    for i in range(len(List)):
        text=List[i].get_text('|').strip()
        l.append(text.split('|'))
    return l





def main(n):
    n=361
    List = []
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    browser = webdriver.Chrome( options=options)
    # browser.get('http://code.nhsa.gov.cn:8000/hc/stdPublishData/toQueryStdPublishDataList.html?batchNumber=')
    browser.get('http://code.nhsa.gov.cn:8000/hc/stdSpecification/toStdSpecificationList.html?batchNumber=')
    page=browser.page_source
    # browser.get('http://code.nhsa.gov.cn:8000/search.html?sysflag=86')
    # aaa=browser.find_element_by_css_selector('''a[onclick='detail("C0101010010100204744")']''')
    # ActionChains(browser).click(aaa).perform()
    # handle=browser.switch_to_alert()
    # browser.switch_to.default_content()
    # all_handles = browser.window_handles
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
    data=DataFrame(List,columns=['id','code','医用耗材代码','三级分类代码','一级分类','二级分类','三级分类'
        ,'通用名代码','通用名','材质代码','耗材材质','规格代码','规格'])
    data.to_csv('C:\\Users\epsoft\Desktop\\医保医用耗材分类与代码.csv',header=True,encoding='utf-8',index=False)


if __name__ == '__main__':
    main(361)
    # main3(10000000)
