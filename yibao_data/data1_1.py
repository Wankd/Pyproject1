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
    return l





def main2(n):
    List = []
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    browser = webdriver.Chrome( options=options)
    browser.get('http://code.nhsa.gov.cn:8000/hc/stdPublishData/toQueryStdPublishDataList.html?batchNumber=')
    # browser.get('http://code.nhsa.gov.cn:8000/hc/stdPublishData/toGgxhDetailDialog.html?specificationCode=C0101010010100204744')
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
            click_=browser.find_element_by_id('next_gridpage')
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
    data=DataFrame(List,columns=['id','医用耗材代码1','医用耗材代码2','一级分类','二级分类','三级分类'
        ,'医保通用名','耗材材质','规格','耗材生产企业','操作'])
    data.to_csv('C:\\Users\epsoft\Desktop\\耗材公示公布.csv',header=True,encoding='utf-8',index=False)


if __name__ == '__main__':
    main2(607)
    # main3(10000000)


# self.url = url
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
# self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
# self.wait = WebDriverWait(self.browser, 10) #超时时长为10s
# self.browser.get(self.url) # 这次返回的是 521 相关的防爬js代码
# self.browser.get(self.url) # 调用2次 self.browser.get 解决 521 问题
# html = self.browser.page_source