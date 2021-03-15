#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\mingyihui")
import re,urllib3,requests,random
from gk import get_gk
from ksjs import get_ksjs_link
from yyys import get_all_doctor_msg
from save_data import save_hospital_msg,get_conn,save_ksjs_msg,save_doctor_msg,get_ip2


def get_http(ip,hreaders):
    '''
    模拟浏览器，进行数据采集初始化
    :return:
    '''
    http = urllib3.ProxyManager(ip,headers=hreaders)
    return http


def get_page(url,http):
    '''
    返回网页源代码
    :param url:
    :param http:
    :return:
    '''
    try:
        page=http.request('get',url+'/ip').data.decode()
    except:
        page=''
    return page


def get_mingyihui_url(word,http,headers,proxies):
    '''
    获取名医汇，某个医院的页面url的四个连接
    :param word:
    :return:
    '''
    # r = http.request('get', 'http://www.baidu.com/s', fields={'wd': u'宁波市第六医院'}
    url=u'http://www.mingyihui.net/hospitalsearch_%s.html' %word
    # page = get_page(url,http)
    page=requests.get(url,headers=headers,proxies=proxies,timeout=5).text
    if re.search(r'/hospital_\d+\.html', page):
        index=re.search(r'\d+',re.search(r'/hospital_\d+\.html', page).group()).group()
        url_gk =u'http://www.mingyihui.net/hospital_%s.html' %index #概况
        url_xxjs = u'http://www.mingyihui.net/hospital_%s/index.html' % index  # 详细介绍
        url_ksjs = u'http://www.mingyihui.net/hospitalx_%s/departments.html' %index #科室介绍
        url_yykb = u'http://www.mingyihui.net/hospital_%s/comment.html' % index #医院口碑
        print(1)
    else:
        url_gk = u''
        url_xxjs = u''
        url_ksjs = u''
        url_yykb = u''
    return url_gk,url_xxjs,url_ksjs,url_yykb


def get_all_url(word,headers,conn,cursor):
    '''
    获取所有连接
    :param word:
    :param http:
    :param headers:
    :param proxies:
    :return:
    '''
    proxies=get_ip2(10,conn,cursor)
    ip=proxies['http']
    http=get_http(ip,headers)
    url_gk=''
    url_xxjs=''
    url_ksjs=''
    url_yykb=''
    page_gk=''
    page_ksjs=''
    while url_gk=='' or page_gk=='' or page_ksjs=='':
        try:
            url_gk, url_xxjs, url_ksjs, url_yykb = get_mingyihui_url(word, http, headers, proxies)
            page_gk = get_page(url_gk, http)
            page_ksjs = get_page(url_ksjs, http)
        except:
            proxies = get_ip2(10,conn,cursor)
            ip = proxies['http']
            http = get_http(ip, headers)
    return page_gk, url_xxjs, page_ksjs, url_yykb ,ip , http



def getheaders():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent=random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers

def passs():
    # word = u'绍兴文理学院附属医院'
    # word = u'浙江大学医学院附属第二医院'
    # word = u'诸暨市中医医院'
    # word = u'浙江省中医院'
    # word = u'浙江省人民医院'
    # word = u'嘉兴市第一医院'
    # word = u'海宁市中心医院'
    # word = u'嘉兴市第二医院'
    # word = u'杭州同济医院'
    # word = u'杭州市中医院'
    # word = u'杭州市余杭区第一人民医院'
    # word = u'浙江大学医学院附属邵逸夫医院'
    # word = u'浙江大学医学院附属儿童医院'
    # word = u'杭州市老年病医院'
    # word = u'温州医科大学附属眼视光医院杭州院区'
    # word = u'浙江康复医疗中心'
    # word = u'浙江绿城心血管病医院'
    # word = u'浙江大学明州医院'
    # word = u'浙江医院'
    # word = u'浙江中医药大学附属第二医院'
    # word = u'浙江武警总队医院'
    # word = u'浙江大学医学院附属口腔医院'
    # word = u'浙江省青春医院'
    # word = u'浙江中医药大学附属第三医院'
    # word = u'浙江省公安边防总队医院'
    # word = u'杭州市第一人民医院'
    # word = u'浙江省中西医结合医院'
    # word = u'杭州市西溪医院'
    # word = u'杭州市第七人民医院'
    # word = u'萧山区第一人民医院'
    # word = u'杭州市下城区中西医结合医院'
    # word = u'杭州市江干区人民医院'
    # word = u'西湖区留下街道社区卫生服务中心'
    # word = u'浙江省复员退伍军人精神病疗养院'
    pass


if __name__ == '__main__':
    conn, cursor = get_conn('test')
    headers =getheaders()
    # word = u'宁波市眼科医院西部院区'
    # word_list=[u'杭州市萧山区第二人民医院',u'浙江中医药大学附属第二医院',u'杭州市余杭区中医院',u'湖州市中医院',
    #            u'绍兴市柯桥区中医医院',u'长兴县中医院',u'长兴县妇幼保健院']
    # word_list = [u'海曙区段塘街道社区卫生服务中心', u'湖州市妇幼保健院', u'宁波市第二医院', u'宁波鄞州眼科医院',
    #              u'平湖市中医院', u'苍南县中医院', u'淳安县中医院']
    # word_list = [u'宁波市第二医院', u'宁波市第九医院', u'临安市昌化人民医院', u'宁波爱尔光明眼科医院有限公司',
    #              u'开化县人民医院', u'慈溪市妇幼保健院', u'杭州市萧山区中医骨伤科医院']
    # word_list = [u'开化县人民医院', u'海宁市妇幼保健院', u'横店文荣医院', u'东阳市横店医院',
    #              u'绍兴市中医院', u'宁波市镇海区人民医院', u'宁波开发区中心医院']
    # word_list = [u'镇海区人民医院', u'宁波市鄞州区第三医院', u'宁波大榭开发区医院', u'绍兴市妇幼保健院',
    #              u'慈溪协和医院', u'上虞市中医院', u'慈溪市中医医院']
    # word_list = [u'慈溪市中医医院', u'宁波市鄞州区中河街道社区卫生服务中心', u'平湖市第二人民医院', u'宁波市北仑区中医院',
    #              u'温州市第七人民医院', u'江山市中医院', u'宁波市康宁医院']
    # word_list = [u'海宁市第四人民医院', u'金华市金东区中医院', u'永嘉县中医医院', u'建德中医院',
    #              u'杭州市余杭区妇幼保健院', u'宁波市北仑区第二人民医院', u'永康医院']
    # word_list = [u'金华眼科医院', u'义乌市第二人民医院', u'海宁市第二人民医院', u'永康市妇幼保健院',
    #              u'浙江省荣军医院', u'兰溪市妇幼保健计划生育服务中心', u'富阳市妇幼保健院']
    # word_list = [u'富阳市妇幼保健院', u'江北区洪塘街道社区卫生服务中心', u'金华市妇幼保健院', u'北仑区大碶街道社区卫生服务中心',
    #              u'瑞安市塘下人民医院', u'宁波健民肛肠医院', u'杭州市余杭区第五人民医院']
    # word_list = [u'金华市妇幼保健院', u'杭州市萧山区第一人民医院', u'杭州市余杭区第一人民医院', u'杭州市余杭区良渚医院',
    #              u'富阳市中医骨伤医院', u'杭州市萧山区中医院', u'永康市中医院']
    # word_list = [u'镇海区骆驼街道社区卫生服务中心', u'富阳市第二人民医院', u'诸暨市中心医院', u'诸暨市第四人民医院',
    #              u'杭州市萧山区第三人民医院', u'余杭区第五人民医院', u'绍兴市第七人民医院']
    # word_list = [u'衢州市妇幼保健院', u'嘉善县第三人民医院', u'余杭区第二人民医院', u'富阳区第一人民医院',
    #              u'杭州市余杭区良渚医院', u'杭州市余杭区第三人民医院', u'富阳市中医骨伤医院', u'杭州市萧山区第三人民医院',u'余杭区第五人民医院']
    # word_list = [u'湖州爱尔眼科医院', u'建德市中西医结合医院', u'富阳市第三人民医院', u'桐乡市第二人民医院',
    #              u'嘉善县第二人民医院', u'宁海县城关医院', u'苍南县第二人民医院', u'诸暨市第六人民医院', u'杭州市大江东医院']
    # word_list = [u'乐清开发区医院有限公司', u'乐清市第二人民医院', u'杭州市余杭区妇幼保健院', u'乐清市第三人民医院',
    #              u'嵊州市妇幼保健院', u'嵊州市中医院', u'江东区白河街道社区卫生服务中心', u'象山县红十字台胞医院', u'永康市第二人民医院']
    # word_list = [u'宁海县妇幼保健院', u'苍南县第三人民医院', u'嘉善县中医医院', u'义乌市精神卫生中心',
    #              u'东阳市红十字会医院', u'温州老年病医院', u'平阳县中医院', u'奉化爱伊美医院', u'奉化新桥骨科医院']
    # word_list = [u'富阳市中医院', u'舟山市第二人民医院', u'宁波市康复医院', u'义乌市后宅街道社区卫生服务中心',
    #              u'新昌县张氏骨伤医院', u'新昌县中医院', u'宁波镇海第二医院', u'温州市龙湾区第一人民医院', u'瑞安市第三人民医院']
    # u'杭州天目山妇产医院', u'温州建国医院'
    word_list = [u'慈溪市第三人民医院', u'浙江中医药大学附属第三医院',
                 u'浙江省肿瘤医院', u'杭州整形医院', u'浙江省嘉兴市海盐县妇幼保健院', u'海曙区古林镇卫生院', u'余姚市第四人民医院',
                 u'温州东华医院',u'临安市於潜人民医院',u'东阳市妇幼保健院',u'浙江慈爱康复医院',u'临安市中医院',u'武义县中医院',u'宁波市杭州湾医院',u'温州市瓯海区第三人民医院']
    for word in word_list:
        page_gk, url_xxjs, page_ksjs, url_yykb, ip, http = get_all_url(word, headers,conn,cursor)
        gk_Lsit = [get_gk(page_gk,word)]
        ksjs_List = get_ksjs_link(page_ksjs, word)
        print('stark docker')
        doctor_List = get_all_doctor_msg(ip,ksjs_List,conn,cursor)
        save_hospital_msg(gk_Lsit,1,conn,cursor)
        save_ksjs_msg(ksjs_List,1000,conn,cursor)
        save_doctor_msg(doctor_List,10000,conn,cursor)
        print('%s success' %word)
    cursor.close()
    conn.close()