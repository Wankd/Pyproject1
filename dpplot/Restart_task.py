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
    sql_run, Dict, label = get_job.get_job_msg(path)
    job_name = Dict['job_name']  # 任务名称
    fu_name = [] if Dict['fu_name'] == '' else [fu_job_name for fu_job_name in re.split(',', Dict['fu_name'])]
    fu_name.append(job_name)  # 父任务名称
    sql = '''delete from task_running where job_name="%s"''' %job_name
    save_.run_sql(sql, conn2, cur2)
    task_list = save_.get_running_task(conn2, cur2)  # 正在执行的任务名称
    while len(set(fu_name) & set(task_list)) > 0:
        print(u'等待')
        sleep(180)
        task_list = save_.get_running_task(conn2, cur2)  # 正在执行的任务名称
    start_time = datetime.now()
    start_time1 = start_time.strftime('%Y-%m-%d %H:%M:%S')
    sql = '''insert into task_running values ('%s','%s')''' % (job_name, start_time1)
    save_.run_sql(sql, conn2, cur2)
    if 'wwkf' in Dict['from_table']:
        conn, cur = connent_.wwfk_databese()
    elif 'sbj' in Dict['from_table']:
        conn, cur = connent_.sbj_database()
    else:
        conn, cur = connent_.ydjy_database()
    try:
        data = save_.get_data(sql_run, conn, cur)
        save_.save_data(Dict, data, conn2, cur2)
        end_time = datetime.now()
        end_time1 = end_time.strftime('%Y-%m-%d %H:%M:%S')
        minutes = u'%s分钟' % round((end_time - start_time).seconds / 60, 2)
        save_.save_job_run_msg(job_name, sql_run, u'成功', '', start_time1, end_time1, minutes, conn2, cur2)
        sql = '''delete from task_running where job_name='%s' and start_time='%s' ''' % (job_name, start_time1)
        save_.run_sql(sql, conn2, cur2)
    except Exception as e:
        error = str(e)[0:200]
        end_time = datetime.now()
        end_time1 = end_time.strftime('%Y-%m-%d %H:%M:%S')
        minutes = u'%s分钟' % round((end_time - start_time).seconds / 60, 2)
        save_.save_job_run_msg(job_name, sql_run, u'失败', error, start_time1, end_time1, minutes, conn2, cur2)
    cur.close()
    conn.close()
    cur2.close()
    conn2.close()

if __name__ == '__main__':
    path = 'C:\pycharmproject\\venv37\data_sub\dpplot\sql\\test'
    # path=sys.argv[1]
    main(path)