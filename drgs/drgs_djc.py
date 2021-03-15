#coding:utf-8
import pandas as pd
import random
from pandas import DataFrame,Series
import datetime

def get_akc196_list(data):
    '''
    获取排序后的akc916列表
    :param data:
    :return:
    '''
    new_data=data.sort_values(by="CNT",ascending=False)
    return [akc196 for akc196 in new_data['AKC196']]


def get_list(Array):
    sum_=0
    List=[]
    for i in Array:
        sum_=sum_+i+1
        List.append(sum_)
    return List

def get_list_czd(Array):
    sum_=0
    List=[]
    for i in Array:
        sum_=sum_+i
        List.append(sum_)
    return List


def get_akc196_dict(data):
    '''
    获取akc196的判断标准
    :param data:
    :type data:DataFrame
    :return:
    '''
    Dict={}
    for value in data.values:
        akc196=value[0]
        sex_list=get_list(value[2:3])
        age_list = get_list(value[4:15])
        zysc_list = get_list(value[16:27])
        amt_list = get_list(value[28:36])
        Dict[akc196]={'sex_list':sex_list,'age_list':age_list,'zysc_list':zysc_list,'amt_list':amt_list}
    return Dict



def get_akc196(akc196_list):
    '''
    随机选取akc196
    :param akc196_list:
    :return:
    '''
    num=random.randint(1,20)*1000
    return random.choice(akc196_list[0:num])



def get_sex(sex_list):
    '''
    根据分布获取性别
    :param sex_list:
    :return:
    '''
    sexList=['男','女']
    random_=random.randint(1,max(sex_list))
    i=0
    for num in sex_list:
        if random_<num:
            break
        else:
            i+=1
    return sexList[i]


def get_age(age_List):
    '''
    根据分布返回年龄
    :param age_List:
    :return:
    '''
    ageList=[0,random.randint(1,10),random.randint(11,20),random.randint(21,30),
                 random.randint(31, 40),random.randint(41,50),random.randint(51,60),random.randint(61,70),
                 random.randint(71, 80),random.randint(81,90),random.randint(91,100),random.randint(101,130)]
    random_ = random.randint(1, max(age_List))
    i = 0
    for num in age_List:
        if random_<num:
            break
        else:
            i+=1
    return ageList[i]



def get_zysc(zysc_list):
    '''
    根据分布返回住院时长
    :param zysc_list:
    :return:
    '''
    zyscList=[0,random.randint(1,3),random.randint(4,6),random.randint(7,10),
                 random.randint(11, 15),random.randint(16,25),random.randint(26,40),random.randint(41,60),
                 random.randint(61, 90),random.randint(91,180),random.randint(181,365),random.randint(366,1095)]
    random_ = random.randint(1, max(zysc_list))
    i = 0
    for num in zysc_list:
        if random_<num:
            break
        else:
            i+=1
    return zyscList[i]


def get_amt(amt_list):
    '''
    根据分布返回花费金额
    :param amt_list:
    :return:
    '''
    amtList=[random.randint(0,100),random.randint(100,300),random.randint(300,800),
             random.randint(800, 1500),random.randint(1500,5000),random.randint(5000,15000),
             random.randint(15000,50000),random.randint(50000, 200000),random.randint(200000,1000000)]
    random_ = random.randint(1, max(amt_list))
    i = 0
    for num in amt_list:
        if random_<num:
            break
        else:
            i+=1
    return amtList[i]+random.random()


def get_cizd_dict(data_cizd):
    '''
    获取次诊断字典
    :param data_cizd:
    :type data_cizd:DataFrame
    :return:
    '''
    Dict={}
    for value in data_cizd.values:
        akc196=value[0]
        czd_=value[1]
        cnt=value[2]
        if akc196 not in Dict:
            Dict[akc196]={'czd_':[],'cnt':[]}
        Dict[akc196]['czd_'].append(czd_)
        Dict[akc196]['cnt'].append(cnt)
    for akc196 in Dict:
        Dict[akc196]['cnt_']=get_list_czd(Dict[akc196]['cnt'])
    return Dict


def get_ong_czd(cdz_,cnt_):
    random_ = random.randint(1, max(cnt_))
    i = 0
    for num in cnt_:
        if random_ < num:
            break
        else:
            i += 1
    return cdz_[i]

def get_n_czd(n,cdz_,cnt_):
    i=1
    List=[]
    if i<=n:
        one_czd=get_ong_czd(cdz_,cnt_)
        if one_czd not in List:
            List.append(one_czd)
    return List

def get_diags_code(akc196,cizd_dict):
    try:
        i = random.random()
        akc196_czd=cizd_dict[akc196]
        cdz_=akc196_czd['czd_']
        cnt_=akc196_czd['cnt_']
        i=random.random()
        List=[]
        if i<=0.6:
            pass
        elif i<=0.80:
            List=get_n_czd(1,cdz_,cnt_)
        elif i<=0.93:
            List=get_n_czd(2,cdz_,cnt_)
        else:
            List = get_n_czd(3, cdz_, cnt_)
        return List
    except:
        return []

def get_data(akc196_list,all_akc196_dict,cizd_dict,opers_code):
    akc196=get_akc196(akc196_list) #DISEASE_CODE
    akc196_dict=all_akc196_dict[akc196]
    sex_list = akc196_dict['sex_list']
    age_list = akc196_dict['age_list']
    zysc_list = akc196_dict['zysc_list']
    amt_list = akc196_dict['amt_list']
    DISEASE_CODE=akc196 #主诊断
    TOTAL_EXPENSE=get_amt(amt_list) #花费金额
    AGE=get_age(age_list) # 年龄
    if AGE!=0:
        SF0100= -1
        SF0101= -1
        SF0102= -1
    else:
        SF0100 = random.randint(1,365)
        SF0101 = random.randint(3,10)
        SF0102 = SF0101+random.randint(1,5)
    GENDER=get_sex(sex_list) #性别
    ACCTUAL_DAYS=get_zysc(zysc_list) #住院天数
    SF0104 = -1 if random.random() <= 0.95 else random.randint(1, 200)
    SF0108 = -1 if random.random() <= 0.99 else 1
    B_WT4_V1_ID = 0
    diags_code=get_diags_code(akc196,cizd_dict)
    opers_code=get_opers_code(akc196,opers_code)
    return {'ACCTUAL_DAYS': ACCTUAL_DAYS, 'AGE': AGE, 'B_WT4_V1_ID': B_WT4_V1_ID, 'DISEASE_CODE': DISEASE_CODE,
            'GENDER': GENDER, 'SF0100': SF0100,
            'SF0101': SF0101, 'SF0102': SF0102, 'SF0104': SF0104, 'SF0108': SF0108, 'TOTAL_EXPENSE': TOTAL_EXPENSE,
            'diags_code': diags_code,'opers_code': opers_code}


def get_opers_codedata(path):
    '''
    获取手术编码
    :return:
    '''
    opers_code=[]
    # path='C:\\Users\epsoft\Desktop\正在工作\drgs\demo\opers_code.txt'
    file=open(path,encoding='utf-8')
    for line in file.readlines():
        data=line.strip()
        opers_code.append(data)
    file.close()
    return opers_code


def getopers(a,opers_code):
    code=random.choice(opers_code)
    code_=code[0:2]
    l=[code]
    if code_=='00' or code_=='17' or code_>='87':
        l=[code]
    elif a in ('D','I'):
        while code_<'35' or code_>'41':
            code = random.choice(opers_code)
            code_ = code[0:2]
        l = [code]
    elif a=='E':
        while code_ not in ('06','07'):
            code = random.choice(opers_code)
            code_ = code[0:2]
        l = [code]
    elif a == 'H':
        while code_<'08' or code_>'29' or (code_>'16' and code_<'21'):
            code = random.choice(opers_code)
            code_ = code[0:2]
        l = [code]
    elif a == 'K':
        while code_<'42' or code_>'45':
            code = random.choice(opers_code)
            code_ = code[0:2]
        l = [code]
    elif a == 'J':
        while code_<'30' or code_>'34':
            code = random.choice(opers_code)
            code_ = code[0:2]
        l = [code]
    elif a == 'L':
        while code_ in ('85','86'):
            code = random.choice(opers_code)
            code_ = code[0:2]
        l = [code]
    elif a == 'M':
        while code_<'76' or code_>'84':
            code = random.choice(opers_code)
            code_ = code[0:2]
        l = [code]
    elif a == 'N':
        while code_<'60' or code_>'71':
            code = random.choice(opers_code)
            code_ = code[0:2]
        l = [code]
    elif a == 'O':
        while code_<'72' or code_>'75':
            code = random.choice(opers_code)
            code_ = code[0:2]
        l = [code]
    return l


def get_opers_code(akc196,opers_code):
    i=random.random()
    a = akc196[0].upper()
    List=[]
    if i<=0.85:
        pass
    else:
        List=getopers(a,opers_code)
    return List


if __name__ == '__main__':
    path='C:\\Users\epsoft\Desktop\drgs2\\all_data.csv'
    data = pd.read_csv(path, encoding='utf-8') #疾病分析数据
    path_cizd='C:\\Users\epsoft\Desktop\drgs2\\cizd.csv' #
    data_cizd=pd.read_csv(path_cizd, encoding='utf-8')
    path_opers_code='C:\\Users\epsoft\Desktop\drgs2\\opers_code.txt'
    opers_code=get_opers_codedata(path_opers_code)
    akc196_list=get_akc196_list(data)
    all_akc196_dict=get_akc196_dict(data)
    cizd_dict=get_cizd_dict(data_cizd)
    i=0
    while i<=100:
        Dict=get_data(akc196_list,all_akc196_dict,cizd_dict,opers_code)
        print(Dict)
        i+=1
