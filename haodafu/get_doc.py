#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\haodafu")
from get_page import get_soup,get_doc_page
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import random,randint
from save_data import get_conn,insert_List,insert_Dict


def get_pl2(hos_name,ks_name,doc_name,soup):
    pl_list = soup.select('#comment_content .doctorjy tbody .dlemd tbody tr')
    List=[]
    for i in range(len(pl_list)):
        if i % 5 == 0:
            hz_name = pl_list[i].get_text().strip()  # 患者
            hz_shjb = pl_list[i + 1].get_text().strip()  # 所患疾病
            hz_kbmd = pl_list[i + 2].get_text().strip()  # 看病目的
            hz_zlfs = pl_list[i + 3].get_text().strip()  # 治疗方式
            hz_zglx = pl_list[i + 4].get_text().strip()  # 患者主观疗效
            j = int(i / 5)
            hz_pl = soup.select('#comment_content .doctorjy tbody tr td table tbody .spacejy')[j].get_text().strip() #患者评论
            List.append(
                {'hz_name': hz_name, 'hz_shjb': hz_shjb, 'hz_kbmd': hz_kbmd, 'hz_zlfs': hz_zlfs, 'hz_zglx': hz_zglx,
                 'hz_pl': hz_pl,'hos_name':hos_name,'ks_name':ks_name,'doc_name':doc_name})
    return List


def get_pl(hos_name,ks_name,doc_name,soup):
    '''
    :param hos_name:
    :param ks_name:
    :param doc_name:
    :param soup:
    :return: [{'hz_name':患者名字,'hz_shjb':所患疾病,'hz_kbmd':看病目的,'hz_zlfs':治疗方式,'hz_zglx':患者主观疗效,
                         'hz_pl':患者评论,'hos_name':医院名称,'ks_name':科室名称,'doc_name':医师名称}]
    '''
    pl_list=soup.select('#bp_doctor_share .middletr .lt .doctorjyjy .doctorjy tbody .dlemd tbody tr')
    List=[]
    for i in range(len(pl_list)):
        if i % 5==0:
            hz_name=pl_list[i].get_text().strip() #患者
            hz_shjb = pl_list[i+1].get_text().strip() #所患疾病
            hz_kbmd = pl_list[i+2].get_text().strip() #看病目的
            hz_zlfs = pl_list[i+3].get_text().strip() #治疗方式
            hz_zglx = pl_list[i+4].get_text().strip() #患者主观疗效
            j= int(i / 5)
            hz_pl = soup.select('#bp_doctor_share .middletr .lt .doctorjyjy .doctorjy tbody tr td table tbody .spacejy')[j].get_text().strip()
            List.append({'hz_name':hz_name,'hz_shjb':hz_shjb,'hz_kbmd':hz_kbmd,'hz_zlfs':hz_zlfs,'hz_zglx':hz_zglx,
                         'hz_pl':hz_pl,'hos_name':hos_name,'ks_name':ks_name,'doc_name':doc_name})
    return List



def get_pl_list(hos_name,ks_name,doc_name,soup,browser):
    pl_List=[]
    # soup=get_soup(pl_page)
    pl_List.extend(get_pl2(hos_name,ks_name,doc_name,soup))
    try:
        index=soup.select('.p_bar .p_num')[-1].get_text()
    except:
        index=None
    while index==u'下一页':
        click_ = browser.find_element_by_link_text(index)
        ActionChains(browser).click(click_).perform()
        sleep(randint(3, 7) + random())
        page = browser.page_source
        soup = get_soup(page)
        try:
            index = soup.select('.p_bar .p_num')[-1].get_text()
        except:
            index = None
        pl_List.extend(get_pl2(hos_name,ks_name,doc_name,soup))
    return pl_List



def get_doc_msg(hos_name,ks_name,doc_url,doc_name,browser):
    '''
    传入医师链接，获取医师信息以及评价
    :param doc_url:
    :param browser:
    :return:{'gxx':感谢信,'lw':礼物,'doc_ks':医师科室,'doc_zc':医师职称,'doc_sc':医师擅长,
    'doc_zjjl':医师执业经历,'doc_zpj':医生总评价,'doc_tp':患者投票,hos_name:医院名称,ks_name:科室名称,doc_name:医师名字}
    '''
    doc_page=get_doc_page(doc_url,browser)
    sleep(randint(3, 7) + random())
    # print(doc_page)
    soup=get_soup(doc_page)
    doc_msg_list = soup.select('.doctor_about .middletr .lt table tbody tr')  #
    try:
        gxx = soup.select('.doctor_about .middletr .lt table tbody tr .button_halfgxx.halfgxx_bgletter.J_switchcomments')[0].get_text()  ##感谢信
    except:
        gxx=''
    try:
        lw = soup.select('.doctor_about .middletr .lt table tbody tr .button_halfgxx.halfgxx_bgpresent.J_switchcomments')[0].get_text()  # 礼物
    except:
        lw=''
    doc_ks=''
    doc_zc=''
    doc_zjjl=''
    doc_sc=''
    for line in doc_msg_list:
        if u'<h2>' in str(line):
            doc_ks=line.h2.get_text().strip()  # 医师科室
        if u'职　　称：' in str(line):
            doc_zc=line.get_text().strip()
        if u'执业经历' in str(line):
            doc_zjjl=line.get_text().strip()
    try:
        doc_sc = soup.select('.doctor_about .middletr .lt table tbody tr #full_DoctorSpecialize')[0].get_text().strip()  # 医师擅长
    except:
        pass
    try:
        doc_zjjl = soup.select('.doctor_about .middletr .lt table tbody tr #full')[0].get_text().strip() #医师简介
    except:
        pass
    try:
        doc_zpj = ';'.join([i.get_text().strip() for i in soup.select('.doctor_about .middletr .lt .recommend-part span')])  # 医生总评价
        doc_tp_tmp = soup.select('#bp_doctor_getvote .doctor_panel .middletr #doctorgood .ltdiv tbody tr td a')
        doc_tp = ';'.join([doc_tp_tmp[i].get_text().strip() + ':' + doc_tp_tmp[i + 1].get_text().strip() for i in range(len(doc_tp_tmp) - 1) if i % 2 == 0])  # 患者投票
    except:
        pass
    doc_Dict={'gxx':gxx,'lw':lw,'doc_ks':doc_ks,'doc_zc':doc_zc,'doc_sc':doc_sc,'doc_zjjl':doc_zjjl,'doc_zpj':doc_zpj,
              'doc_tp':doc_tp,'hos_name':hos_name,'ks_name':ks_name,'doc_name':doc_name}
    try:
        index_doc_pl = soup.select('.orange.underline.font14.bold')[0].get_text().strip()
        # print(index_doc_pl)
    except:
        index_doc_pl=None
    try:
        if index_doc_pl:
            # index_doc_pl = soup.select('.orange.underline.font14.bold')[0].get_text().strip()
            click_ = browser.find_element_by_link_text(index_doc_pl)
            ActionChains(browser).click(click_).perform()
            page = browser.page_source
            soup = get_soup(page)
            pl_List=get_pl_list(hos_name,ks_name,doc_name,soup,browser)
        else:
            pl_List=get_pl(hos_name,ks_name,doc_name,soup)
    except:
        pass
    return doc_Dict,pl_List

#
# def get_browser2():
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
#     browser = webdriver.Chrome(options=options)
#     return browser
#
#
# if __name__ == '__main__':
#     conn, cur = get_conn('test')
#     hos_name=u'浙医二院'
#     ks_name=u'内科'
#     doc_url='https://www.haodf.com/doctor/DE4r0Fy0C9LuSQFi2UmYPzhmqEELeHuif.htm'
#     doc_name=u'张宝荣'
#     browser=get_browser2()
#     doc_Dict,pl_List=get_doc_msg(hos_name, ks_name, doc_url, doc_name, browser)
#     # insert_Dict('hdf_doc_msg', doc_Dict, cur, conn)
#     # insert_List('hdf_hzpl_msg', pl_List, 500, cur, conn)
#     print(doc_Dict)
#     print(pl_List[0])
#     browser.close()
#     cur.close()
#     conn.close()