#coding:utf-8
import re
#采集医院介绍数据
#[\u4E00-\u9FA5]+

def get_name(name_str):
    return re.search(r'[\u4E00-\u9FA5]+',name_str).group()

def get_index(index_str):
    pattern = re.compile(r'[\u4E00-\u9FA5]+')
    return ','.join(pattern.findall(index_str))

def get_word(string_):
    return re.sub(r'<[^/]+>|<.+>','',string_)

def get_qtxx(qtxx_srt):
    '''
    获取医院其他信息
    :param qtxx_srt:
    :type qtxx_srt:list
    :return:
    '''
    Dict={u'bc':'',u'pm':'',u'dz':'',u'dh':'',u'jj':''}
    # List=[u'别称：',u'2017年复旦版全国医院综合排名',u'地址：',u'电话：',u'简介：']
    for string_ in qtxx_srt:
        word=get_word(string_)
        if u'别称：' in word:
            Dict[u'bc']=re.sub('别称：','',word)
            continue
        if u'2017年复旦版全国医院综合排名' in word:
            Dict[u'pm']=word
            continue
        if u'地址：' in word:
            Dict[u'dz']=re.sub('地址：','',word)
            continue
        if u'电话：' in word:
            Dict[u'dh']=re.sub('电话：','',word)
            continue
        if u'简介：' in word:
            Dict[u'jj']=re.sub('简介：','',word)
            continue
    return Dict

def get_gk(page,word):
    '''
    传入概况源代码，获取医院详情
    :param url_gk:
    :param http:
    :return:
    '''
    pattern = re.compile(r'<p class=\"doctortailTitle(?:(?:\s|[a-zA-Z])+\"|\")>.+</p>')
    qtxx_str=pattern.findall(page)
    try:
        name_str=re.search(r'<h1>[\u4E00-\u9FA5]+</h1>',page).group()
    except:
        name_str=word
    index_str = re.search(r'(<li>[\u4E00-\u9FA5]+</li>\s+)+', page).group()
    Dict=get_qtxx(qtxx_str)
    Dict['name']=get_name(name_str)
    Dict['lx']=get_index(index_str)
    Dict['word']=word
    return Dict