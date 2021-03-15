#coding:utf-8
import cx_Oracle,os,pymysql,re,json
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import sys
import re
sys.path.append("C:\pycharmproject\\venv37\data_sub\dpplot")
from Connent import Connent
import multiprocessing as mp
from time import sleep
class Save_result(object):
    def get_data(self,sql,conn,cur):
        '''
        获取数据
        :param sql:
        :param conn:
        :param cur:
        :return:
        '''
        def p1(sql,conn,cur):
            cur.execute(sql)
            conn.commit()
        label=('create' in sql or 'CREATE' in sql) and ('table' in sql or 'TABLE' in sql) and (
                    'as' in sql or 'AS' in sql)
        if label:
            table_name=re.split('table|TABLE',re.split('as|AS',sql)[0])[-1].strip()
            drop_table_sql='''drop table %s''' %table_name
            try:
                cur.execute(drop_table_sql)
                conn.commit()
            except:
                pass
            select_sql = '''select * from %s'''%table_name
            p = mp.Process(target=p1, args=(sql, conn, cur))
            p.start()
            while 0 < 1:
                cur.execute(select_sql)
                conn.commit()
                data = cur.fetchall()
                if len(data) > 0:
                    p.terminate()
                    break
                sleep(180)
            p.join()
        else:
            cur.execute(sql)
            data=cur.fetchall()
        return data

    def save_job_info(self,Dict,conn,cur):
        '''
        连接mysql数据库,存储任务信息
        :param Dict:
        :param conn:
        :param cur:
        :return:
        '''
        key_list = []
        value_list = []
        for key in Dict:
            value = pymysql.escape_string(str(Dict[key]))
            key_list.append('`%s`' % key)
            value_list.append('"%s"' % value)
        sql = '''insert into `job_info`(%s) values(%s)''' % (','.join(key_list), ','.join(value_list))
        cur.execute(sql)
        conn.commit()

    def save_job_run_msg(self,job_name,sql_run,status,error,time1,time2,minutes,conn,cur):
        sql='''insert into job_run_msg values("%s","%s","%s","%s","%s","%s","%s")''' %(job_name,sql_run,status,error,time1,time2,minutes)
        print(sql)
        cur.execute(sql)
        conn.commit()

    def save_data(self,Dict,data,conn,cur):
        '''
        存储数据
        :param data:
        :param Dict:
        :param conn:
        :param cur:
        :return:
        '''
        table=Dict['job_name']
        into_table=Dict['into_table']
        if u'overwrite' in into_table:
            sql='delete from %s where 1=1' %table
            cur.execute(sql)
            conn.commit()
        i=0
        for line in data:
            List=[]
            for word in line:
                if word:
                    List.append(word)
                else:
                    List.append('')
            sql='insert into %s values%s' %(table,tuple(List))
            # print(sql)
            cur.execute(sql)
            i+=1
            if i>=500:
                conn.commit()
                i=0
        conn.commit()

    def run_sql(self,sql,conn,cur):
        '''
        执行sql
        :param sql:
        :param conn:
        :param cur:
        :return:
        '''
        cur.execute(sql)
        conn.commit()

    def get_running_task(self,conn,cur):
        '''
        获取正在执行task列表
        :param conn:
        :param cur:
        :return:
        '''
        sql='''select job_name from task_running'''
        cur.execute(sql)
        data=cur.fetchall()
        task_list=[]
        for line in data:
            task_list.append(line[0])
        return task_list


    def run2(self,sql, Dict):
        connent_=Connent()
        if 'wwkf' in Dict['from_table']:
            conn, cur = connent_.wwfk_databese()
        elif 'sbj' in Dict['from_table']:
            conn, cur = connent_.sbj_database()
        else:
            conn, cur = connent_.ydjy_database()
        conn2, cur2 = connent_.mysql7_databese()
        try:
            data=self.get_data(sql,conn,cur)
            self.save_data(sql,Dict,data,conn2,cur2)
        except Exception as e:
            pass
        cur.close()
        conn.close()
        cur2.close()
        conn2.close()


