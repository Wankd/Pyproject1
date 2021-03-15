#coding:utf-8

import re

def get_data():
    List=[]
    file=open('C:\pycharmproject\\venv37\data_sub\yibao_data\data2.txt',encoding='utf-8')
    lines=file.readlines()
    for line in lines:
        str_=line.strip()
        if re.search(r'第\d+章',str_) or re.search(r'^附录',str_):
            new_str='|-'+str_+'\n'
        elif re.search(r'^[\u4e00-\u9fa5]',str_) and re.search(r'[A-Z]\d{2}-[A-Z]\d{2}',str_):
            new_str='|---'+str_+'\n'
        elif re.search(r'^[A-Z]\d{2}\s[\u4e00-\u9fa5]+',str_):
            new_str='|-----'+str_+'\n'
        elif re.search(r'^[A-Z]\d{2}\.\d\s[\u4e00-\u9fa5]+',str_) or re.search(r'^[A-Z]\d{2}\.\d\*\s[\u4e00-\u9fa5]+',str_) or re.search(r'^[A-Z]\d{2}\.\d\+\s[\u4e00-\u9fa5]+',str_) or re.search(r'^[A-Z]\d{2}\*\s[\u4e00-\u9fa5]+',str_):
            new_str='|-------'+str_+'\n'
        elif re.search(r'^[A-Z]\d{2}\.\d{3}x\d+',str_) or re.search(r'^[A-Z]\d{2}\.x\d{2}x\d+',str_) :
            new_str='|-----------'+str_+'\n'
        else:
            new_str='|---------' + str_+'\n'
        List.append(new_str)
    file.close()
    file_handle = open('C:\\Users\epsoft\Desktop\\icd10.txt', mode='w',encoding='utf-8')
    file_handle.writelines(List)
    file_handle.close()


def get_data2():
    List=[]
    file=open('C:\pycharmproject\\venv37\data_sub\yibao_data\data_2_2.txt',encoding='utf-8')
    lines=file.readlines()
    for line in lines:
        str_=line.strip()
        if str_=='':
            continue
        elif re.search('^\d{1,2}\s[\u4e00-\u9fa5]+',str_):
            new_str='|-'+str_+'\n'
        elif re.search('^[\u4e00-\u9fa5]+',str_):
            new_str='|---'+str_+'\n'
        elif re.search('^\d{2}\.\d\s[\u4e00-\u9fa5]+',str_):
            new_str = '|-----' + str_ + '\n'
        elif re.search('^\d{2}\.\d{2}\s[\u4e00-\u9fa5]+',str_):
            new_str = '|-------' + str_ + '\n'
        else:
            new_str = '|---------' + str_ + '\n'
        List.append(new_str)
    file.close()
    file_handle = open('C:\\Users\epsoft\Desktop\\icd9-cm3医保版.txt', mode='w',encoding='utf-8')
    file_handle.writelines(List)
    file_handle.close()


def get_data3():
    List=[]
    file=open('C:\pycharmproject\\venv37\data_sub\yibao_data\data_2_3.txt',encoding='utf-8')
    lines=file.readlines()
    for line in lines:
        str_=line.strip()
        if str_=='':
            continue
        elif re.search('^[A-Z]{2}\s[\u4e00-\u9fa5]+',str_):
            new_str='|-'+str_+'\n'
        elif re.search('^^[A-Z]{3}\s[\u4e00-\u9fa5]+',str_):
            new_str='|---'+str_+'\n'
        else:
            new_str = '|-----' + str_ + '\n'
        List.append(new_str)
    file.close()
    file_handle = open('C:\\Users\epsoft\Desktop\\中医疾病分类与代码.txt', mode='w',encoding='utf-8')
    file_handle.writelines(List)
    file_handle.close()


def get_data4():
    List=[]
    file=open('C:\pycharmproject\\venv37\data_sub\yibao_data\data_2_4.txt',encoding='utf-8')
    lines=file.readlines()
    for line in lines:
        str_=line.strip()
        if str_=='':
            continue
        elif re.search('^[A-Z]{2}\s[\u4e00-\u9fa5]+',str_):
            new_str='|-'+str_+'\n'
        elif re.search('^^[A-Z]{3}\s[\u4e00-\u9fa5]+',str_):
            new_str='|---'+str_+'\n'
        else:
            new_str = '|-----' + str_ + '\n'
        List.append(new_str)
    file.close()
    file_handle = open('C:\\Users\epsoft\Desktop\\中医症候分类与代码.txt', mode='w',encoding='utf-8')
    file_handle.writelines(List)
    file_handle.close()


if __name__ == '__main__':
    get_data4()