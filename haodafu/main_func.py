#coding:utf-8
import sys
sys.path.append("C:\pycharmproject\\venv37\data_sub\haodafu")
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 引入 ActionChains 类
import requests
from save_data import get_conn,save_hdf_hos_link,insert_Dict,insert_List,update_,check_
from get_ip import get_ip2
from get_page import get_browser,restart_browser
from get_ks_link import get_ks_link
from get_hos_link import get_hos_link
from get_hos import get_hos_msg
from get_ks import get_ks_msg
from get_doc import get_doc_msg

def get_one_hos_link(conn,cur):
     '''
     从数据库获取一条未采集完成的医院连接数据
     :param conn:
     :param cur:
     :return:
     '''
     try:
          cur.execute('''select * from hdf_hos_link where zt="" limit 1''')
          data = cur.fetchall()
     except:
          hos_link_list=get_hos_link()
          save_hdf_hos_link(hos_link_list,1000,conn,cur)
     cur.execute('''select * from hdf_hos_link where zt="" limit 1''')
     data = cur.fetchall()[0]
     return {'hos_name': data[0], 'hos_link':data[1], 'diqu': data[2]}


def get_one_ks_link(conn,cur):
     '''
     从数据库获取一条未采集完成的医院科室连接数据
     :param conn:
     :param cur:
     :return:
     '''
     try:
          cur.execute('''select * from hdf_ks_link where zt="" limit 1''')
          data = cur.fetchall()
     except:
          hos_link_list=get_hos_link()
          save_hdf_hos_link(hos_link_list,1000,conn,cur)
     cur.execute('''select * from hdf_ks_link where zt="" limit 1''')
     data = cur.fetchall()[0]
     return {'hos_name': data[0], 'ks_name':data[1], 'ks_url': data[2],'docker_cnt':data[3]}


def get_one_doc_link(conn,cur):
     '''
     从数据库获取一条未采集完成的医院科室连接数据
     :param conn:
     :param cur:
     :return:
     '''
     try:
          cur.execute('''select * from hdf_doc_link where zt="" limit 1''')
          data = cur.fetchall()
     except:
          hos_link_list=get_hos_link()
          save_hdf_hos_link(hos_link_list,1000,conn,cur)
     cur.execute('''select * from hdf_doc_link where zt="" limit 1''')
     data = cur.fetchall()[0]
     return {'hos_name': data[0], 'ks_name':data[1], 'doc_name': data[2],'doc_url':data[3]}


def doc(one_doc_link,browser,conn,cur):
     hos_name = one_doc_link['hos_name']
     ks_name = one_doc_link['ks_name']
     doc_name = one_doc_link['doc_name']
     doc_url = one_doc_link['doc_url']
     while 0<1:
          try:
               doc_Dict, pl_List=get_doc_msg(hos_name,ks_name,doc_url,doc_name,browser) #获取医师信息
               print('数据写入')
               try:
                    insert_Dict('hdf_doc_msg',doc_Dict,cur,conn)
               except:
                   pass
               try:
                    insert_List('hdf_hzpl_msg',pl_List,500,cur,conn)
               except:
                    pass
               print('写入完成')
               break
          except:
               browser = restart_browser(browser, conn, cur)
     sql='''update hdf_doc_link set zt="完成" where hos_name="%s" and ks_name="%s" and doc_name="%s" and doc_url="%s"''' %(hos_name,ks_name,doc_name,doc_url)
     print('%s -- %s -- %s -- %s'%(hos_name,ks_name,doc_name,u'完成'))
     return sql


def ks(one_ks_link,browser,conn,cur):
     '''
     传入科室信息，采集医师连接，并且进行存储
     :param one_ks_link:
     :param browser:
     :param conn:
     :param cur:
     :return:
     '''
     hos_name=one_ks_link['hos_name']
     ks_name=one_ks_link['ks_name']
     ks_url = one_ks_link['ks_url']
     docker_cnt = one_ks_link['docker_cnt']
     label = check_('hdf_doc_link', cur, conn)
     if label:
          while 0<1:
               try:
                    ks_jj_dict,doc_link_List=get_ks_msg(ks_name,hos_name,ks_url,browser) #获取科室信息
                    insert_Dict('hdf_ks_jj',ks_jj_dict,cur,conn)
                    insert_List('hdf_doc_link',doc_link_List,100,cur,conn)
                    break
               except Exception as e:
                    print(e)
                    browser = restart_browser(browser, conn, cur)
     while 0<1:
          try:
               one_doc_link=get_one_doc_link(conn,cur)
               sql=doc(one_doc_link,browser,conn,cur)
               update_(sql,cur,conn)
          except:
               break
     sql = '''update hdf_ks_link set zt="完成" where hos_name="%s" and ks_name="%s" and ks_url="%s" and docker_cnt="%s"''' % (hos_name, ks_name, ks_url, docker_cnt)
     print('%s -- %s -- %s' % (hos_name, ks_name, u'seccess'))
     return sql


def hos(one_hos_link,browser,conn,cur):
     '''
     获取医院连接，采集医院信息并且进行存储
     :param one_hos_link:
     :param browser:
     :param conn:
     :param cur:
     :return:
     '''
     hos_name=one_hos_link['hos_name']
     hos_link = one_hos_link['hos_link']
     diqu = one_hos_link['diqu']
     #获取医院信息
     label=check_('hdf_ks_link',cur,conn)
     if label:
          while 0<1:
               try:
                    hos_msg_Dict=get_hos_msg(hos_link,browser) #获取医院信息
                    insert_Dict('hdf_hos_msg',hos_msg_Dict,cur,conn)
                    break
               except:
                    # browser=restart_browser(browser,conn,cur)
                    break
          while 0<1:
               try:
                    ks_link_List=get_ks_link(hos_name,hos_link,browser) #获取科室连接
                    insert_List('hdf_ks_link',ks_link_List,100,cur,conn)
                    break
               except:
                    browser = restart_browser(browser, conn, cur)
     while 0<1:
          try:
               one_ks_link = get_one_ks_link(conn, cur)
               sql=ks(one_ks_link,browser,conn,cur)
               update_(sql, cur, conn)
          except:
               break
     sql = '''update hdf_hos_link set zt="完成" where hos_name="%s" and hos_link="%s"  and diqu="%s"''' % (hos_name, hos_link,diqu)
     print('%s -- %s -- %s -- %s' %(hos_name,hos_link,diqu,u'seccess'))
     return sql


def main(browser,conn, cur):
     while 0<1:
          try:
               one_hos_link=get_one_hos_link(conn,cur)
               sql=hos(one_hos_link,browser,conn,cur)
               print(sql)
               update_(sql, cur, conn)
          except:
               break
     print(u'完成')

def get_browser2():
     options = webdriver.ChromeOptions()
     options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
     browser = webdriver.Chrome(options=options)
     return browser


if __name__ == '__main__':
     conn,cur=get_conn('test')
     # proxies=get_ip2(10, conn, cur)
     # print(proxies)
     # browser=get_browser(proxies)
     browser=get_browser2()
     main(browser,conn, cur)
     browser.quit()
     cur.close()
     conn.close()
