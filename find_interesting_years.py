# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 13:21:01 2019

@author: YSu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


year_info=pd.read_csv('year_list.csv',header=None)
price_data=pd.read_csv('all_data.csv',header=None).loc[:,:914]
load=pd.read_csv('Hourly_load.csv',header=0)
CA_load=np.sum(load.values[:,3:],axis=1)
must_run=pd.read_csv('must_run_hourly.csv',header=0)
load_path=pd.read_csv('Load_Path_Sim.csv',header=0)
load_path_matrix=load_path.as_matrix()
pathg=load_path_matrix[:,9:]
CA_hydro=pd.read_excel('CA_hydro_daily.xlsx',header=0)

daily_hydro=np.sum(CA_hydro.values,axis=1)
daily_load=np.sum(load_path_matrix[:,2:6],axis=1)
daily_path=np.sum(pathg,axis=1)


must_run=np.sum(must_run.values,axis=1)
must_run_daily=np.sum(np.reshape(must_run,(365,24)),axis=1)[:364]
#####################################################
year_info=year_info.values

price=price_data.values

AAA=np.average(price,axis=0)
AA=np.argmax(AAA)

top_10_high_idx = np.argsort(AAA)[-10:]
top_10_year=year_info[top_10_high_idx]

Year=year_info[AA]

BB=np.argmin(AAA)
year_min=year_info[BB]


bot_10_idx = (-AAA).argsort()[-10:]
bot_10_year=year_info[bot_10_idx]


####################################################################

def grab_data(year):
    file_name='CA_compacted_result'+ str(year) +'.csv'
    Q=pd.read_csv(file_name,header=0,compression='gzip')
    
    file_name2='CA_renewable'+ str(year) +'.csv'
    Q_2=pd.read_csv(file_name2,header=0,compression='gzip')
    
    last_hour = Q['Time'].iloc[-1]
    Thermal=['Coal','Gas','Nuclear','Oil']
#    Hydro=['Hydro','PSH']
#    Import=['imports']


    T=Q.loc[Q['Type'].isin(Thermal)]
#    H=Q.loc[Q['Type'].isin(Hydro)]
#    I=Q.loc[Q['Type'].isin(Import)]

    T_1=np.zeros(last_hour)
#    H_1=np.zeros(last_hour)#
#    I_1=np.zeros(last_hour)#
    W_1=np.zeros(last_hour)
    S_1=np.zeros(last_hour)
    for i in range(0+1,last_hour+1):
        t1=np.sum(T.loc[T['Time']==i]['mwh_1'].values)
        t2=np.sum(T.loc[T['Time']==i]['mwh_2'].values)
        t3=np.sum(T.loc[T['Time']==i]['mwh_3'].values)
    
        T_1[i-1]=t1+t2+t3
        
#        h1=np.sum(H.loc[H['Time']==i]['mwh_1'].values)
#        h2=np.sum(H.loc[H['Time']==i]['mwh_2'].values)
#        h3=np.sum(H.loc[H['Time']==i]['mwh_3'].values)
#    
#        H_1[i-1]=h1+h2+h3
#        
#        i1=np.sum(I.loc[I['Time']==i]['mwh_1'].values)
#        i2=np.sum(I.loc[I['Time']==i]['mwh_2'].values)
#        i3=np.sum(I.loc[I['Time']==i]['mwh_3'].values)
#    
#        I_1[i-1]=i1+i2+i3
        
        w1=np.sum(Q_2.loc[Q_2['Time']==i]['Wind'].values)
        
        W_1[i-1]=w1
        
        
        s1=np.sum(Q_2.loc[Q_2['Time']==i]['Solar'].values)
        
        S_1[i-1]=s1
#    L=CA_load[year*365*24:year*365*24+364*24]
    T=np.sum(np.reshape(T_1,(364,24)),axis=1)
    S=np.sum(np.reshape(S_1,(364,24)),axis=1)
    W=np.sum(np.reshape(W_1,(364,24)),axis=1)
    must_run=must_run_daily
    hydro=daily_hydro[year*365:year*365+364]
    load=daily_load[year*365:year*365+364]
    imports=daily_path[year*365:year*365+364]
    return T,W,S,must_run,hydro,load,imports

T,W,S,M,H,L,I=grab_data(300)
plt.stackplot(range(0,364),T,W,S,M,H,I*24,alpha=0.7)
plt.plot(L*24)
