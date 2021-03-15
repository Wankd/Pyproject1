#coding:utf-8
import re
import urllib3
import requests

def power(a,b):
    if b>0:
        return a*power(a,b-1)
    else:
        return 1


def get_http():
    '''
    模拟浏览器，进行数据采集初始化
    :return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
    http = urllib3.PoolManager(headers=headers)
    return http

def get_page(url,http):
    '''
    返回网页源代码
    :param url:
    :param http:
    :return:
    '''
    try:
        page=http.request('get',url).data.decode()
    except:
        page=''
    return page

def get_mingyihui_url(word,http):
    '''
    获取名医汇，某个医院的页面url的四个连接
    :param word:
    :return:
    '''
    # word=u'浙江大学医学院附属第一医院'
    # 带参数的get
    # r = http.request('get', 'http://www.baidu.com/s', fields={'wd': u'宁波市第六医院'}
    url='http://www.mingyihui.net/hospitalsearch_%s.html' %word
    page = http.request('get',url).data.decode()
    if re.search(r'/hospital_\d+\.html', page):
        index=re.search(r'\d+',re.search(r'/hospital_\d+\.html', page).group()).group()
        url_gk =u'http://www.mingyihui.net/hospital_%s.html' %index #概况
        url_xxjs = u'http://www.mingyihui.net/hospital_%s/index.html' % index  # 详细介绍
        url_ksjs = u'http://www.mingyihui.net/hospitalx_%s/departments.html' %index #科室介绍
        url_yykb = u'http://www.mingyihui.net/hospital_%s/comment.html' % index #医院口碑
    else:
        url_gk = u''
        url_xxjs = u''
        url_ksjs = u''
        url_yykb = u''
    return url_gk,url_xxjs,url_ksjs,url_yykb

def get_index_link(url,http):
    page=get_page(url,http)

if __name__ == '__main__':
    http=get_http()
    word=u'浙江大学医学院附属第一医院'
    url_gk,url_xxjs,url_ksjs,url_yykb=get_mingyihui_url(word,http)