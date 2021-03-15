#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\haodafu")
from get_page import get_soup,get_ks_url_page


def get_ks_link(hos_name,hos_url,browser):
    '''
    传入一个医院科室页面，ks_url:科室链接,ks_name:科室名称,ks_url:科室配置
    :param ks_url_page:
    :return:[{'ks_url':科室链接,'ks_name':科室名称,'docker_cnt':医师数量,'hos_name':医院名称}]
    '''
    ks_url_page=get_ks_url_page(hos_url,browser)
    soup=get_soup(ks_url_page)
    href_list = soup.select('.bluepanel tbody tr td table tbody a')
    doc_cnt_list = soup.select('.bluepanel tbody tr td table tbody span')
    List=[]
    for i in range(len(href_list)):
        ks_url='https:' + href_list[i]['href']
        ks_name=href_list[i].get_text()
        docker_cnt = doc_cnt_list[i].get_text()
        List.append({'ks_url':ks_url,'ks_name':ks_name,'docker_cnt':docker_cnt,'hos_name':hos_name,'zt':''})
        # print('%s --- %s --- %s' %(ks_url,ks_name,docker_cnt))
    return List