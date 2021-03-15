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
    # List[0]
    for i in range(len(List)):
        text=List[i].get_text('|').strip()
        list_=text.split('|')
        while True:
            if len(list_)<18:
                list_.append('')
            else:
                break
        l.append(list_)
        # print(len(list_))
        # l[39]
    return l





def main2(n):
    List = []
    n=1606
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    browser = webdriver.Chrome( options=options)
    browser.get('http://code.nhsa.gov.cn:8000/yp/toPublishGoodsData.html?batchNumber=20191205')
    sleep(randint(1, 5) + random())
    # browser.get('http://code.nhsa.gov.cn:8000/hc/stdPublishData/toGgxhDetailDialog.html?specificationCode=C0101010010100204744')
    page=browser.page_source
    # print(page)
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
    List2=[]
    for line in List:
        lll=[str_.replace('\n',';') for str_ in line]
        List2.append(lll)
    List[3876]
    data=DataFrame(List,columns=['序号','药品代码','注册名称','商品名称','注册剂型','注册规格'
        ,'包装材质','最小包装数量','最小制剂单位','最小包装单位','药品企业','批准文号','药品本位码',
                                 '甲乙类','编号','药品名称','剂型','备注'])
    data.to_csv('C:\\Users\epsoft\Desktop\\医保药品分类与代码数据.csv',header=True,encoding='utf-8',index=False)
    data = DataFrame(List2, columns=['序号', '药品代码', '注册名称', '商品名称', '注册剂型', '注册规格'
        , '包装材质', '最小包装数量', '最小制剂单位', '最小包装单位', '药品企业', '批准文号', '药品本位码',
                                    '甲乙类', '编号', '药品名称', '剂型', '备注'])
    data.to_csv('C:\\Users\epsoft\Desktop\\医保药品分类与代码数据3.csv', header=True, encoding='utf-8', index=False)


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