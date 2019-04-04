# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 21:31:28 2019

@author: YSu
"""


import pandas as pd
import statsmodels.distributions.empirical_distribution as edis
import numpy as np

Q=pd.read_csv('re_constructed_matrix_netload.csv',header=None)
Q=Q.values

Q_stronger=pd.read_csv('re_constructed_stronger_matrix_netload.csv',header=None).values

Q_weaker=pd.read_csv('re_constructed_weaker_matrix_netload.csv',header=None).values

def Covariance_valuation(data):

    x,y=np.shape(data)
 #data is the data matrix at all time step. The dimention would be X*Y    
 #data 2 is required if calculating disimilarity

#Step 1: Transform the data into emperical CDF 
    P=np.zeros((x,y))
    for i in range(0,y):
        ECDF=edis.ECDF(data[:,i])
        P[:,i]=ECDF(data[:,i])
#Step 2: Transform the ECDF into a uniform distribution
    Y=2*(P-0.5)
#Calculate different indcies
#M is surfeit index which is the mean state of the system    
    M=1/y*np.sum(Y,axis=1)
#S is the severity index showing systemwide how extreme the states are
    S=1/y*np.sum(np.abs(Y),axis=1)
#D measures how dissimilar the states of all sites are with rescpect to each other
    D1=np.zeros((x,y-1))
    D2=np.zeros((x,y))
    for i in range(0,y-1):
        for j in range(i+1,y):
            D2[:,j]=np.abs(Y[:,i]-Y[:,j])
        D1[:,i]=np.sum(D2,axis=1)
    D=1/y**2*np.sum(D1,axis=1)
    
    return M,S,D 


A=edis.ECDF(Q[:,0])
B=edis.ECDF(Q_stronger[:,0])
C=edis.ECDF(Q_weaker[:,0])


import matplotlib.pyplot as plt

#Temperature
fig,ax=plt.subplots()
ax.hist(Q,bins=300,histtype='step',label='Reconstruct')
ax.hist(Q_stronger,bins=300,histtype='step',label='Stronger')
ax.hist(Q_weaker,bins=300,histtype='step',label='Weaker')
fig.legend()
ax.set_title('Histgram')
fig.savefig('Netload_PDF.png')
#


fig2,ax2=plt.subplots()
ax2.plot(A.x,A.y,label='Reconstruct')
ax2.plot(B.x,B.y,label='Stronger')
ax2.plot(C.x,C.y,label='Weaker')
fig2.legend()
ax2.set_title('CDF')
fig2.savefig('Netload_CDF.png')
#fig2,ax2=plt.subplots()
#ax2.hist(A[2],bins=300,histtype='step',label='Reconstruct')
#ax2.hist(B[2],bins=300,histtype='step',label='Stronger')
#ax2.hist(C[2],bins=300,histtype='step',label='Weaker')
#fig2.legend()
#ax2.set_title('Mean state')
#fig2.savefig('Meanstate_Temp.png')
#
#
#fig3,ax3=plt.subplots()
#ax3.hist(A,bins=300,histtype='step',label='Reconstruct')
#ax3.hist(B[0],bins=300,histtype='step',label='Stronger')
#ax3.hist(C[0],bins=300,histtype='step',label='Weaker')
#fig3.legend()
#ax3.set_title('Dissimilarity')
#fig3.savefig('Dissimilarity_Temp.png')