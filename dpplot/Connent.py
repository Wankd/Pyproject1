#coding；utf-8
import cx_Oracle,os,pymysql,re,json
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class Connent(object):
    def sbj_database(self):
        '''
        连接省本级数据库
        :return:
        '''
        conn=cx_Oracle.connect('insiis','INSIIS@2018','10.85.95.1:1521/zjcbdb')
        cur=conn.cursor()
        return conn,cur

    def ydjy_database(self):
        '''
        连接异地就医数据库
        :return:
        '''
        conn = cx_Oracle.connect('ydjy_yw', 'YDJY_YW@2018', '10.85.95.1:1521/zjcbdb')
        cur = conn.cursor()
        return conn, cur

    def wwfk_databese(self):
        '''
        连接oracle测试数据库
        :return:
        '''
        conn = cx_Oracle.connect('genesis', 'genesis', '172.16.3.142:1521/kaifa')
        cur = conn.cursor()
        return conn, cur

    def mysql7_databese(self):
        '''
        连接10.85.159.7数据库
        :return:
        '''
        conn = pymysql.connect(
            host='10.85.159.7', user='wankeda', password='WanKeDa123', database='dpplot', charset='utf8', port=3306)
        cur = conn.cursor()
        return conn,cur

    def mysql8_databese(self):
        '''3                                                                                                
        连接10.85.159.8数据库
        :return:
        '''
        conn = pymysql.connect(
            host='10.85.159.8', user='wankeda', password='WanKeDa123', database='dpplot', charset='utf8', port=3306)
        cur = conn.cursor()
        return conn, cur

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