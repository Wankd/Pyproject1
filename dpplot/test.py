#coding：utf-8

import cx_Oracle,os,pymysql,re,json
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class Connent(object):
    @classmethod
    def sbj_database(self):
        '''
        连接省本级数据库
        :return:
        '''
        conn=cx_Oracle.connect('insiis','INSIIS@2018','10.85.95.1:1521/zjcbdb')
        cur=conn.cursor()
        return conn,cur

    @classmethod
    def ydjy_database(self):
        '''
        连接异地就医数据库
        :return:
        '''
        conn = cx_Oracle.connect('ydjy_yw', 'YDJY_YW@2018', '10.85.95.1:1521/zjcbdb')
        cur = conn.cursor()
        return conn, cur

    @classmethod
    def wwfk_databese(self):
        '''
        连接oracle测试数据库
        :return:
        '''
        conn = cx_Oracle.connect('genesis', 'genesis', '172.16.3.142:1521/kaifa')
        cur = conn.cursor()
        return conn, cur

    @classmethod
    def mysql7_databese(self):
        '''
        连接10.85.159.7数据库
        :return:
        '''
        conn = pymysql.connect(
            host='10.85.159.7', user='wankeda', password='WanKeDa123', database='dpplot', charset='utf8', port=3306)
        cur = conn.cursor()
        return conn,cur

    @classmethod
    def mysql8_databese(self):
        '''
        连接10.85.159.8数据库
        :return:
        '''
        conn = pymysql.connect(
            host='10.85.159.8', user='wankeda', password='WanKeDa123', database='dpplot', charset='utf8', port=3306)
        cur = conn.cursor()
        return conn, cur

    @classmethod
    def mysqll_databese(self):
        '''
        连接10.85.159.8数据库
        :return:
        '''
        conn = pymysql.connect(
            host='localhost', user='root', password='root1', database='dpplot', charset='utf8', port=3306)
        cur = conn.cursor()
        cur = conn.cursor()
        return conn, cur


class Getjob:
    def get_file(self,path):
        '''
        读取jobpath
        :return:
        '''
        # filePath='C:\pycharmproject\\venv37\data_sub\dpplot\sql\\'
        # filePath = self.path
        filelist = os.listdir(path)
        return filelist


    def get_sql(self,path):
        '''
        读取sql
        :return:
        '''
        fr = open(path, encoding='utf-8')
        lines = fr.readlines()
        fr.close()
        sql=(''.join(lines))
        sql=sql.replace('[yyyymmdd]',datetime.now().strftime("%Y%m%d"))
        sql = sql.replace('[yyyymm]', datetime.now().strftime("%Y%m"))
        sql = sql.replace('[yyyy]', datetime.now().strftime("%Y"))
        print(sql)
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


class Test(object):
    def __init__(self,string):
        self.string=string

    def print_str(self):
        print(self.string)

    def print_str2(self,n):
        for i in range(n):
            print(self.string)

if __name__ == '__main__':
    sql=Getjob().get_sql('C:\pycharmproject\\venv37\data_sub\dpplot\sql\\test\\test.sql')
    conn,cur=Connent.wwfk_databese()
    cur.execute(sql)
    data=cur.fetchall()
    print(data)
    cur.close()
    conn.close()