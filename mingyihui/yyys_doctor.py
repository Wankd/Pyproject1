#coding:utf-8
import re
from bs4 import BeautifulSoup


def get_doctor_name(soup):
    '''
    获取医师姓名
    :param sopu:
    :type soup:BeautifulSoup
    :return :'zc':职称,'sf':身份,'pm':排名','doctor_name':姓名
    '''
    Dict={'doctor_name':'','zc': '', 'sf': '', 'pm': ''}
    class_str=soup.select('.doctorName')[0].get_text()
    List=re.split('\n\n',class_str)
    Dict['doctor_name']=re.sub('\n','',List[0])
    doctor_info = re.sub('\n', '', List[1])
    _str = ''
    i = 0
    for word in re.split('\s+',doctor_info):
        if i == 0 and (u'医师'  in word or u'教授' in word):
            Dict['zc'] = word
        elif u'领先' in word:
            Dict['pm'] = word
        else:
            i += 1
            _str = _str + ' ' + word
    Dict['sf'] = _str.strip()
    return Dict

def get_soup(page):
    '''
    传入数据，css解析http
    :param page:
    :return:
    '''
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def get_msg(soup):
    '''
    获取医师出诊地点，擅长领域，执业经历等信息
    :param soup:
    :type soup:BeautifulSoup
    :return:'czdd':出诊地点,'scly':擅长领域,'zyjl':执业经历
    '''
    Dict={'czdd':'','scly':'','zyjl':''}
    class_list=soup.select('.doctortail')
    for class_str in class_list:
        str_ = class_str.get_text()
        if u'出诊地点' in str_:
            Dict['czdd']=re.sub('出诊地点：|\n','',str_)
        if u'擅长领域' in str_:
            Dict['scly']=re.sub('擅长领域：|\n','',str_)
        if u'执业经历' in str_:
            Dict['zyjl']=re.sub('\n','',re.split('\n\n',re.sub('\n执业经历：\n','',str_))[0])
    return Dict

def get_comment(soup):
    '''
    获取医师的评价数据
    :return:all:全部,a:非常满意,b:满意,c:一般,d:不满意
    '''
    commemt_dict={'all':'','a':'','b':'','c':'','d':''}
    soup_comment_tag = soup.select('.serviceRecommen_l')[4]
    for tag_str in soup_comment_tag.find_all('dd'):
        str_=tag_str.get_text()
        # print(str_)
        if re.search('全部（\d+）',str_):
            commemt_dict['all']=re.search('\d+',str_).group()
        if re.search('非常满意（\d+）',str_):
            commemt_dict['a']=re.search('\d+',str_).group()
        if re.search('满意（\d+）',str_):
            commemt_dict['b']=re.search('\d+',str_).group()
        if re.search('一般（\d+）',str_):
            commemt_dict['c']=re.search('\d+',str_).group()
        if re.search('不满意（\d+）',str_):
            commemt_dict['d']=re.search('\d+',str_).group()
    return commemt_dict

def get_pingfen(soup):
    '''
    获取医师评分数据
    :param soup:
    :type soup:BeautifulSoup
    :return:zhpf:综合评分,xsf:学术地位,cgf:学术成果,pjf:患者评价,zcf:平台/职称
    '''
    pingfen_dict={'zhpf':'','xsf':'','cgf':'','pjf':'','zcf':''}
    soup_pingfen_tag = soup.select('.serviceRecommen_l')[1]
    pingfen_dict['zhpf']=re.search('\d+',soup_pingfen_tag.h3.get_text()).group()
    string=''
    for pingfen_str in soup_pingfen_tag.find_all('p'):
        str_=pingfen_str.get_text()
        # print(str_)
        if str_ in (u'学术地位',u'学术成果',u'患者评价',u'平台/职称'):
            string=str_
        if re.sub('\d+','',str_)=='' or u'暂无评分'==str_:
            if string==u'学术地位':
                pingfen_dict['xsf']=str_
            if string==u'学术成果':
                pingfen_dict['cgf']=str_
            if string==u'患者评价':
                pingfen_dict['pjf']=str_
            if string==u'平台/职称':
                pingfen_dict['zcf']=str_
    return pingfen_dict


def get_doctor_msg2(soup):
    '''
    传入医师页面数据
    :param page:
    :return:
    '''
    soup=get_soup(page)
    comment = get_comment(soup)
    pingfen = get_pingfen(soup)
    Dict = {'comment': comment, 'pingfen': pingfen}
    Dict.update(get_doctor_name(soup))
    Dict.update(get_msg(soup))
    return Dict


def get_doctor_msg(page,kesi_name_1,word):
    '''
    传入医师页面数据
    :param page:
    :return:
    '''
    soup=get_soup(page)
    comment=get_comment(soup)
    pingfen=get_pingfen(soup)
    Dict={'comment':comment,'pingfen':pingfen,'kesi_name_1':kesi_name_1,'word':word}
    Dict.update(get_doctor_name(soup))
    Dict.update(get_msg(soup))
    return Dict


