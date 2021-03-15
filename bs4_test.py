#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\mingyihui")
from bs4 import BeautifulSoup
from main_func import get_http,get_page
from yyys_doctor import get_doctor_msg2
import re
import os

def file_name(file_dir):
    Dict={}
    file=[]
    for root, dirs, files in os.walk(file_dir):
        file.extend(files)
    for i in file:
        Dict[i]=i
    return Dict



def open_page():
    with open("C:\\Users\epsoft\Desktop\\html\\kkk.html",encoding='utf-8') as fp:
        soup = BeautifulSoup(fp,'html.parser')
    return soup

def get_soup(str_):
    soup=BeautifulSoup(str_,'html.parser')
    return soup


def get_hos_link(soup):
    '''
    获取医院连接信息
    :param page:
    :return:
    '''
    # soup=get_soup(page)
    hos_link_list=soup.select('.jblb  td')
    diqu=''
    for line in hos_link_list:
        # print(line)
        hos_name=line.get_text().strip()
        try:
            hos_link=line.a['href']
            print('%s -- %s -- %s' %(hos_name,hos_link,diqu))
        except:
            if hos_name:
                diqu=hos_name



def get_pl2(soup):
    pl_list = soup.select('#comment_content .doctorjy tbody .dlemd tbody tr')
    for i in range(len(pl_list)):
        if i % 5 == 0:
            hz_name = pl_list[i].get_text().strip()  # 患者
            hz_shjb = pl_list[i + 1].get_text().strip()  # 所患疾病
            hz_kbmd = pl_list[i + 2].get_text().strip()  # 看病目的
            hz_zlfs = pl_list[i + 3].get_text().strip()  # 治疗方式
            hz_zglx = pl_list[i + 4].get_text().strip()  # 患者主观疗效
            j = int(i / 5)
            hl_pl = soup.select('#comment_content .doctorjy tbody tr td table tbody .spacejy')[j].get_text().strip()
            print(hz_name)
            print(hl_pl)

def get_pl(soup):
    pl_list=soup.select('#bp_doctor_share .middletr .lt .doctorjyjy .doctorjy tbody .dlemd tbody tr')
    for i in range(len(pl_list)):
        if i % 5==0:
            hz_name=pl_list[i].get_text().strip() #患者
            hz_shjb = pl_list[i+1].get_text().strip() #所患疾病
            hz_kbmd = pl_list[i+2].get_text().strip() #看病目的
            hz_zlfs = pl_list[i+3].get_text().strip() #治疗方式
            hz_zglx = pl_list[i+4].get_text().strip() #患者主观疗效
            j= int(i / 5)
            hl_pl = soup.select('#bp_doctor_share .middletr .lt .doctorjyjy .doctorjy tbody tr td table tbody .spacejy')[j].get_text().strip()
            print(hz_name)

def get_insert():
    path=u'c:\\bbb.txt'
    file=open(path,encoding='utf-8')
    lines=file.readlines()
    for line in lines:
        line_list=[i.strip() for i in line.split('\t')]
        sql='''insert into abe2(eaz099,eaz100,eaz101,eaz102,eaz103,aae100,eaz106,eaz107,eaz107) values %s;''' %str(tuple(line_list))
        print(sql)

    file.close()



if __name__ == '__main__':
    get_insert()
    # soup=open_page()
    # get_pl2(soup)
    # len(doc_msg_list)
    # doc_msg_list[5]
    # doc_msg_list = soup.select('.doctor_about .middletr .lt table tbody tr')  #
    # gxx=soup.select('.doctor_about .middletr .lt table tbody tr .button_halfgxx.halfgxx_bgletter.J_switchcomments')[0].get_text() ##感谢信
    # lw=soup.select('.doctor_about .middletr .lt table tbody tr .button_halfgxx.halfgxx_bgpresent.J_switchcomments')[0].get_text() #礼物
    # doc_ks=soup.select('.doctor_about .middletr .lt table tbody tr .button_halfgxx.halfgxx_bgletter.J_switchcomments')
    # doc_ks=doc_msg_list[2].h2.get_text().strip() #医师科室
    # doc_zc = doc_msg_list[3].get_text().strip() #医师职称
    # doc_sc = soup.select('.doctor_about .middletr .lt table tbody tr #full_DoctorSpecialize')[0].get_text().strip() #医师擅长
    # try:
    #     doc_jj = soup.select('.doctor_about .middletr .lt table tbody tr #full')[0].get_text().strip() #医师简介
    # except:
    #     try:
    #         doc_jj=doc_msg_list[5].get_text().strip()
    #     except:
    #         doc_jj=''
    # doc_tjrd= soup.select('.doctor_about .middletr .lt .recommend-part .r-p-l-score')[0].get_text().strip()#推荐热度
    # doc_zpj=';'.join([i.get_text().strip() for i in soup.select('.doctor_about .middletr .lt .recommend-part span')])#医生总评价
    #
    # doc_tp=soup.select('#bp_doctor_getvote .doctor_panel .middletr #doctorgood .ltdiv tbody tr td a')
    # jb_name=';'.join([doc_tp[i].get_text().strip()+':'+doc_tp[i+1].get_text().strip() for i in range(len(doc_tp)-1) if i % 2==0]) #患者投票
    #
    # doc_pl=soup.select('.orange.underline.font14.bold')[0].get_text().strip()


# soup = BeautifulSoup(html, 'html.parser')
#
# # 通过tag查找
# print(soup.select('title'))  # [<title>标题</title>]
#
# # 通过tag逐层查找
# print(soup.select("html head title"))  # [<title>标题</title>]
#
# # 通过class查找
# print(soup.select('.sister'))
# # [<a class="sister" href="http://example.com/1" id="link1">链接1</a>,
# # <a class="sister" href="http://example.com/2" id="link2">链接2</a>,
# # <a class="sister" href="http://example.com/3" id="link3">链接3</a>]
#
#
# # 通过id查找
# print(soup.select('#link1, #link2'))
# # [<a class="sister" href="http://example.com/1" id="link1">链接1</a>,
# # <a class="sister" href="http://example.com/2" id="link2">链接2</a>]
#
#
# # 组合查找
# print(soup.select('p #link1'))
# # [<a class="sister" href="http://example.com/1" id="link1">链接1</a>]
#
#
# # 查找直接子标签
# print(soup.select("head > title"))
# # [<title>标题</title>]
#
# print(soup.select("p > #link1"))
# # [<a class="sister" href="http://example.com/1" id="link1">链接1</a>]
#
# print(soup.select("p > a:nth-of-type(2)"))
# # [<a class="sister" href="http://example.com/2" id="link2">链接2</a>]
# # nth-of-type 是CSS选择器
#
#
# # 查找兄弟节点（向后查找）
# print(soup.select("#link1 ~ .sister"))
# # [<a class="sister" href="http://example.com/2" id="link2">链接2</a>,
# # <a class="sister" href="http://example.com/3" id="link3">链接3</a>]
#
# print(soup.select("#link1 + .sister"))
# # [<a class="sister" href="http://example.com/2" id="link2">链接2</a>]
#
#
# # 通过属性查找
# print(soup.select('a[href="http://example.com/1"]'))
#
# # ^ 以XX开头
# print(soup.select('a[href^="http://example.com/"]'))
#
# # * 包含
# print(soup.select('a[href*=".com/"]'))
#
# # 查找包含指定属性的标签
# print(soup.select('[name]'))
#
# # 查找第一个元素
# print(soup.select_one(".sister"))