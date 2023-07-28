#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:52:51 2023

@author: lmc04
"""
import pandas as pd
import numpy as np
import datetime
import streamlit as st

#root_dir = "/home/lmc04/Downloads/K34/"

biomet=pd.read_csv('TOA5_47272.Biomet.dat', 
                  delimiter=',', skiprows=1, low_memory=False)

biomet=biomet.drop(0)
biomet=biomet.drop(1)

col = biomet.columns

for j in range(len(col)):
    if j>1: 
        biomet[col[j]] = biomet[col[j]].astype(float, errors = 'raise')

# converter para formato datetime
#biomet["TIMESTAMP"]=pd.to_datetime(biomet["TIMESTAMP"], format="%Y/%m/%d %H:%M:%S")
biomet["TIMESTAMP"]=pd.to_datetime(biomet["TIMESTAMP"], format="%Y-%m-%d %H:%M:%S")



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





