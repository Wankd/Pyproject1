#coding:utf-8
import random,re
from pandas import DataFrame,Series


def str_to_int(word):
    try:
        return int(word)
    except:
        return re.split(',|;',word)[0].strip()


def read_data(path,str_,DISEASE_CODE):
    # path='C:\\Users\epsoft\Desktop\drgs2\juming.csv'
    fr=open(path,encoding='utf-8')
    lines=fr.readlines()
    i=0
    List_columns=[]
    List_body=[]
    for line in lines:
        i+=1
        line = re.sub('\"|\||\^','',line.strip())
        if i==1:
            List_columns=get_columns(line,str_)
        elif re.search('^[A-Z]\d{2}\.[x-y0-9]{3}',line.split(str_)[0]) and line.split(str_)[0] in DISEASE_CODE:
            List_body.append([str_to_int(data) for data in line.split(str_)])
        else:
            pass
    fr.close()
    return List_columns,List_body


def read_cizd(path,str_,DISEASE_CODE):
    # path='C:\\Users\epsoft\Desktop\drgs2\juming.csv'
    fr=open(path,encoding='utf-8')
    lines=fr.readlines()
    i=0
    List_columns=[]
    List_body=[]
    for line in lines:
        i+=1
        line = re.sub('\"|\||\^','',line.strip())
        if i==1:
            List_columns=get_columns(line,str_)
        elif re.search('^[A-Z]\d{2}\.[x-y0-9]{3}',line.split(str_)[0]) and line.split(str_)[0] in DISEASE_CODE and line.split(str_)[1] in DISEASE_CODE and line.split(str_)[1]!=line.split(str_)[0]:
            List_body.append([str_to_int(data) for data in line.split(str_)])
        else:
            pass
    fr.close()
    return List_columns,List_body


def get_columns(first_line,str_):
    '''
    传入数据，获取第一行
    :param first_line:
    :type first_line:str
    :param str_:
    :return:
    '''
    List=[]
    for word in first_line.split(str_):
        word=word.upper()
        List.append(word)
    return List

def get_DISEASE_CODE():
    '''
    获取主诊断数据
    :return:
    '''
    DISEASE_CODE={}
    path='C:\\Users\epsoft\Desktop\drgs2\DISEASE_CODE.txt'
    file=open(path,encoding='utf-8')
    for line in file.readlines():
        # DISEASE_CODE.append(line.strip())
        DISEASE_CODE[line.strip()]=None
    file.close()
    return DISEASE_CODE



def get_all_data():
    DISEASE_CODE = get_DISEASE_CODE()
    path_jm='C:\\Users\epsoft\Desktop\drgs2\juming.csv' #居民
    path_zg = 'C:\\Users\epsoft\Desktop\drgs2\zhigong.csv'  # 职工
    path_sbj = 'C:\\Users\epsoft\Desktop\drgs2\sbj.csv'  # 省本级
    path_yd = 'C:\\Users\epsoft\Desktop\drgs2\yd.csv'  # 异地
    List=[]
    jm_columns,jm_body=read_data(path_jm,';',DISEASE_CODE)
    zg_columns, zg_body = read_data(path_zg, ';',DISEASE_CODE)
    sbj_columns, sbj_body = read_data(path_sbj, ',',DISEASE_CODE)
    yd_columns, yd_body = read_data(path_yd, ',',DISEASE_CODE)
    List.extend([line for line in jm_body if len(line)==len(jm_columns)])
    List.extend([line for line in zg_body if len(line) == len(zg_columns)])
    List.extend([line for line in sbj_body if len(line) == len(sbj_columns)])
    List.extend([line for line in yd_body if len(line) == len(yd_columns)])
    return DataFrame(List,columns=jm_columns)



def get_cizd():
    DISEASE_CODE = get_DISEASE_CODE()
    shengbenji_cizd='C:\\Users\epsoft\Desktop\drgs2\shengbenji_cizd.csv' #省本级次诊断
    quansheng_cizd = 'C:\\Users\epsoft\Desktop\drgs2\quansheng_cizd.csv'  # 全省次诊断
    List=[]
    sbj_columns,sbj_body=read_cizd(shengbenji_cizd,',',DISEASE_CODE)
    qs_columns, qs_body = read_cizd(quansheng_cizd, ';',DISEASE_CODE)
    List.extend([line for line in sbj_body if len(line)==len(sbj_columns)])
    List.extend([line for line in qs_body if len(line) == len(qs_columns)])
    return DataFrame(List,columns=sbj_columns)



if __name__ == '__main__':
    pass
    # data=get_all_data()
    # data.groupby('AKC196').sum().to_csv('C:\\Users\epsoft\Desktop\drgs2\\all_data.csv',encoding='utf-8')
    cizd=get_cizd()
    new_data=cizd.groupby(['AKC196','CZD_']).sum()
    type(new_data)
    cizd.groupby(['AKC196','CZD_']).sum().to_csv('C:\\Users\epsoft\Desktop\drgs2\\cizd.csv', encoding='utf-8')
    # print(random.choice(sbj_body))