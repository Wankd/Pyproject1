#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\haodafu")
import re,urllib3,requests,random
from time import sleep
from datetime import datetime
from save_data import sava_pt_ip
from bs4 import BeautifulSoup

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


def get_ip2(n,conn,cursor):
    '''
    自动获取可用ip，并且执行到结尾
    :param n:
    :param conn:
    :param cursor:
    :return:
    '''
    sql='''select ptip from ptip_msg where label="" limit 3'''
    cursor.execute(sql)
    data=cursor.fetchall()
    proxies = {"https": "https://" + '127.0.0.1',"http": "http://" + '127.0.0.1'}
    if len(data)!=3:
        pt_ip_list = get_pt_ip_list(n)
        sava_pt_ip(pt_ip_list, 100, conn, cursor)
        sql = '''select ptip from ptip_msg where label="" limit 3'''
        cursor.execute(sql)
        data = cursor.fetchall()
    while 0<1:
        ip = data[0][0]
        print(ip)
        try:
            cursor.execute('''update ptip_msg set label="1" where ptip="%s"''' %ip)
            conn.commit()
            proxies = {"https": "https://" + ip,"http": "http://" + ip}
            sleep(2)
            res = requests.get('https://zhejiang.haodf.com/', headers=getheaders(), proxies=proxies, timeout=3)
            print(u'已经获取ip')
            break
        except:
            sql = '''select ptip from ptip_msg where label="" limit 3'''
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) !=3:
                pt_ip_list = get_pt_ip_list(n)
                sava_pt_ip(pt_ip_list, 100, conn, cursor)
    print(proxies)
    return proxies