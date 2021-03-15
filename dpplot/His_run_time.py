#coding:utf-8
from datetime import datetime,timedelta


def get_time_list(date1,date2):
    time_list = []
    if len(date1)==4:
        date1=int(date1)
        date2=int(date2)
        while date1<=date2:
            time_list.append(str(date1))
            date1+=1
        return time_list
    if len(date1)==6:
        date1_year=date1[0:4]
        date1_month=date1[4:6]
        while date1<=date2:
            time_list.append(date1)
            date1_month=int(date1_month)+1
            if date1_month==13:
                date1='%s%s' %(int(date1_year)+1,'01')
            else:
                date1 = '%s%s' % (date1_year, str(date1_month) if date1_month>=10 else '0'+ str(date1_month))
            date1_year = date1[0:4]
            date1_month = date1[4:6]
        return time_list
    if len(date1)==8:
        date1=datetime.strptime(date1,'%Y%m%d')
        date2 = datetime.strptime(date2, '%Y%m%d')
        while date1<=date2:
            time_list.append(date1.strftime('%Y%m%d'))
            date1=date1+timedelta(hours=24)
        return time_list