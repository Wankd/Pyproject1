#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\mingyihui")
import pymysql
from daili_ip import get_pt_ip_list,getheaders
from time import sleep
import requests

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
    # data=cursor.fetchone()
    conn.commit()


def insert_data(tablename1,List,n,cursor,conn):
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


def get_insert(tablename1,Dict):
    key_list,value_list=jiexi_dict(Dict)
    sql='''insert into %s(%s) values(%s)''' %(tablename1,','.join(key_list),','.join(value_list))
    return sql




def get_conn(database):
    conn = pymysql.connect(
        host='localhost',user='root',password='root1',database=database,charset ='utf8',port=3306)
    cursor = conn.cursor()
    return conn,cursor


def save_result(List,n,tablename1,tablename2,zhushi,conn,cursor):
    try:
        create_table(tablename1,tablename2,zhushi,cursor,conn)
    except:
        pass
    insert_data(tablename1,List,n,cursor,conn)


def save_hospital_msg(List,n,conn,cursor):
    '''
    存储医院信息数据
    :param List:
    :param n:
    :param conn:
    :param cursor:
    :return:
    '''
    zhushi_gk = {'bc': '医院别称', 'pm': '排名', 'dz': '地址', 'dh': '电话', 'jj': '简介', 'name': '医院名称', 'lx': '医院类型','word':'搜索医院名'}
    tablename_gk, tablename_gk_2= 'hospital_msg', '医院基础信息'
    return save_result(List,n,tablename_gk,tablename_gk_2,zhushi_gk,conn,cursor)

def save_ksjs_msg(List,n,conn,cursor):
    '''
    存储医院科室数据
    :param List:
    :param n:
    :param conn:
    :param cursor:
    :return:
    '''
    zhushi_ksjs = {'kesi_name': '科室大类', 'kesi_name_1': '科室小类', 'kesi_link_1': '科室连接', 'kesi_renshu': '科室人数', 'word': '搜索医院名'}
    tablename_ksjs, tablename_ksjs_2= 'ksjs_msg', '医院科室信息'
    return save_result(List,n,tablename_ksjs,tablename_ksjs_2,zhushi_ksjs,conn,cursor)

def save_doctor_msg(List,n,conn,cursor):
    '''
    存储医师信息数据
    :param List:
    :param n:
    :param conn:
    :param cursor:
    :return:
    '''
    zhushi_doctor = {'zc':'职称','sf':'身份','pm':'排名','doctor_name':'姓名',
                   'czdd':'出诊地点','scly':'擅长领域','zyjl':'执业经历',
                   'comment':'评价','pingfen':'评分','kesi_name_1':'科室小类','word': '搜索医院名'}
    tablename_doctor, tablename_doctor_2= 'doctor_msg', '医院医师信息'
    return save_result(List,n,tablename_doctor,tablename_doctor_2,zhushi_doctor,conn,cursor)


def sava_pt_ip(List,n,conn,cursor):
    zhushi_ptip={'ptip':'普通ip','label':'有效性','ctime':'采集时间'}
    tablename_ptip, tablename_ptip_2 = 'ptip_msg', '采集到的普通ip信息'
    return save_result(List, n, tablename_ptip, tablename_ptip_2, zhushi_ptip, conn, cursor)


def get_ip2(n,conn,cursor):
    sql='''select ptip from ptip_msg where label="" limit 3'''
    cursor.execute(sql)
    data=cursor.fetchall()
    proxies = {"http": "http://" + '127.0.0.1'}
    if len(data)!=3:
        pt_ip_list = get_pt_ip_list(n)
        sava_pt_ip(pt_ip_list, 100, conn, cursor)
        sql = '''select ptip from ptip_msg where label="" limit 3'''
        cursor.execute(sql)
        data = cursor.fetchall()
    while 0<1:
        ip = data[0][0]
        print(ip)
        try:
            cursor.execute('''update ptip_msg set label="1" where ptip="%s"''' %ip)
            conn.commit()
            proxies = {"http": "http://" + ip}
            sleep(3)
            res = requests.get('http://www.mingyihui.net/', headers=getheaders(), proxies=proxies, timeout=3)
            # res = requests.get('http://www.baidu.com/', headers=getheaders(), proxies=proxies, timeout=3)
            break
        except:
            sql = '''select ptip from ptip_msg where label="" limit 3'''
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) !=3:
                pt_ip_list = get_pt_ip_list(n)
                sava_pt_ip(pt_ip_list, 100, conn, cursor)
    print(proxies)
    return proxies


# if __name__ == '__main__':
#     conn, cursor = get_conn('test')
#     get_ip2(2, conn, cursor)
#     cursor.close()
#     conn.close()
#     print(u'完成')

# if __name__ == '__main__':
#     Dict={'bc': '浙医二院', 'pm': '2017年复旦版全国医院综合排名No.19', 'dz': '杭州市上城区解放路88号',
#           'dh': '(0571)87783777', 'jj': '浙江大学医学院附属第二医院（简称浙医二院）是一所集医疗、教学、科研于一体的大型综合性研究型医院，以学科门类齐全、特色专科鲜明、技术力量雄厚、多学科综合优势强大、管理水平精细享誉海内外。1989年，全国首家通过三级甲等医院...',
#           'name': '浙江大学医学院附属第二医院', 'lx': '公立,三甲,综合'}
#     zhushi={'bc': '医院别称', 'pm': '排名', 'dz': '地址', 'dh': '电话', 'jj': '简介','name': '医院名称', 'lx': '医院类型'}
#     conn,cursor=get_conn()
#     tablename1,tablename2='hospital_msg','医院基础信息'
#     save_result(List,n,tablename1,tablename2,zhushi,conn,cursor)
#     cursor.close()
#     conn.close()
#     print(u'完成')
