# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 16:14:19 2019

@author: YSu
"""

import pandas as pd

A=pd.read_csv('PNW_sim_daily_prices231.csv',compression='gzip')
B=pd.read_csv('PNW_sim_hourly_prices231.csv',compression='gzip')
C=pd.read_csv('PNW_Compacted_result231.csv',compression='gzip')

E=pd.read_csv('CA_Compacted_result231.csv',compression='gzip')

D=C.loc[C.loc[:,'Time']==65]
