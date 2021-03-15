#coding:utf-8
import pymysql,json,re
import xgboost as xgb
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
def get_code_Dict(path):
    Dict={}
    fr=open(path,encoding='utf-8')
    lines=fr.readlines()
    i=0
    for line in lines:
        word=line.strip()
        if word not in Dict:
            i+=1
            Dict[word]=i
    return Dict



def get_code():
    '''
    获取主诊断以及手术的编码
    :return:
    '''
    DISEASE_CODE_path='C:\\Users\epsoft\Desktop\drgs2\\xgboost_model\\DISEASE_CODE.txt'
    opers_code_path = 'C:\\Users\epsoft\Desktop\drgs2\\xgboost_model\\opers_code.txt'
    drg_code_path = 'C:\\Users\epsoft\Desktop\drgs2\\xgboost_model\\drg.txt'
    return get_code_Dict(DISEASE_CODE_path),get_code_Dict(opers_code_path),get_code_Dict(drg_code_path)



def get_conn():
    '''
    数据库连接
    :param database:
    :return:
    '''
    conn = pymysql.connect(
        host='192.168.101.46',user='root',password='root1',database='drgs',charset ='utf8',port=3306)
    cursor = conn.cursor()
    return conn,cursor


def get_df(data,DISEASE_CODEdict,opers_codedict,drg_dict):
    '''
    返回训练的数据
    :param data:
    :param DISEASE_CODEdict:
    :param opers_codedict:
    :return:
    '''
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
            label.append(drg_dict[drg])
        except:
            pass
    return dt,label,feature



def get_test_data(conn,cursor,DISEASE_CODEdict,opers_codedict,drg_dict):
    sql = '''select DISEASE_CODE,AGE,GENDER,ACCTUAL_DAYS,SF0100,SF0101,SF0102,SF0104,SF0108,TOTAL_EXPENSE,diags_code,opers_code,drg
               from dwd_drgs_result where date>="20190928" limit 100000'''
    cursor.execute(sql)
    data = cursor.fetchall()
    return get_df(data,DISEASE_CODEdict,opers_codedict,drg_dict)



def get_model(dt,label):
    # dt,label=train_dt, train_label
    dt = np.array(dt)
    # dt.shape
    # label.shape
    num_class=len(set(label))
    print(num_class)
    label = np.array(label)
    params  = {'objective': 'multi:softmax','num_class':num_class}
    dtrain_2class = xgb.DMatrix(dt, label=label)
    gbdt_03 = xgb.train(params , dtrain_2class, num_boost_round=3)
    # 训练三棵树的模型
    # pred=gbdt_03.predict(dtrain_2class)
    # print(gbdt_03.get_dump())
    return gbdt_03





def get_train_data(conn,cursor,DISEASE_CODEdict,opers_codedict,drg_dict):
    sql='''select DISEASE_CODE,AGE,GENDER,ACCTUAL_DAYS,SF0100,SF0101,SF0102,SF0104,SF0108,TOTAL_EXPENSE,diags_code,opers_code,drg
           from drgs_train_data2 limit 2000000'''
    cursor.execute(sql)
    data=cursor.fetchall()
    return get_df(data,DISEASE_CODEdict,opers_codedict,drg_dict)



def main():
    DISEASE_CODEdict,opers_codedict,drg_dict=get_code()
    conn,cursor=get_conn()
    train_dt, train_label, feature=get_train_data(conn,cursor,DISEASE_CODEdict,opers_codedict,drg_dict)
    model_1=get_model(train_dt,train_label)
    test_dt, test_label, feature = get_test_data(conn, cursor, DISEASE_CODEdict, opers_codedict, drg_dict)
    pred=model_1.predict(xgb.DMatrix(np.array(test_dt)))
    print(accuracy_score(test_label,pred))
    cursor.close()
    conn.close()



if __name__ == '__main__':
    main()
    # import xgboost as xgb
    # from sklearn.datasets import load_digits
    # #训练数据
    # digits_2class = load_digits(2)
    # X_2class = digits_2class['data']
    # y_2class = digits_2class['target']
    #
    # xgb_params_01 = {}
    # dtrain_2class = xgb.DMatrix(X_2class, label=y_2class)
    # gbdt_03 = xgb.train(xgb_params_01, dtrain_2class, num_boost_round=3)
    # #训练三棵树的模型
    # print(gbdt_03.get_dump())
    # #显示模型
    # gbdt_03a = xgb.train(xgb_params_01, dtrain_2class, num_boost_round=7, xgb_model=gbdt_03)
    # #在原模型基础上继续训练
    # print(gbdt_03a.get_dump())
    #
    # # main()
    # # get_corr(2000000)