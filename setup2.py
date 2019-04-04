
"""
Created on Tue Dec  4 14:20:33 2018

@author: YSu
"""

import os
from shutil import copy

for run in range(1,21):

#    path=os.getcwd()+'\\' + str(run)
#    os.makedirs(path,exist_ok=True)
    update='demand_pathflows.py'
    path=os.getcwd()+'\\' + str(run)+'\\'+'Syn'
    copy(update,path)