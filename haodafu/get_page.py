#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\haodafu")
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from get_ip import get_ip2

def restart_browser(browser,conn,cousor):
    '''
    从新获取ip地址
    :param doctor_dict:
    :param browser:
    :return:
    '''
    browser.quit()
    proxies = get_ip2(10,conn,cousor)
    browser_ = get_browser(proxies)
    return browser_

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

def get_page(url,proxies,headers):
    '''
    返回网页源代码
    :param url:
    :param http:
    :return:
    '''
    # http = urllib3.ProxyManager(proxies['http'], headers=hreaders)
    try:
        page = requests.get(url, headers=headers, proxies=proxies, timeout=5).text
        # page = requests.get(url, headers=headers, proxies=proxies, timeout=5).content.decode()
    except:
        page=''
    return page

def get_soup(page):
    '''
    传入数据，css解析http
    :param page:
    :return:
    '''
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def get_hos_link_page(browser):
    '''
    获取好大夫浙江地区的医院页面源代码
    :param browser:
    :return:
    '''
    browser.get('https://zhejiang.haodf.com/')
    browser.get('https://zhejiang.haodf.com/')
    return browser.page_source

def get_url_page(url,browser):
    '''
    获取url网页源代码
    :param url:
    :param browser:
    :return:
    '''
    browser.get(url)
    return browser.page_source

def get_hos_page(hos_url,browser):
    '''
    传入医院连接，获取医院网址首页源代码
    :param url:
    :param browser:
    :return:
    '''
    return get_url_page(hos_url,browser)


def get_ks_url_page(hos_url,browser):
    '''
    传入医院连接，获取医院科室列表源代码
    :param url:
    :param browser:
    :return:
    '''
    browser.get(hos_url)
    index = u'科室列表/门诊时间'
    click_ = browser.find_element_by_link_text(index)
    ActionChains(browser).click(click_).perform()
    index = u'查看全部科室列表>>'
    click_ = browser.find_element_by_link_text(index)
    ActionChains(browser).click(click_).perform()
    page=browser.page_source
    # print(page)
    return page


def get_ks_page(ks_url,browser):
    '''
    传入科室url，获取科室源代码
    :param ks_url:
    :param browser:
    :return:
    '''
    return get_url_page(ks_url,browser)


def get_doc_page(doc_url,browser):
    '''
    传入科室url，获取科室源代码
    :param ks_url:
    :param browser:
    :return:sssssss
    '''
    return get_url_page(doc_url,browser)