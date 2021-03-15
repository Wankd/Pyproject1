#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\haodafu")
from get_page import get_soup
from bs4 import BeautifulSoup

def open_page():
    with open("C:\\Users\epsoft\Desktop\\html\\aaa.html",encoding='utf-8') as fp:
        soup = BeautifulSoup(fp,'html.parser')
    return soup


def get_hos_link(page=None):
    '''
    获取医院连接信息
    :param page:
    :return:[{'hos_name': '浙医二院', 'hos_link': 'https://www.haodf.com/hospital/DE4roiYGYZwmGYmS30yF9V0wc.htm', 'diqu': '杭州', 'zt': '医院采集状态'}]
    '''
    if page:
        soup=get_soup(page)
    else:
        soup=open_page()
    hos_link_list=soup.select('.jblb  td')
    diqu=''
    hos_=[]
    for line in hos_link_list:
        # print(line)
        hos_name=line.get_text().strip()
        try:
            hos_link='https:'+line.a['href']
            # print('%s -- %s -- %s' %(hos_name,hos_link,diqu))
            hos_.append({'hos_name':hos_name,'hos_link':hos_link,'diqu':diqu,'zt':''})
        except:
            if hos_name:
                diqu=hos_name
    return hos_

# if __name__ == '__main__':
#     print(get_hos_link()[0])