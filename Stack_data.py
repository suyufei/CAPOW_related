# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 13:39:53 2018

@author: YSu
"""

import pandas as pd
import os
import numpy as np

All_weather=[]
All_hydro=[]
All_hydro_PNW=[]
All_hydro_PNW2=[]
Wind_Power=[]
All_Solar=[]
All_Load_Path=[]
All_Load_Path2=[]
All_Gas=[]


Syn_streamflow_CA=[]
Syn_streamflow_BPA=[]

for i in range(1,7):

    path=os.getcwd()+'\\' + str(i)+'\\'+'Syn\\'

    #Weather
    Weather_file= path +'Synthetic_weather/synthetic_weather_data.csv'
    read_file=pd.read_csv(Weather_file,header=0,index_col=0)
    Weather_title = list(read_file)
    read_file=read_file.values
    All_weather.append(read_file)
    
    
    #Stremflow data
    
    Streamflow_CA_file= path +'Synthetic_streamflows/synthetic_streamflows_CA.csv'
    read_file=pd.read_csv(Streamflow_CA_file,header=0,index_col=0)
    CA_streamflow_title = list(read_file)
    read_file=read_file.values
    Syn_streamflow_CA.append(read_file)
    
    Streamflow_BPA_file= path +'Synthetic_streamflows/synthetic_streamflows_FCRPS.csv'
    read_file=pd.read_csv(Streamflow_BPA_file,header=None)
    read_file=read_file.values
    Syn_streamflow_BPA.append(read_file)
    
    
    #Hydropower CA
    Hydro_file= path + 'CA_hydropower/CA_hydro_daily.xlsx'
    read_file=pd.read_excel(Hydro_file,header=0,index_col=0)
    Hydro_title = list(read_file)
    read_file=read_file.values
    All_hydro.append(read_file)
    
    #Hydropower PNW

    Hydro_file= path + 'PNW_hydro/FCRPS/Modeled_BPA_dams.csv'
    read_file=pd.read_csv(Hydro_file,header=None)
    read_file=read_file.values
    All_hydro_PNW.append(read_file)

    Hydro_file= path + 'PNW_hydro/PNW_hydro_daily.xlsx'
    read_file=pd.read_excel(Hydro_file,header=0,index_col=0)
    read_file=read_file.values
    All_hydro_PNW2.append(read_file)
    
    #Wind Power
    
    Wind_file= path + 'Synthetic_wind_power/wind_power_sim.csv'
    read_file=pd.read_csv(Wind_file,header=0,index_col=0)
    read_file=read_file.values
    Wind_Power.append(read_file)

    #Solar Power
    
    Solar_file= path + 'Synthetic_solar_power/solar_power_sim.csv'
    read_file=pd.read_csv(Solar_file,header=0,index_col=0)
    read_file=read_file.values
    All_Solar.append(read_file)
    
    #Demand and Path
    Load_Path_file2= path +  'Synthetic_demand_pathflows/Load_Path_Sim.csv'
    read_file=pd.read_csv(Load_Path_file2,header=0,index_col=0)
    Load_Path_title = list(read_file)
    read_file=read_file.values
    All_Load_Path2.append(read_file)
   
    Load_Path_file= path + 'Synthetic_demand_pathflows/Sim_hourly_load.csv'
    read_file=pd.read_csv(Load_Path_file,header=0,index_col=0)
    read_file=read_file.values
    All_Load_Path.append(read_file)
    
    #Gas
    Gas_file= path + 'Gas_prices/NG.xlsx'
    read_file=pd.read_excel(Gas_file,header=0,index_col=0)
    read_file=read_file.values
    All_Gas.append(read_file)
    print(i)
    



All_weather=np.vstack(All_weather)
weather= pd.DataFrame(All_weather)
weather.columns = Weather_title    
weather.to_csv('Synthetic_weather/synthetic_weather_data.csv')


All_hydro=np.vstack(All_hydro)    
Hydro = pd.DataFrame(All_hydro)
Hydro.columns = ['PGE_valley','SCE']
Hydro.to_excel('CA_hydropower/CA_hydro_daily.xlsx')
#Orgnize weather data

All_hydro_PNW=np.vstack(All_hydro_PNW)
PNW_Hydro=np.savetxt('PNW_hydro/FCRPS/Modeled_BPA_dams.csv',All_hydro_PNW,delimiter=',')

All_hydro_PNW2=np.vstack(All_hydro_PNW2)
PNW_daily = pd.DataFrame(All_hydro_PNW2)
PNW_daily.columns = ['PNW']
PNW_daily.to_excel('PNW_hydro/PNW_hydro_daily.xlsx')

Wind_Power=np.vstack(Wind_Power)
Wind_Power_result = pd.DataFrame(Wind_Power)
Wind_Power_result.columns = ['BPA','PNW','CAISO']
Wind_Power_result.to_csv('Synthetic_wind_power/wind_power_sim.csv')


All_Solar=np.vstack(All_Solar)
Solar_Power = pd.DataFrame(All_Solar)
Solar_Power.columns = ['CAISO']
Solar_Power.to_csv('Synthetic_solar_power/solar_power_sim.csv')


All_Load_Path2=np.vstack(All_Load_Path2)
df_Load = pd.DataFrame(All_Load_Path2)
df_Load.columns = Load_Path_title
df_Load.to_csv('Synthetic_demand_pathflows/Load_Path_Sim.csv')


All_Load_Path=np.vstack(All_Load_Path)
df_Load = pd.DataFrame(All_Load_Path)
df_Load.columns = ['BPA','PNW','SDGE','SCE','PGE_valley','PGE_bay']
df_Load.to_csv('Synthetic_demand_pathflows/Sim_hourly_load.csv')


All_Gas=np.vstack(All_Gas)
NG = pd.DataFrame(All_Gas)
NG.columns = ['SCE','SDGE','PGE_valley','PGE_bay','PNW']
NG.to_excel('Gas_prices/NG.xlsx')

Syn_streamflow_CA=np.vstack(Syn_streamflow_CA)
CA_syn=pd.DataFrame(Syn_streamflow_CA)
CA_syn.columns=CA_streamflow_title
CA_syn.to_csv('Synthetic_streamflows/synthetic_streamflows_CA.csv')


Syn_streamflow_BPA=np.vstack(Syn_streamflow_BPA)
BPA_syn=pd.DataFrame(Syn_streamflow_BPA)
BPA_syn.to_csv('Synthetic_streamflows/synthetic_streamflows_FCRPS.csv')