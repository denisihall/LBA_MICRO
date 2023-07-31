#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:52:51 2023

@author: lmc04
"""
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import streamlit as st
import os
import glob
import datetime

def seconds_to_datetime(seconds):
    datetime_output_utc = datetime.datetime.utcfromtimestamp(seconds)
    gmt_minus_4 = datetime.timezone(datetime.timedelta(hours=-4))
    datetime_output_gmt_minus_4 = datetime_output_utc.replace(tzinfo=gmt_minus_4)
    datetime_output_gmt_minus_4 = datetime_output_gmt_minus_4.replace(year=2023)
    return datetime_output_gmt_minus_4.strftime('%Y-%m-%d %H:%M:%S')

root_dir = "METEO_ASC/"
lista = sorted(glob.glob(root_dir + '*'))

array_df=[]
for x in lista:
    temp_df = pd.read_csv(x, 
                  delimiter=',', skiprows=1)
    temp_df = temp_df.drop(index=[0, 1]) #deleta linha com unidades.. 
    
    col=temp_df.columns
    for j in range(len(col)):
        temp_df[col[j]] = temp_df[col[j]].astype(float, errors = 'raise')
        # if j<3:
        #     temp_df[col[j]] = temp_df[col[j]].astype(int, errors = 'raise')
        # else:
        #     temp_df[col[j]] = temp_df[col[j]].astype(float, errors = 'raise')
    
    temp_df['TIMESTAMP'] = temp_df['SECONDS'].apply(seconds_to_datetime)
    temp_df['TIMESTAMP'] = pd.to_datetime(temp_df['TIMESTAMP'])
    array_df.append(temp_df)

   

#%%
biomet=array_df[0]
biomet.index=biomet["TIMESTAMP"]
# Filtrar as colunas que começam com o prefixo 'TA'

ta = biomet.filter(regex=r'^(TA)') #ta rh
rh=biomet.filter(regex=r'^(RH)')
ws_wd = biomet.filter(regex=r'^(WS|WD)') #velocidade e direção do vento
rad_ppfd = biomet.filter(regex=r'^(PPFD)') #radiacao PAR
rad_cnr4 = biomet.filter(regex=r'^(SWIN|SWOUT|LW|RN|T_CRN4)') #saldo radiometro CNR4
rad_spn1 = biomet.filter(regex=r'^(RG|SWDIF)') #radiacao global e difusa
meteo=biomet.filter(regex=r'^(PA_|P_|TC)')

filtered_dataframes = {
    'ta': ta,
    'rh': rh,
    'ws_wd': ws_wd,
    'rad_ppfd': rad_ppfd,
    'rad_cnr4': rad_cnr4,
    'rad_spn1': rad_spn1,
    'meteo': meteo
}


#%%
# Definindo as funções de estilo
def highlight_max(data, color='yellow'):
    attr = f'background-color: {color}'
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        is_max = data == data.max()
        return [attr if v else '' for v in is_max]
    else:  # DataFrame from .apply(axis=None)
        is_max = data == data.max().max()
        return pd.DataFrame(np.where(is_max, attr, ''),
                            index=data.index, columns=data.columns)
                            
def highlight_min(data, color='lightblue'):
    attr = f'background-color: {color}'
    if data.ndim == 1:
        is_min = data == data.min()
        return [attr if v else '' for v in is_min]
    else:
        is_min = data == data.min().min()
        return pd.DataFrame(np.where(is_min, attr, ''),
                            index=data.index, columns=data.columns)
#%%
# Escreva o dataframe dashboard

from PIL import Image

image = Image.open('LOGOS/lbalogo.png')
st.image(image)

# image2 = Image.open('LOGOS/micro_logo.png')
# st.image(image2)


#%%
st.title("Dashboard - K34")
st.caption('Check raw data from the K34 micrometeorological tower from LBA program.')


var=['Air temperature', 
     'Relative humidity', 'Wind speed and direction', 
     'PAR radiation', 'Short and long wave radiation (CNR4)', 
     'Global and diffuse radiation', 'Weather']
# st.write("Temperature ºC")
for i, ta in enumerate(filtered_dataframes):
    st.subheader(":red[{:}]".format(var[i]))
    
    df=filtered_dataframes[ta]
    est=df.describe()

# Aplicando os estilos
    styled = est.style.apply(highlight_max, axis=1).apply(highlight_min, axis=0)

# Exibindo o DataFrame estilizado
    st.write(styled)

# Crie um gráfico
    col=df.columns
    st.line_chart(df)
    for j in range(len(df.columns)): #-1 entra por conta do datetime ser a última coluna
        idx = '%s' %(col[j]) 
    # plt.figure(figsize=(12,8))
    # plt.plot(df.index, df["{:}".format(idx)])
        st.line_chart(df["{:}".format(idx)]) 

   






