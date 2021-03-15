#coding:utf-8
import sys,cx_Oracle,os,pymysql,re,json
sys.path.append("C:\pycharmproject\\venv37\data_sub\dpplot")
from Save_result import Save_result
from Getjob import Getjob
from Connent import Connent
from datetime import datetime
from time import sleep

def main(path):
    get_job = Getjob()
    connent_ = Connent()
    save_ = Save_result()
    conn2, cur2 = connent_.mysqll_databese()
    sql_run= get_job.get_sql(path)
    start_time = datetime.now()
    start_time1 = start_time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        save_.run_sql(sql_run,conn2,cur2)
        end_time=datetime.now()
        end_time1=end_time.strftime('%Y-%m-%d %H:%M:%S')
        minutes=u'%s分钟' % round((end_time-start_time).seconds/60,2)
        save_.save_job_run_msg('',sql_run,u'成功','',start_time1,end_time1,minutes,conn2,cur2)
    except Exception as e:
        error=str(e)[0:200]
        end_time = datetime.now()
        end_time1 = end_time.strftime('%Y-%m-%d %H:%M:%S')
        minutes = u'%s分钟' % round((end_time - start_time).seconds / 60, 2)
        save_.save_job_run_msg('',sql_run, u'失败',error, start_time1, end_time1, minutes,conn2,cur2)
    cur2.close()
    conn2.close()

if __name__ == '__main__':
    path='C:\pycharmproject\\venv37\data_sub\dpplot\create\\test.sql'
    # path=sys.argv[1]
    main(path)