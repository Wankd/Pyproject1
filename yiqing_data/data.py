#coding:utf-8

import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 引入 ActionChains 类
from bs4 import BeautifulSoup
import json,re
from datetime import datetime,timedelta
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

def get_soup(page):
    '''
    传入数据，css解析http
    :param page:
    :return:
    '''
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def get_data(page):
    '''

    :param page:
    :return: data_qg全国数据，data_mx数据
    '''
    soup=get_soup(page)
    date_=(datetime.now()+timedelta(hours=-24)).strftime('%m-%d')
    time_ = soup.select('body .topdataWrap .timeNum .d span')[0].text.strip() #数据更新时间
    label_1_1 = soup.select('body .topdataWrap .recentNumber .icbar.confirm .add span')[0].text.strip()  # 全国确诊较上日
    label_1_2 = soup.select('body .topdataWrap .recentNumber .icbar.confirm .number')[0].text.strip()  # 全国确诊人数
    label_2_1 = soup.select('body .topdataWrap .recentNumber .icbar.nowConfirm .add span')[0].text.strip()  # 全国疑似病例较上日
    label_2_2 = soup.select('body .topdataWrap .recentNumber .icbar.nowConfirm  .number')[0].text.strip()  # 全国疑似病例数
    label_3_1 = soup.select('body .topdataWrap .recentNumber .icbar.heal .add span')[0].text.strip()  # 全国治愈人数较上日
    label_3_2 = soup.select('body .topdataWrap .recentNumber .icbar.heal .number')[0].text.strip()  # 全国治愈人数
    label_4_1 = soup.select('body .topdataWrap .recentNumber .icbar.dead .add span')[0].text.strip()  # 全国死亡人数较上日
    label_4_2 = soup.select('body .topdataWrap .recentNumber .icbar.dead .number')[0].text.strip()  # 全国死亡人数
    label_ = soup.select('body .chinaListWraper .listWraper table tbody') # 全国情况
    # label_[0].text
    data_qg=[date_,time_,label_1_1,label_1_2,label_2_1,label_2_2,label_3_1,label_3_2,label_4_1,label_4_2]
    # data_mx=[]
    # for label in label_:
    #     data_=re.sub(r'\s+|\n+',',',label.get_text('\n').strip())
    #     data_ = re.sub(r',详情,', ',', data_)
    #     data_list=re.split(',',data_)
    #     List = []
    #     for i in range(len(data_list)):
    #         List.append(data_list[i])
    #         pro=[date_,data_list[0]]
    #         if i%5==4:
    #             pro.extend(List)
    #             pro.append('详情')
    #             data_mx.append(pro)
    #             List=[]
    return data_qg#,data_mx


def insert_zj():
    conn = pymysql.connect(
        host='localhost', user='root', password='root1', database='test', charset='utf8', port=3306)
    cursor = conn.cursor()
    file=open('C:\pycharmproject\\venv37\data_sub\yiqing_data\浙江.csv',encoding='utf-8')
    lines=file.readlines()
    for line in lines:
        line=line.strip()
        print(len(line.split(',')))
        insert_sql = '''insert into data_mx values %s''' % str(tuple(line.split(',')))
        print(insert_sql)
        cursor.execute(insert_sql)
    conn.commit()
    file.close()
    cursor.close()
    conn.close()


def insert_qg():
    conn = pymysql.connect(
        host='localhost', user='root', password='root1', database='test', charset='utf8', port=3306)
    cursor = conn.cursor()
    file=open('C:\pycharmproject\\venv37\data_sub\yiqing_data\全国.csv')
    lines=file.readlines()
    for line in lines:
        line=line.strip()
        print(len(line.split(',')))
        insert_sql = '''insert into data_qg values %s''' % str(tuple(line.split(',')))
        print(insert_sql)
        cursor.execute(insert_sql)
    conn.commit()
    file.close()
    cursor.close()
    conn.close()


def save_data(conn,cursor,page):
    # data_qg, data_mx=get_data(page)
    data_qg=get_data(page)
    try:
        delete_date_qg='''delete from data_qg where date_="%s"''' % data_qg[0]
        cursor.execute(delete_date_qg)
        print('删除成功')
        conn.commit()
    except:
        pass
    insert_sql='''insert into data_qg values %s''' % str(tuple(data_qg))
    cursor.execute(insert_sql)
    print('插入成功')
    conn.commit()
    # try:
    #     delete_date_mx='''delete from data_mx where date_="%s"''' % data_mx[0][0]
    #     cursor.execute(delete_date_mx)
    #     conn.commit()
    #     print('删除成功')
    # except:
    #     pass
    # for i in data_mx:
    #     insert_sql='''insert into data_mx values %s''' % str(tuple(i))
    #     cursor.execute(insert_sql)
    # conn.commit()
    # print('插入成功')


if __name__ == '__main__':
    conn = pymysql.connect(
        host='localhost', user='root', password='root1', database='test', charset='utf8', port=3306)
    cursor = conn.cursor()
    browser=get_browser2()
    page=get_url_page('https://news.qq.com/zt2020/page/feiyan.htm',browser)
    save_data(conn,cursor,page)
    cursor.close()
    conn.close()
    browser.close()