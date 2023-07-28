#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:52:51 2023

@author: lmc04
"""
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import streamlit as st

root_dir = "/home/lmc04/Downloads/K34/"

biomet=pd.read_csv(root_dir+'TOA5_47272.Biomet.dat', 
                  delimiter=',', skiprows=1, low_memory=False)

biomet=biomet.drop(0)
biomet=biomet.drop(1)

col = biomet.columns

for j in range(len(col)):
    if j>1: 
        biomet[col[j]] = biomet[col[j]].astype(float, errors = 'raise')
# biomet["TIMESTAMP"]=biomet["TIMESTAMP"].astype(str, errors='raise')

#%%
# substituir 24 por 00
# biomet["TIMESTAMP"] = biomet["TIMESTAMP"].replace('24:00:00', '00:00:00', inplace=True)

biomet['ANO']=biomet["TIMESTAMP"].apply(lambda x: str(x) [0:4]).astype(int)
biomet['MES']=biomet["TIMESTAMP"].apply(lambda x: str(x) [5:7]).astype(int)
biomet['DIA']=biomet["TIMESTAMP"].apply(lambda x: str(x) [8:10]).astype(int)
biomet['HORA']=biomet["TIMESTAMP"].apply(lambda x: str(x) [11:13]).astype(int)
biomet['MIN']=biomet["TIMESTAMP"].apply(lambda x: str(x) [14:16]).astype(int)
biomet['SEG']=biomet["TIMESTAMP"].apply(lambda x: str(x) [17:19]).astype(int)

#CORREÇÃO DO DIA QUANDO A HORA FOR 24:00:00 O DIA TEM QUE SOMAR +1
# if 
# biomet['DIA'] = np.where(biomet['HORA'] == 24, biomet['DIA'] + 1, biomet['DIA'])
# biomet["HORA"] = biomet["HORA"].replace(24, 00)

# biomet['hora']=biomet["TIMESTAMP"].apply(lambda x: str(x) [11:19])

#%%

# biomet["hora"] = biomet["hora"].str.replace('24:00:00', '00:00:00')

biomet['MES'] = biomet['MES'].apply(lambda x: str(x).zfill(2))
biomet['DIA'] = biomet['DIA'].apply(lambda x: str(x).zfill(2))
biomet['HORA'] = biomet['HORA'].apply(lambda x: str(x).zfill(2))
biomet['MIN'] = biomet['MIN'].apply(lambda x: str(x).zfill(2))
biomet['SEG'] = biomet['SEG'].apply(lambda x: str(x).zfill(2))

# biomet['data_hora'] = pd.to_datetime(biomet[['ANO', 'MES', 'DIA', 'HORA', 'MIN']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H-%M')

# df['HORAMIN']=df['date'].apply(lambda x: str(x) [11:16])
# biomet['hora']=

# biomet["TIMESTAMP"] = biomet["TIMESTAMP"].replace('24:00:00', '00:00:00', inplace=True)

# converter para formato datetime
biomet["TIMESTAMP"]=pd.to_datetime(biomet["TIMESTAMP"], format="%Y/%m/%d %H:%M:%S")
# biomet["TIMESTAMP"]=pd.to_datetime(biomet["TIMESTAMP"]).dt.strftime("%Y/%m/%d %H:%M:%S")
# biomet["TIMESTAMP"] = biomet["TIMESTAMP"].strftime(biomet["TIMESTAMP"], "%Y/%m/%d %H:%M:%S")

#%%

biomet.index=biomet["TIMESTAMP"]
# Filtrar as colunas que começam com o prefixo 'TA'
# ta_rh = biomet.filter(regex=r'^(TA|RH)') #ta rh

ta_rh = biomet.filter(regex=r'^(TA)') #ta rh


ws_wd = biomet.filter(regex=r'^(WS|WD)') #velocidade e direção do vento

rad_ppfd = biomet.filter(regex=r'^(PPFD)') #radiacao PAR

rad_cnr4 = biomet.filter(regex=r'^(SWIN|SWOUT|LW|RN|T_CRN4)') #saldo radiometro CNR4

rad_spn1 = biomet.filter(regex=r'^(RG|SWDIF)') #radiacao global e difusa

meteo=biomet.filter(regex=r'^(PA_|P_|TC)') #chuva, pressão e temp superficie

#%%

# fig, ax1 = plt.subplots()

# color = 'tab:blue'
# ax1.set_xlabel('time')
# ax1.set_ylabel('Rain [mm]', color=color)
# ax1.plot(biomet["TIMESTAMP"], meteo['P_RAIN_1_1_1'], color=color)
# ax1.tick_params(axis='y', labelcolor=color)

print('start:', biomet["TIMESTAMP"].iloc[0])
print('end:', biomet["TIMESTAMP"].iloc[-1])

#%%
start=datetime.date(2023, 4, 17)
end=datetime.date(2023, 6, 22)

# data=pd.date_range(start='04/17/2023 17:19:00', 
#                              end='06/22/2023 08:53:00', freq='1T', name='datetime')

# dfs=['rad_cnr4', 'meteo', 'rad_ppfd', "rad_spn1"]
dfs_dataframes = [rad_cnr4, meteo, rad_ppfd, rad_spn1]
for x in range(len(dfs_dataframes)):
    df = dfs_dataframes[x]
    col = df.columns
    for j in range(len(df.columns)): #-1 entra por conta do datetime ser a última coluna
        idx = '%s' %(col[j]) 
        plt.figure(figsize=(12,8))
        plt.plot(df.index, df["{:}".format(idx)])
        plt.title("Período: {:} - {:}".format(start, end))
        plt.ylabel("{:}".format(idx))
#    plt.xlim([start, end])
#    plt.ylim(-50,1200)
    # plt.legend()
        # plt.savefig('{:%Y%m%d}_{:%Y%m%d}_{:}.png'.format(start,end,idx))
        plt.close() #fecha o plot para não sobreescrever 
        plt.show()
    # print(col)
#%% PERFIL 

col=rad_cnr4.columns
df=rad_cnr4
for j in range(len(df.columns)): #-1 entra por conta do datetime ser a última coluna
    idx = '%s' %(col[j]) 
    plt.figure(figsize=(12,8))
    plt.plot(df.index, df["{:}".format(idx)])
    plt.title("Período: {:} - {:}".format(start, end))
    plt.ylabel("{:}".format(idx))
#    plt.xlim([start, end])
#    plt.ylim(-50,1200)
    # plt.legend()
    # plt.savefig('{:%Y%m%d}_{:%Y%m%d}_{:}.png'.format(start,end,idx))
    plt.close() #fecha o plot para não sobreescrever 
plt.show()

#%%
# Escreva o dataframe dashboard
st.write("Dashboard - K34")

st.write("Temperature and relative humidity")

# Escreva algumas estatísticas
st.write(ta_rh.describe())

# Crie um gráfico

# st.line_chart(df.['Valor'])
st.line_chart(ta_rh['TA_1_1_1'])

col=ta_rh.columns
df=ta_rh
for j in range(len(df.columns)): #-1 entra por conta do datetime ser a última coluna
    idx = '%s' %(col[j]) 
    # plt.figure(figsize=(12,8))
    # plt.plot(df.index, df["{:}".format(idx)])
    st.line_chart(df["{:}".format(idx)])





