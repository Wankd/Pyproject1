#coding:utf-8
import pymysql



def jiexi_dict(Dict):
    '''
    解析采集到的字典数据
    :param Dict:
    :type Dict:dict
    :return:
    '''
    key_list=[]
    value_list=[]
    for key in Dict:
        value=pymysql.escape_string(str(Dict[key]))
        key_list.append('`%s`' %key)
        value_list.append('"%s"' % value)
    return key_list,value_list


def get_createtable_body(zhushi):
    body_list=[]
    for key in zhushi:
        if key in ('zyjl','scly'):
            body_str = '`%s` TEXT NOT NULL COMMENT "%s"' % (key, zhushi[key])
        else:
            body_str='`%s` VARCHAR(200) NOT NULL COMMENT "%s"' % (key,zhushi[key])
        body_list.append(body_str)
    # print(','.join(body_list))
    return ','.join(body_list)


def get_conn(database):
    '''
    获取连接
    :param database:
    :return:
    '''
    conn = pymysql.connect(
        host='localhost', user='root', password='root1', database=database, charset='utf8', port=3306)
    cursor = conn.cursor()
    return conn, cursor


def get_insert(tablename1,Dict):
    key_list,value_list=jiexi_dict(Dict)
    sql='''insert into %s(%s) values(%s)''' %(tablename1,','.join(key_list),','.join(value_list))
    return sql


def insert_List(tablename1,List,n,cursor,conn):
    i=0
    for Dict in List:
        sql=get_insert(tablename1,Dict)
        # print(sql)
        cursor.execute(sql)
        i+=1
        if i>=n:
            conn.commit()
            i=0
    conn.commit()

def create_table(tablename1,tablename2,zhushi,cursor,conn):
    '''
    根据采集到的字典数据，进行数据表的创建
    :param tablename_dict: 所要创建的数据表名{'table':'数据表1'}
    :param zhushi: 字段注释dict
    :param Dict: 采集的数据字典
    :param conn: 连接器
    :return:
    '''
    sql='''CREATE TABLE `%s` (%s) COMMENT="%s"'''%(tablename1,get_createtable_body(zhushi),tablename2)
    cursor.execute(sql)
    conn.commit()

def save_result(List,n,tablename1,tablename2,zhushi,conn,cursor):
    try:
        create_table(tablename1,tablename2,zhushi,cursor,conn)
    except:
        pass
    insert_List(tablename1,List,n,cursor,conn)

def sava_pt_ip(List,n,conn,cursor):
    zhushi_ptip={'ptip':'普通ip','label':'有效性','ctime':'采集时间'}
    tablename_ptip, tablename_ptip_2 = 'ptip_msg', '采集到的普通ip信息'
    return save_result(List, n, tablename_ptip, tablename_ptip_2, zhushi_ptip, conn, cursor)


def save_hdf_hos_link(List,n,conn,cursor):
    zhushi_hdf_hos_link = {'hos_name':'医院名称','hos_link':'医院url','diqu':'医院所在地区','zt':'采集状态'}
    tablename_1, tablename_2 = 'hdf_hos_link', '好大夫医师链接信息以及采集状态表'
    return save_result(List, n, tablename_1, tablename_2, zhushi_hdf_hos_link, conn, cursor)


def insert_Dict(tablename1,Dict,cursor,conn):
    sql=get_insert(tablename1,Dict)
    cursor.execute(sql)
    conn.commit()


def update_(sql,cursor,conn):
    cursor.execute(sql)
    conn.commit()


def check_(tablename1,cursor,conn):
    sql='''select * from %s where zt=""''' %tablename1
    cursor.execute(sql)
    conn.commit()
    data=cursor.fetchall()
    if len(data)>0:
        label=False
    else:
        label=True
    return label
