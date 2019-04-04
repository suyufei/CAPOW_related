# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 10:19:12 2019

@author: YSu
"""


import pandas as pd
import numpy as np
import random
bad=pd.read_csv('bad_index.csv',header=None)
Gas_price=pd.read_csv('Synthetic_daily_natural_gas.csv')

def New_price_NG(hourly_price,Gas_price):
    
    
    #Calculate electricity prices based on the natural gas price
    ############################
    #Input: hourly zonal price 8376x4
    #       daily natural gas price 365
    #####################################
    
    hourly_NG_price=np.zeros((365*24,4))


    for i in range(0,365*24):
        #The oreder is SEC SDGFE PGEV PGEB
        hourly_NG_price[i,0]=Gas_price[int(i/24)]
        hourly_NG_price[i,1]=Gas_price[int(i/24)]
        hourly_NG_price[i,2]=Gas_price[int(i/24)]+0.19
        hourly_NG_price[i,3]=Gas_price[int(i/24)]+0.19


        
        
    Zones=['SCE','SDGE','PGE_valley','PGE_bay']
    SCE_NG=4.47
    SDGE_NG=4.47
    PGEV_NG=4.66
    PGEB_NG=4.66
    result=np.zeros((np.shape(hourly_price)))
    for i in range(0,len(hourly_price)):
        Q=hourly_price.loc[i,:]
        #SCE
        Q_SCE=Q[Zones[0]]
        if Q_SCE <=10: #It is PHS or hydro
            result[i,0]=Q_SCE
        elif Q_SCE >=20 and Q_SCE <=22.5: #It is coal
            result[i,0]=Q_SCE
        elif Q_SCE>26 and Q_SCE<=26.9: #This is import
            result[i,0]=(Q_SCE-14.5)*Gas_price[0]/SCE_NG
        elif Q_SCE==700:
            result[i,0]=Q_SCE
        else:
            result[i,0]=Q_SCE*Gas_price[0]/SCE_NG
        
        #SDGE   
        Q_SDGE=Q[Zones[1]]
        if Q_SDGE <=10: #It is PHS or hydro
            result[i,1]=Q_SDGE
        elif Q_SDGE>26.8 and Q_SDGE<=26.9: #This is import
            result[i,1]=(Q_SDGE-14.5)*Gas_price[1]/SDGE_NG
        elif Q_SDGE==700:
            result[i,1]=Q_SDGE
        else:
            result[i,1]=Q_SDGE*Gas_price[1]/SDGE_NG
            
        #PGEV
        Q_PGEV=Q[Zones[2]]
        if Q_PGEV <=10: #It is PHS or hydro or import
            result[i,2]=Q_PGEV
        elif Q_PGEV==700:
            result[i,2]=Q_PGEV
        else:
            result[i,2]=Q_PGEV*Gas_price[2]/PGEV_NG
            
        #PGEB
        Q_PGEB=Q[Zones[3]]
        if Q_PGEB <=10: #It is PHS or hydro or import
            result[i,3]=Q_PGEB
        elif Q_PGEV==700:
            result[i,3]=Q_PGEB
        elif Q_PGEB>=270 and Q_PGEB<=300:
            result[i,3]=Q_PGEB
        else:
            result[i,3]=Q_PGEB*Gas_price[3]/PGEB_NG
    
    Hourly_zone_price=pd.DataFrame(result,columns=Zones)
    Hourly_zone_price['Weighted_hourly']=Hourly_zone_price['SCE']*0.27824257 + Hourly_zone_price['SDGE']*0.42484199+Hourly_zone_price['PGE_valley']*-0.12790958+Hourly_zone_price['PGE_bay']*0.85398822
#    Hourly_zone_price.to_csv('Hourly_price_all.csv')
    daily_prices = np.zeros((int(len(Hourly_zone_price)/24),4))

    for i in range(0,int(len(Hourly_zone_price)/24)):
    
        for z in range(0,4):
            
            
            daily_prices[i,z] = np.mean(result[i*24:i*24+24,z])

    weighted_daily_price=daily_prices[:,0]*0.27824257 + daily_prices[:,1]*0.42484199+daily_prices[:,2]*-0.12790958+daily_prices[:,3]*0.85398822
#    np.savetxt('weighted_daily_price_NG.csv',weighted_daily_price,delimiter=',')
    return Hourly_zone_price,weighted_daily_price

weighted_daily=np.zeros((364,999))
count=0
for i in range(862,999):
    if i in bad[0].values:
        pass
    else:
        try:
            name='data_' + str(i)
            path='CA_sim_hourly_prices' + str(i) +'.csv'
            locals()[name]=pd.read_csv(path,header=0,compression='gzip',index_col=0)
            a=random.randint(0,999)
            Gas_price_run=Gas_price.values[a*365:a*365+365]
            hour,day=New_price_NG(locals()[name],Gas_price_run)
            weighted_daily[:,count]=day
            count=count+1
        except FileNotFoundError:
            pass
        
weighted_daily_clean=weighted_daily[:,:915]
np.savetxt('Add_NG_effect.csv',weighted_daily_clean,delimiter=',')
