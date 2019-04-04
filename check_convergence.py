# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 14:30:09 2018

@author: YSu
"""

from __future__ import division
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
from datetime import timedelta
load_path=pd.read_csv('Synthetic_demand_pathflows/Load_Path_Sim.csv',header=0)
load_path_matrix=load_path.as_matrix()
#BPA_Hydro=pd.read_csv('Modeled_BPA_dams.csv',header=None)
CA_Hydro_PGE=pd.read_excel('CA_hydropower/CA_hydro_daily.xlsx').loc[:,'PGE_valley']
CA_Hydro_SCE=pd.read_excel('CA_hydropower/CA_hydro_daily.xlsx').loc[:,'SCE']
wind=pd.read_csv('Synthetic_wind_power/wind_power_sim.csv',header=0).loc[:,'CAISO']
wind_matrix=wind.as_matrix()
Solar=pd.read_csv('Synthetic_solar_power/solar_power_sim.csv',header=0).loc[:,'CAISO']
Solar_matrix=Solar.as_matrix()


CA_Hydro=CA_Hydro_PGE.values+CA_Hydro_SCE.values
CA_Hydro=CA_Hydro/24



price=pd.read_csv('prices_daily.csv',header=None)
price_0=pd.read_csv('data_0year.csv',header=None)
#yearly_load_path[:,11]=yearly_load_path[:,11]/24

daily_load_agg=np.sum(load_path_matrix[:,2:6],axis=1)
#yearly_path_agg=np.sum(yearly_load_path[:,9:],axis=1)
pathg=load_path_matrix[:,9:]
daily_path=np.sum(pathg,axis=1)




Hydro_percentail=np.percentile(CA_Hydro,[1,5,10,50,90,95,99])
Wind_percentail=np.percentile(wind,[1,5,10,50,90,95,99])
Solar_precentail=np.percentile(Solar,[1,5,10,50,90,95,99])
Load_precentail=np.percentile(daily_load_agg,[1,5,10,50,90,95,99])

daily_wind=np.zeros(len(CA_Hydro))
daily_solar=np.zeros(len(CA_Hydro))
for i in range(0,int(len(wind)/24)):
    daily_wind[i]=np.sum(wind[i*24+0:i*24+24])/24
    daily_solar[i]=np.sum(Solar[i*24+0:i*24+24])/24
    
    
Net_load=daily_load_agg-daily_wind-CA_Hydro-daily_solar-daily_path

What_we_care=[Hydro_percentail,Wind_percentail,Solar_precentail,Load_precentail]
AAA=pd.DataFrame(What_we_care)

His_stats=pd.read_csv('His_data_stats.csv',header=0,index_col=0)

His_matrix=His_stats.values


Model_matrix=AAA.values

#Full_Diff=His_matrix-Model_matrix

step=np.zeros(100)
for i in range(1,101):
    step[i-1]=i*10
    
Dif_1=np.zeros(100)
Dif_99=np.zeros(100)


Dif_1_load=np.zeros(100)
Dif_99_load=np.zeros(100)

Dif_1_wind=np.zeros(100)
Dif_99_wind=np.zeros(100)

Dif_1_netload=np.zeros(100)
Dif_99_netload=np.zeros(100)
c=0
for i in step:
    New_CA_hydro=CA_Hydro[:365*int(i)]
    Hydro_percentail_new_1=np.percentile(New_CA_hydro,[1])
    Hydro_percentail_new_99=np.percentile(New_CA_hydro,[99])
    
    New_CA_load=daily_load_agg[:365*int(i)]
    Load_percentail_new_1=np.percentile(New_CA_load,[1])
    Load_percentail_new_99=np.percentile(New_CA_load,[99])
    
    New_CA_wind=wind[:365*int(i)*24]
    Wind_percentail_new_1=np.percentile(New_CA_wind,[1])
    Wind_percentail_new_99=np.percentile(New_CA_wind,[99])
    
    
    New_CA_netload=Net_load[:365*int(i)]
    NL_percentail_new_1=np.percentile(New_CA_netload,[1])
    NL_percentail_new_99=np.percentile(New_CA_netload,[99])
    
    Dif_1[c]=abs(His_matrix[0,0]-Hydro_percentail_new_1)
    Dif_99[c]=abs(His_matrix[0,6]-Hydro_percentail_new_99)
    
    
    Dif_1_load[c]=abs(His_matrix[3,0]-Load_percentail_new_1)
    Dif_99_load[c]=abs(His_matrix[3,6]-Load_percentail_new_99)
    
    
    Dif_1_wind[c]=abs(His_matrix[1,0]-Wind_percentail_new_1)
    Dif_99_wind[c]=abs(His_matrix[1,6]-Wind_percentail_new_99)
    
    Dif_1_netload[c]=His_matrix[4,0]-NL_percentail_new_1
    Dif_99_netload[c]=His_matrix[4,6]-NL_percentail_new_99
    c=c+1

plt.figure()
plt.plot(Dif_1)
plt.title('Hydro 1%')
plt.xticks(np.arange(100,step=10),([0,100,200,300,400,500,600,700,800,900,1000]))
plt.savefig('Hydro_1%.png')
np.savetxt('Hydro_1%.csv',Dif_1,delimiter=',')

plt.figure()
plt.plot(Dif_99)
plt.title('Hydro 99%')
plt.xticks(np.arange(100,step=10),([0,100,200,300,400,500,600,700,800,900,1000]))
plt.savefig('Hydro_99%.png')
np.savetxt('Hydro_99%.csv',Dif_99,delimiter=',')

plt.figure()
plt.plot(Dif_1_load)
plt.title('Load 1%')
plt.xticks(np.arange(100,step=10),([0,100,200,300,400,500,600,700,800,900,1000]))
plt.savefig('Load_1%.png')
np.savetxt('Load_1%.csv',Dif_1_load,delimiter=',')

plt.figure()
plt.plot(Dif_99_load)
plt.title('Load 99%')
plt.xticks(np.arange(100,step=10),([0,100,200,300,400,500,600,700,800,900,1000]))
plt.savefig('Load_99%.png')
np.savetxt('Load_99%.csv',Dif_99_load,delimiter=',')


plt.figure()
plt.plot(Dif_1_wind)
plt.title('Wind 1%')
plt.xticks(np.arange(100,step=10),([0,100,200,300,400,500,600,700,800,900,1000]))
plt.savefig('Wind_1%.png')
np.savetxt('Wind_1%.csv',Dif_1_wind,delimiter=',')

plt.figure()
plt.plot(Dif_99_wind)
plt.title('Wind 99%')
plt.xticks(np.arange(100,step=10),([0,100,200,300,400,500,600,700,800,900,1000]))
plt.savefig('Wind_99%.png')
np.savetxt('Wind_99%.csv',Dif_99_wind,delimiter=',')




plt.figure()
plt.plot(Dif_1_netload)
plt.title('Net Load 1%')
plt.xticks(np.arange(100,step=10),([0,100,200,300,400,500,600,700,800,900,1000]))
plt.savefig('Netload_1%_abs.png')
np.savetxt('Netload_1%_abs.csv',Dif_1_netload,delimiter=',')

plt.figure()
plt.plot(Dif_99_netload)
plt.title('Net load 99%')
plt.xticks(np.arange(100,step=10),([0,100,200,300,400,500,600,700,800,900,1000]))
plt.savefig('Netload_99%_abs.png')
np.savetxt('Netload_99%_abs.csv',Dif_99_netload,delimiter=',')
##########################################################################################
#
#Below is convergance calculation for temperature and wind
weather_data=pd.read_csv('Synthetic_weather/synthetic_weather_data.csv',header =0,index_col=0)
weather_title=list(weather_data)

#Generate matrix for storing the results
weather_stats= np.zeros((len(weather_title),3))

def fillgap(Q,d):
    #The first step is to check where the gaps are
    gaps_location=np.argwhere(np.isnan(Q))
    if len(gaps_location)==0:
        print('There is no gap')
    else:
        gaps=Q.isnull().astype(int).groupby(Q.notnull().astype(int).cumsum()).sum()
        list_of_gaps = gaps.loc[~(gaps==0)]
        largest_gap=np.max(gaps)
        if largest_gap>=d:
            print('More cleaning up')
        else:
            Index_correction=0
            for i in range(0,len(list_of_gaps)):
                Num_NaNs=list_of_gaps.values[i]
                Num_previous_point=math.ceil(Num_NaNs/2)
                
                for j in range(0,Num_NaNs):
                    gap_location=list_of_gaps.index.values[i]+Index_correction
                    if j <=Num_previous_point:
                        Q.iloc[gap_location]=Q.iloc[gap_location-1]
                        Index_correction=Index_correction+1
                    else:
                        Q.iloc[gap_location]=Q.iloc[gap_location+Num_NaNs+1]
                        Index_correction=Index_correction+1
    gaps_location_2=np.argwhere(np.isnan(Q))
    if len(gaps_location)==0:
        pass
    elif len(gaps_location_2)==0:
        print('gaps are filled')
    else:
        print("there are still gaps")
        print(gaps_location_2)
    
    return Q
                
Q=fillgap(weather_data.loc[:,'PASCO_T'],12)
weather_data['PASCO_T']=Q
weather_data.to_csv('His_temp_wind.csv')
weather_data=weather_data.values
count=0
for i in range(0,len(weather_title)):
    weather_stats[i,:]=np.percentile(weather_data[:,i],[1,50,99])


np.savetxt('His_weather.csv',weather_data_hist,delimiter=',')

weather_data_hist=pd.read_csv('Synthetic_weather/WIND_TEMP.csv',header =0,index_col=0)
for i in weather_title:
    Q=fillgap(weather_data_hist.loc[:,i],12)
    weather_data_hist[i]=Q

weather_data_hist=weather_data_hist.values

#Generate matrix for storing the results
weather_stats_hist= np.zeros((len(weather_title),3))

for i in range(0,len(weather_title)):
    weather_stats_hist[i,:]=np.percentile(weather_data_hist[:,i],[1,50,99])

plt.figure()
plt.plot(weather_stats_hist,'o')
plt.plot(weather_stats,'x')

np.savetxt('His_weather_1_50_99.csv',weather_stats_hist,delimiter=',')

np.savetxt('syn_weather_1_50_99.csv',weather_stats,delimiter=',')

#Diff=weather_stats_hist- weather_stats
T_index=[0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32]


#for i in range(0,34):
#    if i in T_index:
#        for j in range(0,7):
#            if abs(Diff[i,j])<=0.5:
#                Diff[i,j]=0
#    else:
#        for j in range(0,7):
#            if abs(Diff[i,j])<=0.05 *(weather_stats_hist[i,j]):
#                Diff[i,j]=0
#        
##            
#Diff=pd.DataFrame(Diff)
#Diff.columns=[1,5,10,50,90,95,99]
#Diff.index=weather_title
#Diff.to_csv('Weather_difference.csv')
#
#
#PCT_Diff= Diff/ weather_stats_hist
#PCT_Diff.to_csv('Weather_difference_percentage.csv')
##
#
###############################################################################
#Streamflow convergence calculation
CA_his_streamflow=pd.read_excel('Synthetic_streamflows/CA_hist_streamflow.xlsx')
CA_syn_streamflow=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_CA.csv', header =0, index_col=0)


CA_streamflow_title=CA_syn_streamflow.columns



#Generate matrix for storing the results
streamflow_CA_stats_hist= np.zeros((len(CA_streamflow_title),3))
streamflow_CA_stats_syn= np.zeros((len(CA_streamflow_title),3))

count=0
for i in CA_streamflow_title:
    Q_syn=CA_syn_streamflow[i].values
    Q_his=CA_his_streamflow[i].values
    streamflow_CA_stats_hist[count,:]=np.percentile(Q_his,[1,50,99])
    streamflow_CA_stats_syn[count,:]=np.percentile(Q_syn,[1,50,99])
    count=count+1
    
plt.figure()
plt.plot(streamflow_CA_stats_syn,'o')
plt.plot(streamflow_CA_stats_hist,'x')
np.savetxt('CA_streamflow_his_1_50_99.csv',streamflow_CA_stats_hist,delimiter=',')
np.savetxt('CA_streamflow_syn_1_50_99.csv',streamflow_CA_stats_syn,delimiter=',')

#
#Diff_CA_streamflow=streamflow_CA_stats_syn-streamflow_CA_stats_hist
#
#
#for i in range(0,30):
#        for j in range(0,7):
#            if abs(Diff_CA_streamflow[i,j])<=0.05 *(streamflow_CA_stats_hist[i,j]):
#                Diff_CA_streamflow[i,j]=0
#        
#
#PCT_Diff_CA= Diff_CA_streamflow/ streamflow_CA_stats_hist
#
#
##

#PNW streamflow covergence

PNW_his_streamflow=pd.read_excel('Synthetic_streamflows/BPA_hist_streamflow.xlsx')
PNW_syn_streamflow=pd.read_csv('Synthetic_streamflows/synthetic_streamflows_FCRPS.csv', header =0, index_col=0)

PNW_his_streamflow=PNW_his_streamflow.values[:,3:]
PNW_syn_streamflow=PNW_syn_streamflow.values

streamflow_BPA_stats_hist= np.zeros((55,3))
streamflow_BPA_stats_syn= np.zeros((55,3))
for i in range(0,55):
    Q_syn=PNW_syn_streamflow[:,i]
    Q_his=PNW_his_streamflow[:,i]
    streamflow_BPA_stats_hist[i]=np.percentile(Q_his,[1,50,99])
    streamflow_BPA_stats_syn[i]=np.percentile(Q_syn,[1,50,99])
    
streamflow_BPA_stats_hist[47,:]=0
streamflow_BPA_stats_syn[47,:]=0
plt.figure()
plt.plot(streamflow_BPA_stats_syn,'o')
plt.plot(streamflow_BPA_stats_hist,'x')

np.savetxt('BPA_streamflow_his_1_50_99.csv',streamflow_BPA_stats_hist,delimiter=',')
np.savetxt('BPA_streamflow_syn_1_50_99.csv',streamflow_BPA_stats_syn,delimiter=',')

#