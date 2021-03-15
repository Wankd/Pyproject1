#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/27 15:19
# @Author  : yhl
# @Software: PyCharm

import re
import time
import js2py
import random
import requests
from lxml import etree
import decimal
from decimal import Decimal

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    "Host": 'www.66ip.cn',
    # "Referer": 'http://www.66ip.cn/index.html',
    "Upgrade-Insecure-Requests": '1',
}

def get_521_content(url):
    req = requests.get(url=url, headers=headers)
    cookies = req.cookies
    cookies = '; '.join(['='.join(item) for item in cookies.items()])
    txt_521 = req.text
    txt_521 = ''.join(re.findall('<script>(.*?)</script>', txt_521))
    return (txt_521, cookies, req)


def fixed_fun(function,url):
    print(function)
    js = function.replace("<script>", "").replace("</script>", "").replace("{eval(", "{var my_data_1 = (")
    # print(js)
    # 使用js2py的js交互功能获得刚才赋值的data1对象
    context = js2py.EvalJs()
    context.execute(js)
    js_temp = context.my_data_1
    print(js_temp)
    index1 = js_temp.find("document.")
    index2 = js_temp.find("};if((")
    js_temp = js_temp[index1:index2].replace("document.cookie", "my_data_2")
    new_js_temp = re.sub(r'document.create.*?firstChild.href', '"{}"'.format(url), js_temp)
    # print(new_js_temp)
    # print(type(new_js_temp))
    context.execute(new_js_temp)
    data = context.my_data_2
    # print(data)
    __jsl_clearance = str(data).split(';')[0]
    return __jsl_clearance


def get_66daili(url):
    txt_521, cookies, req = get_521_content(url)
    print(req.status_code)
    if req.status_code == 521:
        __jsl_clearance = fixed_fun(txt_521,url)
        headers['Cookie'] = __jsl_clearance + ';' + cookies
        res1 = requests.get(url=url, headers=headers)
    else:
        res1 = req
    res1.encoding = 'gb2312'
    html = etree.HTML(res1.text)
    tr_list = html.xpath('//table//tr')
    for num, tr in enumerate(tr_list, 1):
        proxy_ip_dict = {}
        if num != 1:
            proxy_ip_dict['proxy_ip'] = ''.join(tr.xpath('.//td[1]/text()'))
            proxy_ip_dict['proxy_port'] = ''.join(tr.xpath('.//td[2]/text()'))
            proxy_ip_dict['proxy_local'] = ''.join(tr.xpath('.//td[3]/text()'))
            proxy_ip_dict['proxy_anonymous'] = ''.join(tr.xpath('.//td[4]/text()'))
            print(proxy_ip_dict)  #proxy_type 网页没有,自己添加+代理检测


def main():
    for i in range(1, 2000):
        get_66daili('http://www.66ip.cn/%s.html' % (i))


if __name__ == '__main__':
    a=Decimal(41063)
    b=int(a)
    type(a)=='int'
    isinstance (a,Decimal)