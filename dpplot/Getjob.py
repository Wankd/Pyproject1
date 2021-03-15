#coding:utf-8
import cx_Oracle,os,pymysql,re,json
from datetime import datetime
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class Getjob(object):
    def get_all_path(self,open_file_path):
        rootdir = open_file_path
        path_list = []
        list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            com_path = os.path.join(rootdir, list[i])
            # print(com_path)
            if os.path.isfile(com_path):
                path_list.append(com_path)
            if os.path.isdir(com_path):
                path_list.extend(get_all_path(com_path))
        # print(path_list)
        return path_list

    def get_file(self,path):
        '''
        读取jobpath
        :return:
        '''
        # filePath='C:\pycharmproject\\venv37\data_sub\dpplot\sql\\'
        # filePath = self.path
        filelist = os.listdir(path)
        return filelist


    def get_sql(self,path,date=None):
        '''
        读取sql
        :return:
        '''
        fr = open(path, encoding='utf-8')
        lines = fr.readlines()
        fr.close()
        sql=(''.join(lines))
        if date is None:
            sql=sql.replace('[yyyymmdd]',datetime.now().strftime("%Y%m%d"))
            sql = sql.replace('[yyyymm]', datetime.now().strftime("%Y%m"))
            sql = sql.replace('[yyyy]', datetime.now().strftime("%Y"))
        else:
            sql = sql.replace('[yyyymmdd]', date)
            sql = sql.replace('[yyyymm]', date)
            sql = sql.replace('[yyyy]', date)
        return sql


    def get_job_info(self,path):
        '''
        读取job信息
        :return:
        '''
        # jobpath = 'C:\pycharmproject\\venv37\data_sub\dpplot\sql\\test\\test.txt'
        fr = open(path, encoding='utf-8')
        lines = fr.readlines()
        Dict = {'job_name': '', 'person': '', 'job_mas': '', 'run_time': '', 'into_table': '', 'from_table': '',
                'fu_name': '', 'zi_id': ''}
        for line in lines:
            if u'[任务名称]' in line:
                Dict['job_name'] = re.sub('\n|\[|\]', '', line.split('--')[1].strip())
            if u'[负责人]' in line:
                Dict['person'] = re.sub('\n|\[|\]', '', line.split('--')[1].strip())
            if u'[任务描述]' in line:
                Dict['job_mas'] = re.sub('\n|\[|\]', '', line.split('--')[1].strip())
            if u'[执行周期]' in line:
                Dict['run_time'] = re.sub('\n|\[|\]', '', line.split('--')[1].strip())
            if u'[目标表]' in line:
                Dict['into_table'] = re.sub('\n|\[|\]', '', line.split('--')[1].strip())
            if u'[数据来源]' in line:
                Dict['from_table'] = re.sub('\n|\[|\]', '', line.split('--')[1].strip())
            if u'[父任务名称]' in line:
                Dict['fu_name'] = re.sub('\n|\[|\]', '', line.split('--')[1].strip())
            if u'[子任务名称]' in line:
                Dict['zi_id'] = re.sub('\n|\[|\]', '', line.split('--')[1].strip())
        fr.close()
        return Dict

    def get_readme(self,path,msg):
        '''
        生成readme文件
        :param path:
        :param msg:
        :return:
        '''
        file = open(path+'readme.m', 'w')
        file.write(msg)
        file.close()


    def get_job_msg(self,path):
        '''
        获取job信息，sql代码，以及任务是否存在定时的状态
        :param path:
        :return:
        '''
        # path = 'C:\pycharmproject\\venv37\data_sub\dpplot\sql\\test'
        filepath_list = self.get_all_path(path)
        filename_list = self.get_file(path)
        sql = ''
        Dict = {}
        label = False
        for filepath in filepath_list:
            if '.sql' in filepath:
                sql = self.get_sql(filepath)
            if '.txt' in filepath:
                Dict = self.get_job_info(filepath)
            if 'readme' in filepath:
                label = True
        return sql, Dict, label #sql代码，配置信息，是否执行标识
