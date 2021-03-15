#incoding:utf-8
import pymysql

def get_data(table_name,table_name_2,n):
    conn = pymysql.connect(host='localhost', user='root', password='root1', database='test', charset='utf8', port=3306)
    cursor = conn.cursor()
    conn2 = pymysql.connect(host='10.85.159.7', user='wankeda', password='WanKeDa123', database='dpplot', charset='utf8', port=3306)
    cursor2 = conn2.cursor()
    sql='select * from %s' %table_name
    cursor.execute(sql)
    data = cursor.fetchall()
    i=0
    for line in data:
        l=[]
        for j in line:
            l.append(j)
        sql2='''insert into %s values %s''' %(table_name_2,str(tuple(l)))
        print(sql2)
        cursor2.execute(sql2)
        i += 1
        if i >= n:
            conn2.commit()
            i = 0
    conn2.commit()
    cursor.close()
    conn.close()
    cursor2.close()
    conn2.close()


def save_hz():
    conn2 = pymysql.connect(host='10.85.159.7', user='wankeda', password='WanKeDa123', database='dpplot',
                            charset='utf8', port=3306)
    cursor2 = conn2.cursor()
    path='C:\pycharmproject\\venv37\data_sub\yiqing_data\杭州.csv'
    fr=open(path,encoding='utf-8')
    lines=fr.readlines()
    i=0
    for line in lines:
        i+=1
        if i>2:
            sql='insert into dwd_yqfx_hzdt values %s' % str(tuple(line.strip().split(',')))
            print(sql)
            cursor2.execute(sql)
    conn2.commit()
    fr.close()
    cursor2.close()
    conn2.close()



if __name__ == '__main__':
    get_data('data_mx','dwd_yqfx_mxdt',1000)
    get_data('data_qg', 'dws_yqfx_qgdt', 1000)
    get_data('data_qx', 'dwd_yqfx_qxdt', 1000)
