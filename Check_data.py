# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:26:12 2019

@author: YSu
"""

from __future__ import division
import pandas as pd
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
Solar=pd.read_excel('Synthetic_solar_power/solar_power_sim.xlsx',header=0).loc[:,'CAISO']
Solar_matrix=Solar.as_matrix()

CA_Hydro=CA_Hydro_PGE.values+CA_Hydro_SCE.values
CA_Hydro=CA_Hydro/24

y=int(len(CA_Hydro)/365)
#yearly_CA_Hydro=np.zeros(46)
#daily_load_path=np.zeros((36546,16))
daily_solar=np.zeros(y*365)
daily_wind=np.zeros((y*365))

for i in range(0,y*365):
#    yearly_CA_Hydro[i]=sum(CA_Hydro[i*52+0:i*52+52])/24
#    yearly_load_path[i,:]=np.sum(load_path_matrix[i*365+0:i*365+365,:],axis=0)
    daily_solar[i]=np.sum(Solar_matrix[i*24+0:i*24+24])
    daily_wind[i]=np.sum(wind_matrix[i*24+0:i*24+24],axis=0)
    

#yearly_load_path[:,11]=yearly_load_path[:,11]/24

daily_load_agg=np.sum(load_path_matrix[:,2:6],axis=1)
daily_path_agg=np.sum(load_path_matrix[:,9:],axis=1)
pathg=load_path_matrix[:,9:]
daily_renewable=(daily_wind+daily_solar)/24


net_load=daily_load_agg-daily_renewable-CA_Hydro-daily_path_agg
np.savetxt('Oringial_constructed_matrix.csv',daily_load_agg,delimiter=',')

re_constructed=pd.read_csv('re_constructed_matrix_netload.csv',header=None)
re_constructed_load=pd.read_csv('re_constructed_matrix_load.csv',header=None)
re_constructed_hydro=pd.read_csv('re_constructed_matrix_hydro.csv',header=None)
re_constructed_import=pd.read_csv('re_constructed_matrix_import.csv',header=None)
re_constructed_renewable=pd.read_csv('re_constructed_matrix_renewable.csv',header=None)

re_constructed_weaker=pd.read_csv('re_constructed_weaker_matrix_netload.csv',header=None)
re_constructed_load_weaker=pd.read_csv('re_constructed_weaker_matrix_load.csv',header=None)
re_constructed_hydro_weaker=pd.read_csv('re_constructed_weaker_matrix_hydro.csv',header=None)
re_constructed_import_weaker=pd.read_csv('re_constructed_weaker_matrix_import.csv',header=None)
re_constructed_renewable_weaker=pd.read_csv('re_constructed_weaker_matrix_renewable.csv',header=None)

re_constructed_stronger=pd.read_csv('re_constructed_stronger_matrix_netload.csv',header=None)
re_constructed_load_stronger=pd.read_csv('re_constructed_stronger_matrix_load.csv',header=None)
re_constructed_hydro_stronger=pd.read_csv('re_constructed_stronger_matrix_hydro.csv',header=None)
re_constructed_import_stronger=pd.read_csv('re_constructed_stronger_matrix_import.csv',header=None)
re_constructed_renewable_stronger=pd.read_csv('re_constructed_stronger_matrix_renewable.csv',header=None)


fig1,ax1=plt.subplots()
#ax1.hist(net_load,bins=300,rwidth=0.7,histtype='step',label='Historical Covariance')
ax1.hist(re_constructed.values,bins=300,rwidth=0.7,histtype='step',label='Reconstructed')
ax1.hist(re_constructed_weaker.values,bins=300,rwidth=0.7,histtype='step',label='Weaker')
ax1.hist(re_constructed_stronger.values,bins=300,rwidth=0.7,histtype='step',label='Stronger')
ax1.legend()
ax1.set_title('Netload')
fig1.savefig('Netload.png')



fig2,ax2=plt.subplots()
#ax2.hist(daily_load_agg,bins=300,rwidth=0.7,histtype='step',label='Historical Covariance')
ax2.hist(re_constructed_load.values,bins=300,rwidth=0.7,histtype='step',label='Reconstructed')
ax2.hist(re_constructed_load_weaker.values,bins=300,rwidth=0.7,histtype='step',label='Weaker')
ax2.hist(re_constructed_load_stronger.values,bins=300,rwidth=0.7,histtype='step',label='Stronger')
ax2.legend()
ax2.set_title('Load')
fig2.savefig('Load.png')


fig3,ax3=plt.subplots()
#ax3.hist(daily_renewable,bins=300,rwidth=0.7,histtype='step',label='Historical Covariance')
ax3.hist(re_constructed_renewable.values,bins=300,rwidth=0.7,histtype='step',label='Reconstructed')
ax3.hist(re_constructed_renewable_weaker.values,bins=300,rwidth=0.7,histtype='step',label='Weaker')
ax3.hist(re_constructed_renewable_stronger.values,bins=300,rwidth=0.7,histtype='step',label='Stronger')

ax3.legend()
ax3.set_title('Renewable')
fig3.savefig('Renewable.png')


fig4,ax4=plt.subplots()
#ax4.hist(CA_Hydro,bins=300,rwidth=0.7,histtype='step',label='Historical Covariance')
ax4.hist(re_constructed_hydro.values,bins=300,rwidth=0.7,histtype='step',label='Reconstructed')
ax4.hist(re_constructed_hydro_weaker.values,bins=300,rwidth=0.7,histtype='step',label='Weaker')
ax4.hist(re_constructed_hydro_stronger.values,bins=300,rwidth=0.7,histtype='step',label='Stronger')

ax4.legend()
ax4.set_title('Hydro')
fig4.savefig('Hydro.png')

fig5,ax5=plt.subplots()
#ax5.hist(daily_path_agg,bins=300,rwidth=0.7,histtype='step',label='Historical Covariance')
ax5.hist(re_constructed_import.values,bins=300,rwidth=0.7,histtype='step',label='Reconstructed')
ax5.hist(re_constructed_import_weaker.values,bins=300,rwidth=0.7,histtype='step',label='Weaker')
ax5.hist(re_constructed_import_stronger.values,bins=300,rwidth=0.7,histtype='step',label='Stronger')

ax5.legend()
ax5.set_title('Import')
fig5.savefig('Import.png')