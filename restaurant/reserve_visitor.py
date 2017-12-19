import glob, re
import numpy as np
import pandas as pd
from sklearn import *
from datetime import datetime
import  matplotlib.pyplot as plt
def findPeak(data):
    indmax=[]
    indmin=[]
    for i in range(1,data.size-2):
        if (data[i]>data[i-1] and data[i+1]<data[i]):
            indmax.append(i)
        else :
            if (data[i]<data[i-1] and data[i+1]>data[i]):
             indmin.append(i)
    return indmax,indmin

data = {
    'air_visit': pd.read_csv('G:/kaggle/restron/train_data/air_visit_data.csv'),
    'as': pd.read_csv('G:/kaggle/restron/train_data/air_store_info.csv'),
    'hs': pd.read_csv('G:/kaggle/restron/train_data/hpg_store_info.csv'),
    'areserve': pd.read_csv('G:/kaggle/restron/train_data/air_reserve.csv'),
    'hreserve': pd.read_csv('G:/kaggle/restron/train_data/hpg_reserve.csv'),
    'id': pd.read_csv('G:/kaggle/restron/train_data/store_id_relation.csv'),
    'tes': pd.read_csv('G:/kaggle/restron/train_data/sample_submission.csv'),
    'hol': pd.read_csv('G:/kaggle/restron/train_data/date_info.csv').rename(columns={'calendar_date':'visit_date'})
    }
perid={}
#print(data['air_visit']['visitors'])
#print(data['air_visit'])
for df in['areserve']:
    data[df]['visit_datetime'] = pd.to_datetime(data[df]['visit_datetime'])
    data[df]['visit_datetime'] = data[df]['visit_datetime'].dt.date
    data[df]['reserve_datetime'] = pd.to_datetime(data[df]['reserve_datetime'])
    data[df]['reserve_datetime'] = data[df]['reserve_datetime'].dt.date
    data[df]['reserve_datetime_diff'] = data[df].apply(lambda r: (r['visit_datetime'] - r['reserve_datetime']).days,
                                                       axis=1)
    tmp1 = data[df].groupby(['air_store_id', 'visit_datetime'], as_index=False)[
        ['reserve_datetime_diff', 'reserve_visitors']].sum().rename(
        columns={'visit_datetime': 'visit_date', 'reserve_datetime_diff': 'rs1', 'reserve_visitors': 'rv1'})
    tmp2 = data[df].groupby(['air_store_id', 'visit_datetime'], as_index=False)[
        ['reserve_datetime_diff', 'reserve_visitors']].mean().rename(
        columns={'visit_datetime': 'visit_date', 'reserve_datetime_diff': 'rs2', 'reserve_visitors': 'rv2'})
    data[df] = pd.merge(tmp1, tmp2, how='inner', on=['air_store_id', 'visit_date'])
    #print(data['areserve'])
    #train = pd.merge(data['air_visit'], data['areserve'], how='left', on= 'visit_date')

data['air_visit']['visit_date'] = pd.to_datetime(data['air_visit']['visit_date'])
data['air_visit']['dow'] = data['air_visit']['visit_date'].dt.dayofweek
data['air_visit']['year'] = data['air_visit']['visit_date'].dt.year
data['air_visit']['month'] = data['air_visit']['visit_date'].dt.month
data['air_visit']['visit_date'] = data['air_visit']['visit_date'].dt.date
peridperdate=pd.merge(data['air_visit'],data['areserve'],how='inner', on=['air_store_id', 'visit_date'])
peridperdate['div']=peridperdate['visitors']/peridperdate['rv1']
peridperdate['sub']=peridperdate['visitors']-peridperdate['rv1']
print(peridperdate)
for i in peridperdate['air_store_id'].drop_duplicates():
    perid[i]=peridperdate[peridperdate['air_store_id']==i]
id_list=peridperdate['air_store_id'].drop_duplicates()
print(id_list)
#考察了一个店
store_id='air_0164b9927d20bcc3jud'
print(perid[store_id])
peridate_id=perid[store_id][['air_store_id', 'visit_date','visitors','rv1','div','dow']]
print(peridate_id.corr())
#测试visitor 和reserve 的高峰点和低谷点,结果对应较好，但是高峰点都在周六，与星期数据较符合，由于数据不是特别完整详细，待进一步检测
"""
x_visitors=(peridate_id['visitors'])
x_reserve=np.array(peridate_id['rv1'])
#num=x.sizenp.array
indmax_visitor,indmin_visitor=findPeak(x_visitors)
indmax_rv1,indmin_rv1=findPeak(x_reserve)
print(peridate_id)
"""
#print(np.array(peridate_id['dow'])(indmax_visitor))
#find peaks
#IndMax=find(diff(sign(diff(a)))<0)+1
#peridate_id.plot()
#plt.show()
peridate=peridperdate[['air_store_id', 'visit_date','div']]
peridate_group=peridperdate.groupby(['air_store_id'],as_index=False)['visitors','rv1'].sum().rename(columns={'air_store_id': 'air_store_id', 'visitors': 'visitors', 'rv1': 'rv1'})
peridate_group['div']=peridate_group['visitors']/peridate_group['rv1']
peridate.corr()
print(peridate.corr())
#print(peridate_group)
#peridate_group['div'].plot()
#print(peridperdate)
#plt.show()
tempvisitor=data['air_visit'].groupby(['visit_date'],as_index=False)['visitors'].sum().rename(
columns={'visit_date': 'visit_date','visitors':'visitor_total'})
tempreserve=data['areserve'].groupby(['visit_date'],as_index=False)['rv1'].sum().rename(
columns={'visit_date': 'visit_date','visitors':'reserve_total'})
#print(tempvisitor)
#print(tempreserve)
visitor_reserve=pd.merge(tempvisitor, tempreserve, how='inner', on=[ 'visit_date'])
visitor_reserve['sub']=visitor_reserve['visitor_total']/visitor_reserve['rv1']
visitor_reserve['visit_date'] = pd.to_datetime(visitor_reserve['visit_date'])
visitor_reserve['dow'] = visitor_reserve['visit_date'].dt.dayofweek
#print(visitor_reserve)
#plt.plot(visitor_reserve['sub'],visitor_reserve['visit_date'])
#print(visitor_reserve['sub'])
#plt.figure()
#plt.plot(visitor_reserve['sub'],visitor_reserve['visit_date'])
#y=visitor_reserve['sub']
#x=visitor_reserve['visit_date']
#plt.plot(x, y)  # b代表blue颜色  -代表直线
#visitor_reserve.plot()
#plt.show()
