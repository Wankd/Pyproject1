#coding:utf-8
import pymysql,json,re
import numpy as np
import scipy as spy
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree.export import export_text
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from pandas import DataFrame,Series
import seaborn as sns

def get_code(data):
    '''
    获取数据编码
    :param data:
    :return:
    '''
    DISEASE_CODEdict={}
    DISEASE_CODElist=[]
    opers_codelist=[]
    for line in data:
        DISEASE_CODE=line[0]
        diags_code = re.sub('''\[|\]|\'|\"''', '', line[10])
        opers_code = re.sub('''\[|\]|\'|\"''', '', line[11])
        DISEASE_CODElist.append(DISEASE_CODE)
        DISEASE_CODElist.extend(re.split(',',diags_code) if diags_code!='' else [])
        if opers_code!='':
            opers_codelist.append(opers_code)
    DISEASE_CODElist=list(set(DISEASE_CODElist))
    opers_codelist = list(set(opers_codelist))
    DISEASE_CODElist.sort()
    opers_codelist.sort()
    return get_code_dict(DISEASE_CODElist),get_code_dict(opers_codelist)


def get_code_dict(List):
    Dict={}
    i=1
    for word in List:
        Dict[word]=i
        i+=1
    return Dict


def get_df(data,DISEASE_CODEdict,opers_codedict):
    '''
    返回训练的数据
    :param data:
    :param DISEASE_CODEdict:
    :param opers_codedict:
    :return:
    '''
    if opers_codedict is None and DISEASE_CODEdict is None:
        DISEASE_CODEdict,opers_codedict=get_code(data)
    # DISEASE_CODEdict=get_code_dict(DISEASE_CODElist)
    # opers_codedict=get_code_dict(opers_codelist)
    feature = ['DISEASE_CODE','age', 'sex_name', 'ACCTUAL_DAYS',
               'SF0100', 'SF0101', 'SF0102', 'SF0104', 'SF0108',
               'TOTAL_EXPENSE','czz_1','czz_2','czz_3','opers_code']
    dt=[]
    label=[]
    print(1)
    for line in data:
        try:
            DISEASE_CODE=DISEASE_CODEdict[line[0]]
            age=int(line[1])
            sex_name=1 if line[2]==u'男' else 0
            ACCTUAL_DAYS=int(line[3])
            SF0100=int(line[4])
            SF0101 = int(line[5])
            SF0102 = int(line[6])
            SF0104 = int(line[7])
            SF0108 = int(line[8])
            TOTAL_EXPENSE=float(line[9])
            diags_code = re.sub('''\[|\]|\'|\"''', '', line[10])
            opers_code = re.sub('''\[|\]|\'|\"''', '', line[11])
            if diags_code=='':
                czz_1 = 0
                czz_2 = 0
                czz_3 = 0
            elif len(re.split(',',diags_code))==1:
                czz_1=DISEASE_CODEdict[re.split(',',diags_code)[0]]
                czz_2 = 0
                czz_3 = 0
            elif len(re.split(',',diags_code))==2:
                czz_1 = DISEASE_CODEdict[re.split(',', diags_code)[0]]
                czz_2 = DISEASE_CODEdict[re.split(',', diags_code)[1]]
                czz_3 = 0
            elif len(re.split(',', diags_code)) == 3:
                czz_1 = DISEASE_CODEdict[re.split(',', diags_code)[0]]
                czz_2 = DISEASE_CODEdict[re.split(',', diags_code)[1]]
                czz_3 = DISEASE_CODEdict[re.split(',', diags_code)[2]]
            else:
                czz_1 = 0
                czz_2 = 0
                czz_3 = 0
            if opers_code=='':
                opers_code = 0
            elif len(re.split(',', opers_code)) == 1:
                opers_code=opers_codedict[opers_code]
            else:
                opers_code = 0
            drg=line[12]
            dt.append([DISEASE_CODE, age, sex_name, ACCTUAL_DAYS,
                         SF0100, SF0101, SF0102, SF0104, SF0108,
                         TOTAL_EXPENSE, czz_1, czz_2, czz_3, opers_code])
            label.append(drg)
        except:
            pass
    return DISEASE_CODEdict,opers_codedict,dt,label,feature


def get_train_data(lineNum):
    '''
    数据库连接，获取训练数据
    :param database:
    :return:
    '''
    conn = pymysql.connect(
        host='192.168.101.49',user='root',password='root1',database='drgs',charset ='utf8',port=3306)
    cursor = conn.cursor()
    sql='''select DISEASE_CODE,AGE,GENDER,ACCTUAL_DAYS,SF0100,SF0101,SF0102,SF0104,SF0108,TOTAL_EXPENSE,diags_code,opers_code,drg
           from dwd_drgs_result where date='20190909' and drg!='' and DISEASE_CODE!='' limit %s''' %lineNum
    cursor.execute(sql)
    DISEASE_CODEdict,opers_codedict,data,label,feature=get_df(cursor.fetchall(),None,None)
    cursor.close()
    conn.close()
    return  DISEASE_CODEdict,opers_codedict,data,label,feature
    # return DataFrame(data,columns=feature)


def get_test_data(lineNum,DISEASE_CODEdict,opers_codedict):
    '''
    数据库连接，获取测试数据
    :param database:
    :return:
    '''
    conn = pymysql.connect(
        host='192.168.101.49',user='root',password='root1',database='drgs',charset ='utf8',port=3306)
    cursor = conn.cursor()
    sql='''select DISEASE_CODE,AGE,GENDER,ACCTUAL_DAYS,SF0100,SF0101,SF0102,SF0104,SF0108,TOTAL_EXPENSE,diags_code,opers_code,drg
           from dwd_drgs_result where date='20190910' and drg!='' and DISEASE_CODE!='' limit %s''' %lineNum
    cursor.execute(sql)
    DISEASE_CODEdict,opers_codedict,data,label,feature=get_df(cursor.fetchall(),DISEASE_CODEdict,opers_codedict)
    cursor.close()
    conn.close()
    return  data,label


def save_model(data,label):
    print(u'建立模型')
    clf = DecisionTreeClassifier(max_depth=19)
    # clf.fit(X_train,y_train)
    clf.fit(data, label)
    joblib.dump(clf, "C:\\Users\epsoft\Desktop\drgs2\\drgs_model\\train_model.m")


def load_model():
    '''
    加载模型
    :return:
    '''
    path="C:\\Users\epsoft\Desktop\drgs2\\drgs_model\\train_model.m"
    clf=joblib.load(path)
    return clf


def get_model(lineNum):
    '''
    建立模型
    :param lineNum:
    :return:
    '''
    DISEASE_CODEdict, opers_codedict, data, label, feature = get_train_data(lineNum)
    save_model(data,label)
    clf=load_model()
    return DISEASE_CODEdict,opers_codedict,clf,feature


def print_model(clf,feature):
    '''
    打印决策树
    :param clf: 
    :return: 
    '''
    import sys
    sys.setrecursionlimit(1000000)
    r = export_text(clf, feature_names=feature, max_depth=19)
    print(r)


def print_err(lineNum_test,DISEASE_CODEdict,opers_codedict,clf):
    '''
    打印模型准确性
    :param lineNum_test: 
    :param DISEASE_CODEdict: 
    :param opers_codedict: 
    :param clf: 
    :return: 
    '''
    X_test, y_test = get_test_data(lineNum_test, DISEASE_CODEdict, opers_codedict)
    j = 0
    for i in range(len(X_test)):
        line=X_test[i]
        y=clf.predict([line])
        if y_test[i]==y:
            j+=1
    print(j/len(y_test))


def save_dict(DISEASE_CODEdict,opers_codedict):
    '''
    存储编码
    :param DISEASE_CODEdict: 
    :param opers_codedict: 
    :return: 
    '''
    DISEASE_CODE_path='C:\\Users\epsoft\Desktop\drgs2\\drgs_model\\DISEASE_CODE.csv'
    opers_code_path = 'C:\\Users\epsoft\Desktop\drgs2\\drgs_model\\opers_code.csv'
    DISEASE_CODElist=[]
    opers_codelist=[]
    for DISEASE_CODE in DISEASE_CODEdict:
        DISEASE_CODElist.append([DISEASE_CODE,DISEASE_CODEdict[DISEASE_CODE]])
    for opers_code in opers_codedict:
        opers_codelist.append([opers_code,opers_codedict[opers_code]])
    DataFrame(DISEASE_CODElist,columns=[u'疾病编码','疾病id']).to_csv(DISEASE_CODE_path,encoding='utf-8')
    DataFrame(opers_codelist, columns=[u'手术编码', '手术id']).to_csv(opers_code_path, encoding='utf-8')


def get_corr(lineNum):
    '''
    获取相关系数图
    :param lineNum:
    :return:
    '''
    Df = get_train_data(lineNum)
    data = Df.corr()  # test_feature => pandas.DataFrame#
    sns.heatmap(data)
    plt.show()

def main():
    lineNum=2000000
    lineNum_test=int(lineNum*0.3)
    DISEASE_CODEdict,opers_codedict,clf,feature=get_model(lineNum)
    # X_train, X_test, y_train, y_test =train_test_split(data,label,test_size=0.3, random_state=0)
    print_err(lineNum_test,DISEASE_CODEdict,opers_codedict,clf)
    print_model(clf,feature)
    save_dict(DISEASE_CODEdict,opers_codedict)


if __name__ == '__main__':
    main()
    # get_corr(2000000)