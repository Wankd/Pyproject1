#coding:utf-8
import sys,cx_Oracle,os,pymysql,re,json
sys.path.append("C:\pycharmproject\\venv37\data_sub\dpplot")
from Save_result import Save_result
from Getjob import Getjob
from Connent import Connent
from Linux_task import Create_task

def Set_task(path):
    get_job=Getjob()
    connent_=Connent()
    save_=Save_result()
    conn2, cur2 = connent_.mysql7_databese() #连接数据库
    in_path=get_job.get_file(path)
    for new_path in in_path:
        new_path=path+new_path
        sql, Dict, label=get_job.get_job_msg(new_path)
        if label:
            pass
        else:
            save_.save_job_info(Dict,conn2,cur2)
            get_job.get_readme(new_path,u'完成')
            Create_task(Dict,path)
    cur2.close()
    conn2.close()


if __name__ == '__main__':
    path=''
    Set_task(path)