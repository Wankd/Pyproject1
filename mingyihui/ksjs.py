#coding:utf-8
#采集科室数据，以及科室对应的url
import re

def get_word(string_):
    return re.sub(r'<[^\u4E00-\u9FA5]+>|<.+>','',string_)

def get_link(kesi_link,word):
    '''
    传入科室数据，获取科室连接
    :param kesi_link:
    :type kesi_link:str
    :return:
    '''
    List=[]
    kesi_name=re.search('[\u4E00-\u9FA5]+',re.search(r'<span>[\u4E00-\u9FA5]+:</span>',kesi_link).group()).group()
    pattern=re.compile('<a href=\"[^\s]+\">[^\s]+</a>')
    kesi_link_=pattern.findall(kesi_link)
    for kesi_str in kesi_link_:
        Dict = {}
        kesi_name_1=get_word(kesi_str)
        kesi_renshu=re.search(r'\d+',kesi_name_1).group()
        kesi_name_1=re.sub(r'（\d+人）','',kesi_name_1)
        kesi_link_1=re.sub(r'href=\"','',re.search(r'href=\"[^\"]+',kesi_str).group())
        Dict[u'kesi_name']=kesi_name
        Dict[u'kesi_name_1'] = kesi_name_1
        Dict[u'kesi_link_1'] ='http://www.mingyihui.net/'+kesi_link_1
        Dict[u'kesi_renshu']=kesi_renshu
        Dict[u'word'] = word
        List.append(Dict)
        # print(Dict)
    return List




def get_ksjs_link(page,wrod):
    '''
    传入科室介绍网页数据，自动解析，返回字典数据
    :param page:
    :return:
    '''
    # http_pt=u'http://www.mingyihui.net/'
    List=[]
    pattern=re.compile('<span>[\u4E00-\u9FA5]+:</span>\s+<dl>(?:\s+<a .+>)+\s+</dl>')
    kesi_link_lsit=pattern.findall(page)
    for kesi_link in kesi_link_lsit:
        # print(kesi_link)
        List_=get_link(kesi_link,wrod)
        List.extend(List_)
    return List