#coding:utf-8
import pymysql
from datetime import datetime,timedelta
from time import sleep


def select_data(lineNum,date_,Dict,cursor):
    List=[]
    i=0
    for line in cursor:
        i+=1
        drg=line[12]
        if drg not in Dict:
            Dict[drg]=0
        if Dict[drg]<10000:
            Dict[drg] =Dict[drg] +1
            List.append(line)
        else:
            pass
    if i==1000000:
        lineNum=lineNum+1000000
        date_=date_
    else:
        lineNum=0
        date_=(datetime.strptime(date_,'%Y%m%d')+timedelta(hours=24)).strftime('%Y%m%d')
    return List,Dict,lineNum,date_


def get_train_data():
    '''
    数据库连接，获取测试数据
    :param database:
    :return:
    '''
    conn = pymysql.connect(
        host='192.168.101.46',user='root',password='root1',database='drgs',charset ='utf8',port=3306)
    cursor = conn.cursor()
    date_='20190902'
    lineNum=0
    Dict={}
    min_Dict_value=0
    sql='''select DISEASE_CODE,AGE,GENDER,ACCTUAL_DAYS,SF0100,SF0101,SF0102,SF0104,SF0108,TOTAL_EXPENSE,diags_code,opers_code,drg
           from dwd_drgs_result where date='%s' and DISEASE_CODE!='' limit %s,1000000''' %(date_,lineNum)
    cursor.execute(sql)
    print(sql)
    while len(Dict)<=208 and min_Dict_value<10000 and date_<='20191105':
        List,Dict,lineNum,date_=select_data(lineNum,date_,Dict,cursor)
        if len(Dict)>0:
            min_Dict_value=min(Dict.values())
        print('%s --- %s --- %s --- %s'%(len(Dict),min_Dict_value,date_,len(List)))
        i=0
        if len(List)>0:
            for line in List:
                insert_sql='''insert into drgs_train_data2 values %s''' %(line,)
                i+=1
                cursor.execute(insert_sql)
                if i>=50000:
                    print(line)
                    conn.commit()
                    i=0
            conn.commit()
        sql = '''select DISEASE_CODE,AGE,GENDER,ACCTUAL_DAYS,SF0100,SF0101,SF0102,SF0104,SF0108,TOTAL_EXPENSE,diags_code,opers_code,drg
                   from dwd_drgs_result where date='%s' and drg!='' and DISEASE_CODE!='' limit %s,1000000''' % (date_, lineNum)
        cursor.execute(sql)
        print(sql)
        sleep(60)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    get_train_data()