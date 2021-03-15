#coding:utf-8
#采集医院医生数据
import re,os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 引入 ActionChains 类
from time import sleep
from yyys_doctor import get_doctor_msg
from save_data import get_ip2
from numpy import random


def get_doctor_link(page):
    '''
    获取某个页面的医师链接信息
    :param page:
    :return:
    '''
    pattern=re.compile('<a href=\"/doctor_\d+\.html\">[\u4E00-\u9FA5]+</a>')
    doctor_list=pattern.findall(page)
    Dict={}
    for dortor in doctor_list:
        doctor_name=re.search('[\u4E00-\u9FA5]+',dortor).group()
        doctor_link='http://www.mingyihui.net/' + re.search('/doctor_\d+\.html',dortor).group()
        Dict[doctor_name]=doctor_link
    return Dict


def get_doctor_dict(url,browser):
    '''
    获取当前科室所有医师链接信息
    :param url:
    :param browser:
    :return:
    '''
    browser.get(url)
    page = browser.page_source
    index = u'下一页'
    i = 1
    Dict = {}
    j=10
    while index in page and j<=10:
        doctor_link_Dict = get_doctor_link(page)
        Dict.update(doctor_link_Dict)
        click = browser.find_element_by_link_text(index)
        ActionChains(browser).click(click).perform()
        sleep(random.random()+random.randint(0,2))
        url = browser.current_url
        browser.get(url)
        page = browser.page_source
        i += 1
        j+=1
    doctor_link_Dict = get_doctor_link(page)
    Dict.update(doctor_link_Dict)
    return Dict


def get_doctor_page(doctor_link,browser):
    '''
    得到某个医师网页源代码
    :param doctor_link:
    :param browser:
    :return:
    '''
    browser.get(doctor_link)
    return browser.page_source


def get_ksjs_doctor_List(doctor_dict,kesi_name_1,word,browser,conn,cousor):
    '''
    传入科室url,采集科室医师的数据,返回某个医院某个科室的所有医师信息数据
    :param url:
    :param browser:
    :return:
    '''
    doctor_one_ks_List=[] #某个医院某个科室的医师所有数据
    for doctor_name in doctor_dict:
        doctor_link=doctor_dict[doctor_name]
        Dict={}
        while Dict==dict():
            try:
                doctor_page = get_doctor_page(doctor_link, browser)
                Dict = get_doctor_msg(doctor_page,kesi_name_1,word)
                doctor_one_ks_List.append(Dict)
            except:
                browser=reget_ip(browser,conn,cousor)
        sleep(random.random()+random.randint(0,2))
    return doctor_one_ks_List


def get_browser(ip):
    '''
    从新获取ip地址
    :param ip:
    :return:
    '''
    chromeOptions = webdriver.ChromeOptions()
    str_ = '--proxy-server=%s' % ip  # 设置代理
    chromeOptions.add_argument(str_)
    # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    browser.set_page_load_timeout(60)
    return browser


def reget_ip(browser,conn,cousor):
    '''
    从新获取ip地址
    :param doctor_dict:
    :param browser:
    :return:
    '''
    browser.quit()
    proxies = get_ip2(10,conn,cousor)
    ip = proxies['http']
    browser_ = get_browser(ip)
    return browser_


def get_all_doctor_msg(ip,ksjs,conn,cousor):
    '''
    传入某个医院的所有科室数据，返回某个所有医师数据
    :param ip:
    :param ksjs:
    :return:
    '''
    all_dcotor_List=[]
    browser = get_browser(ip)
    for ksjs_msg in ksjs:
        ksjs_url=ksjs_msg['kesi_link_1'] #科室连接
        kesi_name=ksjs_msg['kesi_name'] #科室大类
        kesi_name_1=ksjs_msg['kesi_name_1'] #科室小类
        word=ksjs_msg['word']
        doctor_dict={}
        if kesi_name!=u'特色科室':
            print(ksjs_msg['kesi_name_1'])
            while doctor_dict == dict():
                try:
                    doctor_dict = get_doctor_dict(ksjs_url, browser)  # 获取医师链接
                    if doctor_dict==dict():
                        break
                except:
                    browser = reget_ip(browser,conn,cousor)
        if doctor_dict!=dict():
            doctor_one_ks_List=get_ksjs_doctor_List(doctor_dict,kesi_name_1,word,browser,conn,cousor)
            all_dcotor_List.extend(doctor_one_ks_List)
            print('seccess')
    browser.quit()
    return all_dcotor_List

# if __name__ == '__main__':
#     ksjs=[{'kesi_name': '外科', 'kesi_name_1': '肛肠科', 'kesi_link_1': 'http://www.mingyihui.net//hospitalx_392/department_98.html', 'kesi_renshu': '28'},
#           {'kesi_name': '外科', 'kesi_name_1': '胃肠外科', 'kesi_link_1': 'http://www.mingyihui.net//hospitalx_392/department_105.html', 'kesi_renshu': '5'},]
#     ip = 'http://202.20.16.82:10152'
#     get_all_doctor_msg(ip,ksjs)