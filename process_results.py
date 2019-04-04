# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 10:40:05 2019

@author: YSu
"""


import pandas as pd
import numpy as np
import os
A=pd.read_csv('Total_emission_471.csv',compression='gzip')
B=pd.read_csv('CA_weighted_daily_prices123.csv',compression='gzip')
C=pd.read_csv('CA_other123.csv',compression='gzip')
bad=pd.read_csv('bad_index.csv',header=None)
#bad=pd.DataFrame(['s'])
re_run=[]
#55 to be re run
n=74
data_emission_total_CO2e=np.zeros(999-n)
data_emission_total_CO2=np.zeros(999-n)
data_emission_total_SO2=np.zeros(999-n)
data_emission_total_N2O=np.zeros(999-n)
data_emission_total_NOX=np.zeros(999-n)
data=np.zeros((364,999-n))
count=0

year_info=[]
#now we have years of runs. But we have some missing
for i in range(0,999):
    if i in bad[0].values:
        pass
    else:
        try:
            name='data_' + str(i)
            path='CA_weighted_daily_prices' + str(i) +'.csv'
            locals()[name]=pd.read_csv(path,header=0,compression='gzip')
            a=locals()[name].loc[:]['CAISO'].values
            data[:,count]=a
    
    #        
            
            name='data_' + str(i)
            path='Total_emission_' +str(i) + '.csv'
            locals()[name]=pd.read_csv(path,header=0, compression='gzip')
            a=locals()[name].loc[:]['Total CO2 equivelent lb'].values *0.0005
            b=locals()[name].loc[:]['Total CO2 lb'].values *0.0005
            c=locals()[name].loc[:]['Total SO2 lb'].values *0.0005
            d=locals()[name].loc[:]['Total N2O lb'].values *0.0005
            e=locals()[name].loc[:]['Total NOX lb'].values *0.0005
            data_emission_total_CO2e[count]=a
            data_emission_total_CO2[count]=b
            data_emission_total_SO2[count]=c
            data_emission_total_N2O[count]=d
            data_emission_total_NOX[count]=e  
            count=count+1
    #        mydir='D:\OneDrive - University of North Carolina at Chapel Hill\CA_INFEWs\Historical_Runs\Results'
    #        mydir_temp=mydir+ '/'+ str(i)
    #        mydir_new = os.chdir(mydir_temp) # change the current working directory
    #        os.system('python CA_price_calculation.py')
            
            print(i)
            year_info.append(i)
    
    
        except FileNotFoundError:
            re_run.append(i)

np.savetxt('all_data.csv',data,delimiter=',')
np.savetxt('year_list.csv',year_info,delimiter=',')


data_emission_total_CO2=data_emission_total_CO2/1000000
data_emission_total_CO2e=data_emission_total_CO2e/1000000
data_emission_total_N2O=data_emission_total_N2O
data_emission_total_NOX=data_emission_total_NOX
data_emission_total_SO2=data_emission_total_SO2

emission_data=pd.DataFrame()
emission_data['CO2']=data_emission_total_CO2
emission_data['CO2e']=data_emission_total_CO2e
emission_data['N2O']=data_emission_total_N2O
emission_data['NOX']=data_emission_total_NOX
emission_data['SO2']=data_emission_total_SO2

emission_data.to_csv('Emission_data.csv')

import matplotlib.pyplot as plt


data=data[:,:914]
reshaped_data=np.reshape(data,(364*914))

mins = data.min(1)
maxes = data.max(1)
means = data.mean(1)
perc=np.zeros((2,364))
for i in range(0,364):
    
    perc[0,i]=means[i]-np.percentile(data[:,i],25)
    perc[1,i]=np.percentile(data[:,i],75)-means[i]

std = data.std(1)




########
#Find all the bad runs
bad_index=np.argwhere(data>150)
AAA=data[bad_index[:,0],bad_index[:,1]]

np.savetxt('bad_index.csv',bad_index,delimiter=',')

#



average_price=np.average(data,axis=0)
highest=np.argmax(average_price)
lowest=np.argmin(average_price)

data_emission_total_CO2[highest]
data_emission_total_CO2[lowest]
data_emission_total_N2O[highest]
data_emission_total_SO2[highest]
data_emission_total_NOX[highest]

np.argmax(data_emission_total_CO2)
np.argmax(data_emission_total_CO2e)
np.argmax(data_emission_total_N2O)
np.argmax(data_emission_total_NOX)
np.argmax(data_emission_total_SO2)



np.argmin(data_emission_total_CO2)
np.argmin(data_emission_total_CO2e)
np.argmin(data_emission_total_N2O)
np.argmin(data_emission_total_NOX)
np.argmin(data_emission_total_SO2)
########

import seaborn as sns; sns.set(color_codes=True)

plt.figure()
plt.style.use('fivethirtyeight')
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams['font.size']=12

plt.subplots()
plt.plot(means,'k',label='Average price')
plt.errorbar(np.arange(364), means, perc, fmt='.k',ecolor='red',lw=3,label='Interquatile range')
plt.errorbar(np.arange(364), means, [means - mins, maxes - means],
             fmt='.k', ecolor='orange', lw=1,label='max min')
plt.plot(data[:,highest],label='Highest average year',linestyle='-',linewidth=3,color='blue',alpha=0.5)
plt.plot(data[:,lowest],label='Lowest average year',linestyle='-',linewidth=3,color='green',alpha=0.5)
plt.xlim(-1, 365)
plt.ylim(25,85)
plt.xlabel('Day of the year')
plt.ylabel('Price $/MWH')
#plt.legend(bbox_to_anchor=(0.3, -0.6, 0.5, 0.5),loc='center',ncol=5)

#plt.subplot2grid((3,2),(1,0))
n, bins, patches=plt.hist(data_emission_total_CO2e[:915],13,color='blue',density=True)
sns.kdeplot(data_emission_total_CO2e[:915])
#patches[-1].set_facecolor('blue')
#patches[0].set_facecolor('green')
#
plt.xlabel('CO2 equivelent million ton')
plt.ylabel('Frequency')
plt.title('CO2 emission from power sector')
#
#plt.subplot2grid((3,2),(1,1))
#n, bins, patches=plt.hist(data_emission_total_N2O,13,color='orange')
#plt.xlabel('N2O equivelent ton')
#plt.ylabel('Frequency')
#patches[-1].set_facecolor('blue')
#patches[0].set_facecolor('green')
#
#plt.subplot2grid((3,2),(2,0))
#n, bins, patches=plt.hist(data_emission_total_NOX,13,color='orange')
#plt.xlabel('NOX equivelent ton')
#plt.ylabel('Frequency')
#patches[-1].set_facecolor('blue')
#patches[0].set_facecolor('green')
#
#plt.subplot2grid((3,2),(2,1))
#n, bins, patches=plt.hist(data_emission_total_SO2,13,color='orange')
#patches[4].set_facecolor('blue')
#patches[0].set_facecolor('green')
#plt.xlim(150,400)
#plt.xlabel('SO2 equivelent ton')
#plt.ylabel('Frequency')
#plt.tight_layout()