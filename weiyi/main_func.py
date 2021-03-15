#coding:utf-8

import re,pymysql,xgboost

def change_sql():
    sql='''select sum(akc196),sum(akc186),sum(1),max(akc914) from kc22'''
    return re.sub('sum|\(|\)|max|min','',re.sub('^select\s+|from.+','',sql))


def get_str():
    pass


if __name__ == '__main__':
    str=change_sql()
    print(str)