#================================#
#Libraries
#================================#
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#================================#
#Bibliotecas necessárias
#================================#
import folium
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import re
import inflection
import pandas as pd
st.set_page_config(page_title='Visão Geral',page_icon='🌌',layout='wide')
#================================#
#Importação de dados
#================================#

df = pd.read_csv('dataset/zomato.csv')
df1 = df.copy() #Criando uma cópia do dataframe

#--------------------------------------Funções-----------------------------------#

#============Operações iniciais=================#
#Categorizando a culinária
df1['Cuisines'] = df1['Cuisines'].astype( str )
df1["Cuisines"] = df1.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])

#===================Funções======================#
#1. Limpeza dos dados
def clean_code(df1):
  """ Esta função tem por responsabilidade limpar o dataframe
      Tipos de limpeza:
      1. Substituir os espaços dos títulos por underline
      2. Remoção dos dados nan
      3. Remoção dos valores Others
      4. Remoção da coluna 'Switch_to_order_menu'
      5. Remoção de linhas duplicadas

      Imput: Dataframe
      Output: Dataframe 
  """
  #Removendo espaços do título por "_"
  df1.columns = df1.columns.str.replace(' ', '_')

  #Apagar as linhas com vazios e com o valor "Others"
  linhas_vazias = df1['Cuisines'] != 'nan'
  df1 = df1.loc[linhas_vazias, :].copy()

  linhas_Others = df1['Cuisines'] != 'Others'
  df1 = df1.loc[linhas_Others, :].copy()

  #Removendo a coluna 'Switch to order menu', pois todos os valores eram iguais.
  df1 = df1.drop(columns = ['Switch_to_order_menu'], axis = 1)

  #Removendo linhas duplicadas
  df1 = df1.drop_duplicates().reset_index()

  return df1

#2. Preenchimento do nome dos países
COUNTRIES = {
  1: "India",
  14: "Australia",
  30: "Brazil",
  37: "Canada",
  94: "Indonesia",
  148: "New Zeland",
  162: "Philippines",
  166: "Qatar",
  184: "Singapure",
  189: "South Africa",
  191: "Sri Lanka",
  208: "Turkey",
  214: "United Arab Emirates",
  215: "England",
  216: "United States of America",
}
def country_name(Country_Code):
  return COUNTRIES[Country_Code]

#3. Criação do tipo de categoria de comida
def create_price_type(Price_range):
  if Price_range == 1:
    return "cheap"
  elif Price_range == 2:
    return "normal"
  elif Price_range == 3:
    return "expensive"
  else:
    return "gourmet"

#4. Criação do nome das cores
COLORS = {
  "3F7E00": "darkgreen",
  "5BA829": "green",
  "9ACD32": "lightgreen",
  "CDD614": "orange",
  "FFBA00": "red",
  "CBCBC8": "darkred",
  "FF7800": "darkred",
}
def color_name(Rating_color):
  return COLORS[Rating_color]

#=========Funções dos Códigos===========#
#1. Big Numbers
def calculate_big_number(col , operation):
  if operation == 'nunique':
    results = df2.loc[:, col].nunique()
  elif operation == 'sum':
    results = df2.loc[:, col].sum()
  return results 

#2. Map
def city_map(df1):
  df_aux = df1.loc[:,['Latitude','Longitude','Restaurant_Name','City','Aggregate_rating','Price_range']].groupby(['City','Restaurant_Name','Price_range','Aggregate_rating']).max().reset_index()
  map = folium.Map(tiles='Cartodb dark_matter',zoom_start=8)
  mCluster = MarkerCluster(name='Restaurantes').add_to(map)

  for index, location_info in df_aux.iterrows():

    folium.Marker([location_info['Latitude'],
                  location_info['Longitude']],
                  popup=location_info[['City','Restaurant_Name','Price_range','Aggregate_rating']],
                  icon = folium.Icon(color = 'red', icon='home')).add_to(mCluster)
  folium_static(map, width=800, height = 480)

#-----------------------------------------Aplicação das funções --------------------------------------#
#1. Limpeza dos dados
df1 = clean_code(df1)

#1. Criação da coluna "Country_Name"
df1['Country_Name'] = df1.loc[:,'Country_Code'].apply(lambda x: country_name(x))

#2. Preenchimento do Price_range
df1['Price_range'] = df1['Price_range'].apply(create_price_type)

#3. Criação no nome das cores
df1['Rating_color'] = df1['Rating_color'].apply(color_name)

#4. Criando um df reserva
df2 = df1.copy()

#-------------------------------------------------Códigos---------------------------------------------#
st.title('Fome Zero!')
st.markdown('## O melhor lugar para encontrar seu mais novo restaurante favorito! :shallow_pan_of_food:')
#st.dataframe(df1)

#=======================================#
#Sidebar
#=======================================#
image = Image.open('zomato_logo1.png')
st.sidebar.image(image, width=270)
st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown("""---""")

#-------Filtro Sidebar-------#
st.sidebar.markdown('## Filtros')
countries_options = st.sidebar.multiselect(
    'Seleciones os países desejados para verificação',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default = ['Brazil','India','England','South Africa','United States of America'])
st.sidebar.markdown("""---""")
st.sidebar.markdown('## :gray[Powered by Carneiro]:sunglasses:')

#------Filtro de culinária----#
linhas_selecionadas = df1['Country_Name'].isin(countries_options)
df1 = df1.loc[linhas_selecionadas, :]

#=======================================#
#Layout
#=======================================#
#---------------Containers e colunas---------------------#
with st.container():#Container 1 -> Columns
  st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')

  col1,col2,col3,col4,col5= st.columns(5, gap='medium')
  with col1:
    results = calculate_big_number('Restaurant_ID' , operation='nunique')
    col1.metric('Restaurantes Cadastrados',results)
      
    
  with col2:
    results = calculate_big_number('Country_Name' , operation='nunique')
    col2.metric('Países Cadastrados',results)

  with col3:
    results = calculate_big_number('City' , operation='nunique')
    col3.metric('Cidades Cadastradas',results)

  with col4:
    results = calculate_big_number('Votes' , operation='sum')
    col4.metric('Total de Avaliações',results)

  with col5:
    results = calculate_big_number('Cuisines' , operation='nunique')
    col5.metric('Culinárias', results)

#=======================================#
#Inserindo Mapa
#=======================================#
city_map(df1)









