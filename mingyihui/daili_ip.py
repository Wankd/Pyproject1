#coding:utf-8
#采集数据到mysql
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\mingyihui")
import random,json,urllib3,requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import numpy as np
# from save_data import get_conn,sava_pt_ip
#-----------------------------------------------------------------------------------------------------------------------
def get_daili_http():
    host = 'http://ipproxyv2.market.alicloudapi.com'
    path = '/devtoolservice/ipagency'
    method = 'GET'
    appcode = '39a1655fb4504475b4c260ac6a0b14bd' #购买得到的
    querys = 'foreigntype=0&protocol=0'
    bodys = {}
    url = host + path + '?' + querys
    import urllib3
    headers = {
       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Authorization':'APPCODE ' + appcode
    }
    http_daili = urllib3.PoolManager(headers = headers)
    return http_daili,url


def get_daili_ip(daili_http, url):
    label=''
    while u'成功'!=label:
        content=daili_http.request('get',url).data.decode()
        print(content)
        content_=json.loads(content)
        # type(content_)
        label=content_['reason']
    return content_['result']
#-----------------------------------------------------------------------------------------------------------------------

def getheaders():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent=random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers


def get_ip_list(url, headers):
    '''
    获取西刺代理页面的ip地址
    :param url:
    :param headers:
    :return:
    '''
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'html.parser')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


def get_random_ip(ip_list,headers):
    proxies={"http":''}
    for ip in ip_list:
        print(ip)
        try:
            proxies = {"http": "http://" + ip}
            res = requests.get('http://www.mingyihui.net/', headers=headers, proxies=proxies, timeout=3)
            break
        except:
            pass
    print(proxies)
    return proxies


def get_ip(max_index):
    proxies = {"http": ''}
    headers = getheaders()
    for index in np.arange(1,max_index):
        url='http://www.xicidaili.com/nn/%s' %index
        ip_list = get_ip_list(url, headers=headers)
        proxies=get_random_ip(ip_list,headers)
        if proxies["http"]=='':
            pass
        else:
            break
    return proxies


def get_pt_ip_list(n):
    '''
    获取n页普通代理ip数据
    :param n:
    :return:
    '''
    pt_ip_list=[]
    for i in range(1,n):
        print(i)
        header=getheaders()
        url_='https://www.xicidaili.com/nn/%s' %i
        # url_ = 'https://www.xicidaili.com/nn/1' % i
        for ip in get_ip_list(url_, header):
            pt_ip_list.append({'ptip':ip,'label':'','ctime':datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        sleep(random.randint(3,10))
    return pt_ip_list


# if __name__ == '__main__':
#     n=2
#     conn, cursor = get_conn('test')
#     pt_ip_list=get_pt_ip_list(n)
#     sava_pt_ip(pt_ip_list,100,conn, cursor)
#     cursor.close()
#     conn.close()

