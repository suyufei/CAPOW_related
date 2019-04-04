# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:16:51 2019

@author: YSu
"""

import pandas as pd
import numpy as np

#149 is bad. skip for now

badfile=[]

for i in range(170,171):
    try:
        path= str(i) + '//UCED//'
        
        
    #######################################################################
    
    #CA
        
        d1=pd.read_csv(path+'CAISO\Mwh_1.csv',header=0)
        d2=pd.read_csv(path+'CAISO\mwh_2.csv',header=0)
        d3=pd.read_csv(path+'CAISO\mwh_3.csv',header=0)
        emission=pd.read_csv(path+'Emission_calculation.csv',header=0)
        Results=emission
        
            #Annual emission
        Total_NOX= np.sum(Results.loc[:]['NOX lb'].values)
        Total_SO2= np.sum(Results.loc[:]['SO2 lb'].values)
        Total_CO2= np.sum(Results.loc[:]['CO2 lb'].values)
        Total_N2O= np.sum(Results.loc[:]['N2O lb'].values)
        Total_CO2_e= np.sum(Results.loc[:]['CO2_equivelent lb'].values)
        
        Annual_total=pd.DataFrame()
        Annual_total.loc[1,'Total NOX lb']=Total_NOX
        Annual_total.loc[1,'Total N2O lb']=Total_N2O
        Annual_total.loc[1,'Total CO2 lb']=Total_CO2
        Annual_total.loc[1,'Total CO2 equivelent lb'] = Total_CO2_e
        Annual_total.loc[1,'Total SO2 lb']=Total_SO2
        
        store_path='Total_emission_' + str(i) + '.csv'
    
        Annual_total.to_csv(store_path,compression='gzip')
        
        
        big_result=pd.DataFrame()
        big_result['Generator']=d1['Generator']
        big_result['Time']=d1['Time']
        big_result['Zones']=d1['Zones']
        big_result['Type']=d1['Type']
        big_result['mwh_1']=d1['Value']
        big_result['mwh_2']=d2['Value']
        big_result['mwh_3']=d3['Value']
        big_result['mwh_1 $/MWh']=d1['$/MWh']
        big_result['mwh_2 $/MWh']=d2['$/MWh']
        big_result['mwh_3 $/MWh']=d3['$/MWh']
        big_result['NOX lb']=emission['NOX lb']
        big_result['SO2 lb']=emission['SO2 lb']
        big_result['CO2 lb']=emission['CO2 lb']
        big_result['N2O lb']=emission['N2O lb']
        big_result['CO2_equivelent lb']=emission['CO2_equivelent lb']
        
        store_path='CA_Compacted_result' + str(i) + '.csv'
        big_result.to_csv(store_path,compression='gzip')
        
        
        solar=pd.read_csv(path+'CAISO\solar_out.csv',header=0)
        wind=pd.read_csv(path+'CAISO\wind_out.csv',header=0)
        renewable=pd.DataFrame()
        renewable['Zone']=wind['Zone']
        renewable['Time']=wind['Time']
        renewable['Wind']=wind['Value']
        renewable['Solar']=solar['Value']
        store_path='CA_renewable' + str(i) + '.csv'
        renewable.to_csv(store_path,compression='gzip')
        
        
        flow=pd.read_csv(path+'CAISO\\flow.csv',header=0)
        store_path='CA_flow' + str(i) + '.csv'
        flow.to_csv(store_path,compression='gzip')
        
        
        
        
        nrsv=pd.read_csv(path+'CAISO\\nrsv.csv',header=0)
        srsv=pd.read_csv(path+'CAISO\srsv.csv',header=0)
        on=pd.read_csv(path+'CAISO\on.csv',header=0)
        switch=pd.read_csv(path+'CAISO\switch.csv',header=0)
        other=pd.DataFrame()
        other['Generator']=nrsv['Generator']
        other['Time']=nrsv['Time']
        other['Zones']=nrsv['Zones']
        other['NRSV']=nrsv['Value']
        other['SRSV']=srsv['Value']
        other['On']=on['Value']
        other['Switch']=switch['Value']
        store_path='CA_other' + str(i) + '.csv'
        other.to_csv(store_path,compression='gzip')
        
        sim_price_daily=pd.read_excel(path+'CAISO\\sim_daily_prices.xlsx',header=0)
        store_path='CA_sim_daily_prices' + str(i) + '.csv'
        sim_price_daily.to_csv(store_path,compression='gzip')
        
        sim_price_houyrly=pd.read_excel(path+'CAISO\\sim_hourly_prices.xlsx',header=0)
        store_path='CA_sim_hourly_prices' + str(i) + '.csv'
        sim_price_houyrly.to_csv(store_path,compression='gzip')
        
        
        weight_price_daily=pd.read_excel(path+'CAISO\\weighted_daily_prices.xlsx',header=0)
        store_path='CA_weighted_daily_prices' + str(i) + '.csv'
        weight_price_daily.to_csv(store_path,compression='gzip')
        
        weight_price_houyrly=pd.read_excel(path+'CAISO\\weighted_hourly_prices.xlsx',header=0)
        store_path='CA_weighted_hourly_prices' + str(i) + '.csv'
        weight_price_houyrly.to_csv(store_path,compression='gzip')
        
    #########################################################################################
        d1PNW=pd.read_csv(path+'PNW\Mwh_1.csv',header=0)
        d2PNW=pd.read_csv(path+'PNW\mwh_2.csv',header=0)
        d3PNW=pd.read_csv(path+'PNW\mwh_3.csv',header=0)
    
        
        big_resultPNW=pd.DataFrame()
        big_resultPNW['Generator']=d1['Generator']
        big_resultPNW['Time']=d1['Time']
        big_resultPNW['Zones']=d1['Zones']
        big_resultPNW['Type']=d1['Type']
        big_resultPNW['mwh_1']=d1['Value']
        big_resultPNW['mwh_2']=d2['Value']
        big_resultPNW['mwh_3']=d3['Value']
        big_resultPNW['mwh_1 $/MWh']=d1['$/MWh']
        big_resultPNW['mwh_2 $/MWh']=d2['$/MWh']
        big_resultPNW['mwh_3 $/MWh']=d3['$/MWh']
    
        
        store_path='PNW_Compacted_result' + str(i) + '.csv'
        big_resultPNW.to_csv(store_path,compression='gzip')
        
        
        solarPNW=pd.read_csv(path+'PNW\solar_out.csv',header=0)
        windPNW=pd.read_csv(path+'PNW\wind_out.csv',header=0)
        renewablePNW=pd.DataFrame()
        renewablePNW['Zone']=wind['Zone']
        renewablePNW['Time']=wind['Time']
        renewablePNW['Wind']=wind['Value']
        renewablePNW['Solar']=solar['Value']
        store_path='PNW_renewable' + str(i) + '.csv'
        renewablePNW.to_csv(store_path,compression='gzip')
           
        
        
        nrsvPNW=pd.read_csv(path+'PNW\\nrsv.csv',header=0)
        srsvPNW=pd.read_csv(path+'PNW\srsv.csv',header=0)
        onPNW=pd.read_csv(path+'PNW\on.csv',header=0)
        switchPNW=pd.read_csv(path+'PNW\switch.csv',header=0)
        otherPNW=pd.DataFrame()
        otherPNW['Generator']=nrsv['Generator']
        otherPNW['Time']=nrsv['Time']
        otherPNW['Zones']=nrsv['Zones']
        otherPNW['NRSV']=nrsv['Value']
        otherPNW['SRSV']=srsv['Value']
        otherPNW['On']=on['Value']
        otherPNW['Switch']=switch['Value']
        store_path='PNW_other' + str(i) + '.csv'
        otherPNW.to_csv(store_path,compression='gzip')
        
        sim_price_dailyPNW=pd.read_csv(path+'PNW\\sim_daily_prices.csv',header=0)
        store_path='PNW_sim_daily_prices' + str(i) + '.csv'
        sim_price_dailyPNW.to_csv(store_path,compression='gzip')
        
        sim_price_houyrlyPNW=pd.read_csv(path+'PNW\\sim_hourly_prices.csv',header=0)
        store_path='PNW_sim_hourly_prices' + str(i) + '.csv'
        sim_price_houyrlyPNW.to_csv(store_path,compression='gzip')
        print(i)
    except FileNotFoundError:
        badfile.append(i)
        print(str(i) +'bad')
    
    
