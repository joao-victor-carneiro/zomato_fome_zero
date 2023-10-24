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
from numpy import unique
st.set_page_config(page_title='Visão Países',page_icon='🌎',layout='wide')
#================================#
#Importação de dados
#================================#
import pandas as pd
import re
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

#==========Funções dos Códigos==========#
#Gráfics 1.0
def graphic_country_01(df1,col1,name1,operation,title):
  if operation == 'count':
    restaurant_country =( df1.loc[:,['Country_Name',col1]].groupby('Country_Name')
                                                                    .count()
                                                                    .sort_values(col1,ascending=False)
                                                                    .reset_index())
    restaurant_country.rename(columns={'Country_Name':'Países',col1:name1}, inplace=True)
    fig = px.bar(restaurant_country,x='Países',
                                    y=name1, 
                                    color='Países', 
                                    title=title,
                                    text_auto=True)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) # -> Ajustes
    return fig
  else:
    restaurant_country =( df1.loc[:,['Country_Name',col1]].groupby('Country_Name')
                                                                    .nunique()
                                                                    .sort_values(col1,ascending=False)
                                                                    .reset_index())
    restaurant_country.rename(columns={'Country_Name':'Países',col1:name1}, inplace=True)
    fig = px.bar(restaurant_country,x='Países',
                                    y=name1, 
                                    color='Países', 
                                    title=title,
                                    text_auto=True)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) # -> Ajustes
    return fig

#Gráfics 2.0
def graphic_country_02(df1,col1,name1,operation,title):
  if operation == 'mean':
    restaurant_country =( df1.loc[:,['Country_Name',col1]].groupby('Country_Name')
                                                                    .mean()
                                                                    .sort_values(col1,ascending=False)
                                                                    .reset_index())
    restaurant_country.rename(columns={'Country_Name':'Países',col1:name1}, inplace=True)
    fig = px.bar(restaurant_country,x='Países',
                                    y=name1, 
                                    title=title,
                                    text_auto='.5s')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) # -> Ajustes
    return fig
  else:
    restaurant_country =( df1.loc[:,['Country_Name',col1]].groupby('Country_Name')
                                                                    .mean()
                                                                    .sort_values(col1,ascending=False)
                                                                    .reset_index())
    restaurant_country.rename(columns={'Country_Name':'Países',col1:name1}, inplace=True)
    fig = px.bar(restaurant_country,x='Países',
                                    y=name1, 
                                    title=title,
                                    text_auto='.5s')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) # -> Ajustes
    return fig
#-----------------------------------------Aplicação das funções --------------------------------------#
#1. Limpeza dos dados
df1 = clean_code(df1)

#1. Criação da coluna "Country_Name"
df1['Country_Name'] = df1.loc[:,'Country_Code'].apply(lambda x: country_name(x))

#2. Preenchimento do Price_range
df1['Price_range'] = df1['Price_range'].apply(create_price_type)

#3. Criação no nome das cores
df1['Rating_color'] = df1['Rating_color'].apply(color_name)

#-------------------------------------------------Códigos---------------------------------------------#
st.title('Visão Países :earth_americas:')

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
with st.container():
  fig = graphic_country_01(df1,
                           col1 = 'Restaurant_ID',
                           name1 = 'Restaurantes por País',
                           operation = 'count',
                           title = 'Quantidade de Restaurantes por País')
  st.plotly_chart(fig, use_container_width=True)

with st.container():
  fig = graphic_country_01(df1,
                           col1 = 'City',
                           name1 = 'Quantidade de Cidades',
                           operation = 'nunique',
                           title = 'Quantidade de Cidades por País')
  st.plotly_chart(fig, use_container_width=True)

with st.container():
  col1,col2 = st.columns(2,gap='small')

  with col1:
    fig = graphic_country_02(df1, 
                             col1='Votes',
                             name1='Votos por País',
                             operation='mean',
                             title='Quantidade de Votos por País')
    st.plotly_chart(fig, use_container_width=True)

  with col2:
    fig = graphic_country_02(df1, 
                             col1='Average_Cost_for_two',
                             name1='Média de preço de prato para dois',
                             operation='mean',
                             title='Custo Médio do Prato para Dois por País')
    st.plotly_chart(fig, use_container_width=True)
    