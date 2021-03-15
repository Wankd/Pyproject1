#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\haodafu")
from selenium.webdriver.common.action_chains import ActionChains
from get_page import get_soup
from get_doc_link import get_doc_link
from time import sleep
from random import random,randint


def get_ks_jj(page):
    soup=get_soup(page)
    ks_jj=''
    try:
        ks_jj=soup.select('.box_a #about_det')[0].get_text().strip()
    except:
        page
    return ks_jj



def get_ks_msg(ks_name,hos_name,ks_url,browser):
    '''

    :param ks_name:
    :param hos_name:
    :param ks_url:
    :param browser:
    :return: {'doc_url':医师链接,'doc_name':医师名称,'doc_zc':医师职称,'doc_jzdz':就诊地址,'ks_name':科室名称,'hos_name':医院名称,'zt':采集状态}
    '''
    browser.get(ks_url)
    ks_jj=''
    try:
        index = u'完整介绍>>'
        click_ = browser.find_element_by_link_text(index)
        ActionChains(browser).click(click_).perform()
        page=browser.page_source
        ks_jj=get_ks_jj(page)
        sleep(randint(1,5)+random())
        browser.get(ks_url)
    except:
        pass
    ks_jj_dict={'ks_name':ks_name,'hos_name':hos_name,'ks_jj':ks_jj}
    doc_list=[] #科室医师信息
    page = browser.page_source
    doc_list1,index = get_doc_link(ks_name,hos_name,page)
    doc_list.extend(doc_list1)
    while index==u'下一页':
        try:
            click_ = browser.find_element_by_link_text(index)
            ActionChains(browser).click(click_).perform()
            sleep(randint(1, 5) + random())
            page = browser.page_source
            doc_list1,index = get_doc_link(page)
            doc_list.extend(doc_list1)
        except:
            break
    return ks_jj_dict,doc_list

