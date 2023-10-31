#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 13:23:30 2023

@author: Denisi H. Hall (halldenisi@gmail.com)
"""
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import streamlit as st
import os
import glob
import datetime
import streamlit as st
from datetime import datetime


root_dir = "METEO_ASC/"
lista = sorted(glob.glob(root_dir + '*.dat'))


array_df=[]
for x in lista:
    temp_df = pd.read_csv(x, 
                  delimiter=',', skiprows=1)
    temp_df = temp_df.drop(index=[0, 1]) #deleta linha com unidades.. 
    
    col=temp_df.columns
    for j in range(1,len(col),1):
        temp_df[col[j]] = temp_df[col[j]].astype(float, errors = 'raise')
        # if j<3:
        #     temp_df[col[j]] = temp_df[col[j]].astype(int, errors = 'raise')
        # else:
        #     temp_df[col[j]] = temp_df[col[j]].astype(float, errors = 'raise')
    
    # temp_df['TIMESTAMP'] = temp_df['SECONDS'].apply(seconds_to_datetime)
    temp_df['TIMESTAMP'] = pd.to_datetime(temp_df['TIMESTAMP'],format="%Y-%m-%d %H:%M:%S")
    temp_df.set_index('TIMESTAMP', inplace=True)

    array_df.append(temp_df)

#%%
biomet=array_df[0]
# biomet.index=biomet["TIMESTAMP"]
# Filtrar as colunas que começam com o prefixo 'TA'

ta = biomet.filter(regex=r'^(TA)') #ta rh
rh=biomet.filter(regex=r'^(RH)')
ws = biomet.filter(regex=r'^(WS)') 
wd= biomet.filter(regex=r'^(WD)')#velocidade e direção do vento
rad_ppfd = biomet.filter(regex=r'^(PPFD)') #radiacao PAR
rad_cnr4 = biomet.filter(regex=r'^(SWIN|SWOUT|LW|RN|T_CRN4)') #saldo radiometro CNR4
rad_spn1 = biomet.filter(regex=r'^(RG|SWDIF)') #radiacao global e difusa
meteo=biomet.filter(regex=r'^(PA_|P_|TC)')


#%%


var=['Air temperature', 
      'Relative humidity', 'Wind speed', 'Wind direction', 
      'PAR radiation', 'Short and long wave radiation (CNR4)', 
      'Global and diffuse radiation', 'Weather',"Profile temperature"]

filtered_dataframes = {
    var[0]: ta,
    var[1]: rh,
    var[2]: ws,
    var[3]: wd,
    var[4]: rad_ppfd,
    var[5]: rad_cnr4,
    var[6]: rad_spn1,
    var[7]: meteo,
    var[8]: ta
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
st.subheader('Check raw data from the K34 micrometeorological tower from LBA program.')
st.caption('Leonardo R. Oliveira, Denisi H. Hall and Carla S. Farias')

# criar um seletor para as variáveis
var_option = st.selectbox('Select variable:', var)

# obter o índice da variável selecionada
var_index = var_option

st.subheader(":blue[{:}]".format(var_index))

df = filtered_dataframes[var_index]


if var_index == "Profile temperature":
    start_time = st.slider(
    "When do you start?",
    min_value=df.index.min().to_pydatetime(),
    max_value=df.index.max().to_pydatetime(),
    # value=(df.index.min(), df.index.max()),
    step=pd.Timedelta(minutes=30)
    )
    st.write("Start time:", start_time)

   # Filtrar o DataFrame para o intervalo de tempo selecionado

    df_filtrado = df[df.index == start_time].reset_index()
    
    df_filtrado = df_filtrado.drop(columns=['TIMESTAMP'])
    df_filtrado=df_filtrado.T
    
    df_filtrado["level"]=[51.1, 42.5, 35.5, 28.0, 15.6, 5.2]
    df_filtrado = df_filtrado.rename(columns={0: 'temperature'})

    # Aplicando os estilos
    styled = df_filtrado.style.apply(highlight_max, axis=0).apply(highlight_min, axis=0)
    # Exibindo o DataFrame estilizado
    st.write(styled)


    plt.figure(figsize=(8, 6))
    plt.plot(df_filtrado["temperature"], df_filtrado["level"])
    plt.xlabel('Temperature (ºC)',size=14)
    plt.ylabel("Level (m)", size=14)
    # plt.title(f'Gráfico de {idx}')
    st.pyplot(plt)

 
else:
        # permitir que o usuário selecione um intervalo de datas
    data_inicio, data_fim = st.date_input('Select date range:', [df.index.min(), df.index.max()])
    
    st.write("Start:", data_inicio , "End:", data_fim)


    df_filtrado = df[(df.index.date >= data_inicio) & (df.index.date <= data_fim)]
    
    #estatistica
    est = df_filtrado.describe()
    
    # Aplicando os estilos
    styled = est.style.apply(highlight_max, axis=1).apply(highlight_min, axis=1)
    
    # Exibindo o DataFrame estilizado
    st.write(styled)
    
    # Crie um gráfico
    col = df_filtrado.columns
    # st.line_chart(df_filtrado)
    for j in range(len(df_filtrado.columns)):
        idx = '%s' % (col[j])
        st.write(f"Variable: {idx}")
        st.line_chart(df_filtrado["{:}".format(idx)])

