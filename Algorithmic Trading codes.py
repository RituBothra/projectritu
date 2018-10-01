# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 15:13:36 2018

@author: Ritu
"""

import pandas as pd
import numpy as np
from io import StringIO
import os
import matplotlib.pyplot as plt

data_HDFC=pd.read_csv("D:\\Algo trading banks\\HDFC.csv",header=0)
data_ICICI=pd.read_csv("D:\\Algo trading banks\\ICICI.csv",header=0)
data_Axis=pd.read_csv("D:\\Algo trading banks\\Axis.csv",header=0)
data_SBI=pd.read_csv("D:\\Algo trading banks\\SBI.csv",header=0)
data_KotakMahindra=pd.read_csv("D:\\Algo trading banks\\Kotak Mahindra.csv",header=0)
data_YES=pd.read_csv("D:\\Algo trading banks\\YES.csv",header=0)
data_Pnb=pd.read_csv("D:\\Algo trading banks\\Pnb.csv",header=0)


data=pd.concat([data_HDFC.Date,data_HDFC.Close,data_ICICI.Close,data_Axis.Close,data_SBI.Close,data_KotakMahindra.Close,data_YES.Close,data_Pnb.Close],axis=1)
#rsi
window_length = 14
for i in range(1,8):
    close = data.iloc[:,i]
    delta = close.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = pd.stats.moments.ewma(up, window_length)
    roll_down1 = pd.stats.moments.ewma(down.abs(), window_length)
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    data['RSI_'+str(i)]=RSI1
    
#bollinger
for i in range(1,8):
    MA = data.iloc[:,i].rolling(window=20).mean()
    SD = data.iloc[:,i].rolling(window=20).std()
    data['MA'+str(i)]=MA
    data['Upper_'+str(i)] = MA + (2 * SD) 
    data['Lower_'+str(i)] = MA - (2 * SD)

#bollinger graph
bolli_HDFC=pd.concat([data.iloc[:,1],data.MA1,data.Upper_1,data.Lower_1],axis=1).plot(figsize=(15,7))
bolli_ICICI=pd.concat([data.iloc[:,2],data.MA2,data.Upper_2,data.Lower_2],axis=1).plot(figsize=(15,7))
bolli_Axis=pd.concat([data.iloc[:,3],data.MA3,data.Upper_3,data.Lower_3],axis=1).plot(figsize=(15,7))
bolli_SBI=pd.concat([data.iloc[:,4],data.MA4,data.Upper_4,data.Lower_4],axis=1).plot(figsize=(15,7))
bolli_KotakMahindra=pd.concat([data.iloc[:,5],data.MA5,data.Upper_5,data.Lower_5],axis=1).plot(figsize=(15,7))
bolli_YES=pd.concat([data.iloc[:,6],data.MA6,data.Upper_6,data.Lower_6],axis=1).plot(figsize=(15,7))
bolli_Pnb=pd.concat([data.iloc[:,7],data.MA7,data.Upper_7,data.Lower_7],axis=1).plot(figsize=(15,7))

#rsi graph
rsi_HDFC=data.RSI_1.plot(figsize=(15,7))
rsi_ICICI=data.RSI_2.plot(figsize=(15,7))
rsi_Axis=data.RSI_3.plot(figsize=(15,7))
rsi_SBI=data.RSI_4.plot(figsize=(15,7))
rsi_KotakMahindra=data.RSI_5.plot(figsize=(15,7))
rsi_YES=data.RSI_6.plot(figsize=(15,7))
rsi_Pnb=data.RSI_7.plot(figsize=(15,7))


#buy-sell by bollinger graph
Upper_touch= pd.DataFrame(0, index=range(743), columns=range(7))
Upper_touch.columns = ['HDFC_sell','ICICI_sell','Axis_sell','SBI_sell','KotakMahindra_sell','YES_sell','Pnb_sell']
for j in range(1,8):
    for i in range (0,743):
        if(data.iloc[i,j]>data['Upper_'+str(j)][i]):
            Upper_touch.iloc[i,j]=data.iloc[i,j]

lower_touch= pd.DataFrame(0, index=range(743), columns=range(7))
lower_touch.columns = ['HDFC_buy','ICICI_buy','Axis_buy','SBI_buy','KotakMahindra_buy','YES_buy','Pnb_buy']
for j in range(1,8):
    for i in range (0,743):
        if(data.iloc[i,j]<data['Lower_'+str(j)][i]):
            lower_touch.iloc[i,j]=data.iloc[i,j]        

#buy-sell by bollinger+rsi graphs
Upper_touch_b= pd.DataFrame(0, index=range(743), columns=range(8))
Upper_touch_b.iloc[:,0]=data['Date']
Upper_touch_b.columns = ['HDFC_sell','ICICI_sell','Axis_sell','SBI_sell','KotakMahindra_sell','YES_sell','Pnb_sell']
for j in range(1,8):
    for i in range (0,743):
        if(data.iloc[i,j]>data['Upper_'+str(j)][i] and data.iloc[i+1,j]<data['Upper_'+str(j)][i+1] and data['RSI_'+str(j)][i]>70):
            Upper_touch_b.iloc[i,j]=data.iloc[i,j]

lower_touch_b= pd.DataFrame(0, index=range(743), columns=range(8))
lower_touch_b.iloc[:,0]=data['Date']
lower_touch_b.columns = ['HDFC_buy','ICICI_buy','Axis_buy','SBI_buy','KotakMahindra_buy','YES_buy','Pnb_buy']
for j in range(1,8):
    for i in range (0,743):
        if(data.iloc[i,j]<data['Lower_'+str(j)][i] and data['RSI_'+str(j)][i]<40):
            lower_touch_b.iloc[i,j]=data.iloc[i,j]



HDFC=pd.concat([lower_touch_b.date_buy,lower_touch_b.HDFC_buy,Upper_touch_b.HDFC_sell],axis=1)
ICICI=pd.concat([lower_touch_b.date_buy,lower_touch_b.ICICI_buy,Upper_touch_b.ICICI_sell],axis=1)
Axis=pd.concat([lower_touch_b.date_buy,lower_touch_b.Axis_buy,Upper_touch_b.Axis_sell],axis=1)
SBI=pd.concat([lower_touch_b.date_buy,lower_touch_b.SBI_buy,Upper_touch_b.SBI_sell],axis=1)
KotakMahindra=pd.concat([lower_touch_b.date_buy,lower_touch_b.KotakMahindra_buy,Upper_touch_b.KotakMahindra_sell],axis=1)
YES=pd.concat([lower_touch_b.date_buy,lower_touch_b.YES_buy,Upper_touch_b.YES_sell],axis=1)
Pnb=pd.concat([lower_touch_b.date_buy,lower_touch_b.pnb_buy,Upper_touch_b.Pnb_sell],axis=1)

#final dataframe to show buy-sell dates and stock prices
HDFC=HDFC[(HDFC.HDFC_buy+HDFC.HDFC_sell)!=0]
ICICI=ICICI[(ICICI.ICICI_buy+ICICI.ICICI_sell)!=0]
Axis=Axis[(Axis.Axis_buy+Axis.Axis_sell)!=0]
SBI=SBI[(SBI.SBI_buy+SBI.SBI_sell)!=0]
KotakMahindra=KotakMahindra[(KotakMahindra.KotakMahindra_buy+KotakMahindra.KotakMahindra_sell)!=0]
YES=YES[(YES.YES_buy+YES.YES_sell)!=0]
Pnb=Pnb[(Pnb.Pnb_buy+Pnb.Pnb_sell)!=0]
