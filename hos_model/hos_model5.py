#coding:utf-8

import pymysql
import re
def get_conn():
    '''
    获取连接
    :param database:
    :return:
    '''
    conn = pymysql.connect(
        host='localhost', user='root', password='root1', database='test', charset='utf8', port=3306)
    cursor = conn.cursor()

    return conn, cursor




def t(str):
    zhong={'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9};
    danwei={'十':10,'百':100,'千':1000,'万':10000};
    num=0;
    if len(str)==0:
        return 0;
    if len(str)==1:
        if str == '十':
            return 10;
        num=zhong[str];
        return num;
    temp=0;
    if str[0] == '十':
        num=10;
    for i in str:
        if i == '零':
            temp=zhong[i];
        elif i == '一':
            temp=zhong[i];
        elif i == '二':
            temp=zhong[i];
        elif i == '三':
            temp=zhong[i];
        elif i == '四':
            temp=zhong[i];
        elif i == '五':
            temp=zhong[i];
        elif i == '六':
            temp=zhong[i];
        elif i == '七':
            temp=zhong[i];
        elif i == '八':
            temp=zhong[i];
        elif i == '九':
            temp=zhong[i];
        if i == '十':
            temp=temp*danwei[i];
            num+=temp;
        elif i == '百':
            temp=temp*danwei[i];
            num+=temp;
        elif i == '千':
            temp=temp*danwei[i];
            num+=temp;
        elif i == '万':
            temp=temp*danwei[i];
            num+=temp;
    if str[len(str)-1] != '十'and str[len(str)-1] != '百'and str[len(str)-1] != '千'and str[len(str)-1] != '万':
        num+=temp
    return num


def get_liangci(word):
    liangci = re.search('([0-9一二三四五六七八九十]){0,6}(余|多)?[篇|项|个]', word)
    if liangci:
        liangci_1 = re.search('([0-9一二三四五六七八九十])+', liangci.group())
        if liangci_1:
            try:
                num=int(liangci_1.group())
            except:
                num = int(t(liangci_1.group()))
        else:
            num=1
    else:
        num=1
    return num

def get_doc_zjjl_score(doc_zjjl):
    score=0
    word_list=re.split('，|、|：|。|．|；',doc_zjjl)
    for word in word_list:
        if u'基金' in word or u'项目' in word or u'课题' in word:
            score+=get_liangci(word)*1
        if u'一等将' in word or u'1等级' in word:
            score+=get_liangci(word)*12
        elif u'二等将' in word or u'2等级' in word:
            score+=get_liangci(word)*6
        elif u'三等将' in word or u'3等级' in word:
            score+=get_liangci(word)*3
        elif u'将' in word:
            score += get_liangci(word) * 1
        if u'论文' in  word or u'文章' in word:
            score += get_liangci(word) * 0.1
        if u'发明' in word:
            score += get_liangci(word) * 10
    return score

def get_data(conn,cursor):
    Dict={}
    sql = '''select hos_name,doc_name,doc_zjjl from hdf_doc_msg group by hos_name,doc_name,doc_zjjl'''
    cursor.execute(sql)
    data = cursor.fetchall()
    for line in data:
        hos_name=line[0]
        doc_name=line[1]
        doc_zjjl=line[2]
        if hos_name not in Dict:
            Dict[hos_name]=0
        Dict[hos_name]+=get_doc_zjjl_score(doc_zjjl)
    return Dict


def get_(conn,cursor):
    file=open('C:\pycharmproject\\venv37\data_sub\hos_model\data.csv',encoding='utf-8')
    lines=file.readlines()
    i,j=0,0
    List=[]
    for line in lines:
        i+=1
        if i>1:
            line=line.replace('\"','').strip()
            value_list=line.split(';')
            print(value_list)
            hos_name=value_list[0]
            amt =0.0 if value_list[1]=='' else  float(value_list[1])
            jj_amt =0.0 if value_list[2]=='' else float(value_list[2])
            bili =0.0 if value_list[3]=='' else float(value_list[3])
            user_cnt =0 if value_list[4]=='' else  int(value_list[4])
            sql='''insert into hos_model_5data values("%s",%.2f,%.2f,%.6f,%s)''' %(hos_name,amt,jj_amt,bili,user_cnt)
            j+=1
            cursor.execute(sql)
        if j>=500:
            conn.commit()
            j=0
    conn.commit()
    file.close()


def main():
    conn, cursor=get_conn()
    Dict=get_data(conn,cursor)
    Dict2=sorted(Dict.items(), key=lambda x: x[1], reverse=True)
    k=0
    for key in Dict2:
        sql='''insert into tmp_hos_model_4 values("%s",%.2f)''' %(key[0],key[1])
        cursor.execute(sql)
    conn.commit()
    # get_(conn, cursor)
    cursor.close()
    conn.close()



def get_hos_index():
    conn, cursor = get_conn()
    file = open('C:\pycharmproject\\venv37\data_sub\hos_model\hos_index.csv', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        value_list = re.split('[\s|\t]+',line.strip())
        sql = '''insert into hos_index values("%s",%s)''' % (value_list[0],value_list[1])
        print(sql)
        cursor.execute(sql)
    conn.commit()
    file.close()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()