#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\haodafu")
from get_page import get_soup


def get_doc_link(ks_name,hos_name,ks_page):
    '''
    传入科室界面，获取医师的连接数据
    :param ks_page:
    :return:
    '''
    doct_list=[]
    soup=get_soup(ks_page)
    try:
        index=soup.select('.p_bar .p_num')[-1].get_text()
    except:
        index=None
    doc_msg_list= soup.select('#doc_list_index tbody tr .tdnew_a') #
    doc_jzdz_list= soup.select('#doc_list_index tbody tr .tdnew_c')
    for i in range(len(doc_msg_list)):
        doc_url = 'https:' + doc_msg_list[i].li.a['href']  # 医师链接
        doc_name = doc_msg_list[i].li.a.get_text().strip()  # 姓名
        doc_zc = doc_msg_list[i].li.p.get_text().strip()  # 职称
        try:
            doc_jzdz =doc_jzdz_list[i].div.div.get_text().strip() # 就诊地址
        except:
            doc_jzdz='无'
        doct_list.append({'doc_url':doc_url,'doc_name':doc_name,'doc_zc':doc_zc,'doc_jzdz':doc_jzdz,'ks_name':ks_name,'hos_name':hos_name,'zt':''})
    return doct_list,index



