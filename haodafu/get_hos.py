#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\haodafu")
from bs4 import BeautifulSoup
from get_page import get_url_page,get_soup,get_hos_page
from time import sleep



def get_jj(url,browser):
    sleep(5)
    page=get_url_page(url,browser)
    soup=get_soup(page)
    try:
        jj=soup.select('.czsj td')[0].get_text().strip()
    except:
        jj=''
    return jj

def get_dz(url,browser):
    dh=''
    lx=''
    dz=''
    sleep(5)
    page = get_url_page(url, browser)
    soup = get_soup(page)
    data_list = soup.select('.bluepanel tbody tr td table tr td')
    for i in range(len(data_list)):
        text=data_list[i].get_text()
        if u'电话：' in text:
            try:
                dh=data_list[i+1].get_text()
            except:
                pass
        if u'地址：' in text:
            try:
                dz = data_list[i + 1].get_text()
            except:
                pass
        if u'怎么走：' in text:
            try:
                lx = data_list[i + 1].get_text()
            except:
                pass
    return lx,dz,dh

def get_hos_msg(url,browser):
    '''
    'name':'医院名称','djlx':'等级类型','jj':'简介','dz':'地址','lx':'路线','dh':电话
    :param page:
    :param browser:
    :return:
    '''
    page=get_hos_page(url,browser)
    hos_dis={'hos_name':'','djlx':'','jj':'','dz':'','lx':'','dh':''}
    soup = get_soup(page)
    hos_name=soup.select('.hospital-name')[0].get_text() #医院名称
    hos_djlx = ','.join([i.get_text() for i in soup.select('.hospital-label-item')]) #医院等级类型
    hos_dis['hos_name']=hos_name
    hos_dis['djlx']=hos_djlx
    hos_msg1 = soup.select('.h-d-c-item .h-d-c-item-name')
    hos_msg2 = soup.select('.h-d-c-item .h-d-c-item-text')
    hos_msg3 = soup.select('.h-d-c-item .h-d-c-item-link')
    for i in range(len(hos_msg1)):
        msg1=hos_msg1[i].get_text() # 名称
        msg2= hos_msg2[i].get_text().strip() # 内容
        try:
            msg3= 'https:'+hos_msg3[i]['href'] # 连接
        except:
            msg3=None
        if u'简介' in msg1:
            if msg3:
                hos_dis['jj']=msg2 if 'javascript:void(0)' in msg3 else get_jj(msg3,browser)
            else:
                hos_dis['jj'] = msg2
        if u'地址' in msg1:
            if 'javascript:void(0)' in msg3 or msg3 is None:
                hos_dis['dz']=msg2
            else:
                lx,dz,dh=get_dz(msg3,browser)
                hos_dis['lx'] = lx
                hos_dis['dz'] = dz
                hos_dis['dh'] = dh
        hos_dis['lx']=msg2 if hos_dis['lx']=='' else hos_dis['lx']
        hos_dis['dh'] = msg2 if hos_dis['dh'] == '' else hos_dis['dh']
    # print(hos_dis)
    return hos_dis
