#coding:utf-8

import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 引入 ActionChains 类
from bs4 import BeautifulSoup
import json,re
from datetime import datetime,timedelta
from time import sleep

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


def get_soup(page):
    '''
    传入数据，css解析http
    :param page:
    :return:
    '''
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def get_data(page,city_or_pro,city):
    # city_or_pro='城市级别'
    soup=get_soup(page)
    label=soup.select('.mgs-list-title')[0].text
    List = soup.select('.mgs-list-box tbody .undefined td')
    ll=[]
    date_ = (datetime.now() + timedelta(hours=-24)).strftime('%m-%d')
    l=[date_,city,label,city_or_pro]
    i=0
    for line in List:
        l.append(line.text)
        i+=1
        if i%3==0:
            ll.append(l)
            l=[date_,city,label,city_or_pro]
    return ll


def get_all_data(url,city,browser):
    List=[]
    page=get_url_page(url,browser)
    List.extend(get_data(page,'城市级别',city))
    print(1)
    sleep(10)
    click_ = browser.find_element_by_xpath('//*[@id="content"]/div/div[2]/ul/li[2]')
    ActionChains(browser).click(click_).perform()
    page = browser.page_source
    List.extend(get_data(page,'城市级别',city))
    print(2)
    sleep(10)
    click_ = browser.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/label[2]/span[2]')
    ActionChains(browser).click(click_).perform()
    page = browser.page_source
    List.extend(get_data(page, '省份级别',city))
    print(3)
    sleep(10)
    click_ = browser.find_element_by_xpath('//*[@id="content"]/div/div[2]/ul/li[1]')
    ActionChains(browser).click(click_).perform()
    page = browser.page_source
    List.extend(get_data(page, '省份级别',city))
    print(4)
    return List




def save_data(List):
    try:
        delete_date_qg='''delete from data_qx where date_="%s"''' % List[0][0]
        cursor.execute(delete_date_qg)
        print('删除成功')
        conn.commit()
    except:
        pass
    for line in List:
        insert_sql='''insert into data_qx values %s''' % str(tuple(line))
        cursor.execute(insert_sql)
    print('插入成功')
    conn.commit()


if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='root1', database='test', charset='utf8', port=3306)
    cursor = conn.cursor()
    browser=get_browser2()
    Dict={'浙江':330000,'杭州':330100,'宁波':330200,'温州':330300,
          '绍兴':330600,'湖州':330500,'嘉兴':330400,'金华':330700,
          '衢州':330800,'舟山':330900,'台州':331000,'丽水':331100}
    List=[]
    for city in Dict:
        city_url='https://qianxi.baidu.com/?from=shoubai#city='+str(Dict[city])
        # city_url = 'https://qianxi.baidu.com/?from=shoubai#city=' + str(300800)
        # city='衢州'
        List2=get_all_data(city_url,city,browser)
        List.extend(List2)
        browser.close()
        sleep(5)
        browser = get_browser2()
    save_data(List)
    cursor.close()
    conn.close()
    browser.close()