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
st.set_page_config(page_title='Visão Cidades', page_icon='🌇', layout= 'wide')
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
#1. Chart 
def top_10_restaurant_city(df1):
  restaurant_city = df1.loc[:,['City','Restaurant_ID']].groupby('City').count().sort_values('Restaurant_ID',ascending=False).reset_index()
  top_10_city = restaurant_city.head(10)
  top_10_city.rename(columns={'City':'Cidades','Restaurant_ID':'Quantidade de Restaurantes'}, inplace=True)
  fig = px.bar(top_10_city, x='Cidades', y='Quantidade de Restaurantes', color='Cidades', title='Top 10 cidades com mais restaurantes', text_auto=True)
  fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) # -> Ajustes
  return fig
#2. Chart
def top_7_restaurant(df1):
  top_avg_rate_restaurant = df1.loc[df1['Aggregate_rating']>4,['City','Restaurant_ID']].groupby('City').count().sort_values('Restaurant_ID',ascending=False).reset_index()
  top_7_rate_restaurant = top_avg_rate_restaurant.head(7)
  top_7_rate_restaurant.rename(columns={'City':'Cidades','Restaurant_ID':'Quantidade de Restaurantes'}, inplace=True)
  fig = px.bar(top_7_rate_restaurant, x='Cidades', y='Quantidade de Restaurantes', color='Cidades', title='Top 7 cidades com restaurantes com média acima de 4.0', text_auto=True)
  fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) # -> Ajustes
  return fig

#3. Chart
def bot_7_restaurant(df1):
  bot_avg_rate_restaurant = df1.loc[df1['Aggregate_rating']<2.5,['City','Restaurant_ID']].groupby('City').count().sort_values('Restaurant_ID',ascending=False).reset_index()
  bot_7_rate_restaurant = bot_avg_rate_restaurant.head(7)
  bot_7_rate_restaurant.rename(columns={'City':'Cidades','Restaurant_ID':'Quantidade de Restaurantes'}, inplace=True)
  fig = px.bar(bot_7_rate_restaurant, x='Cidades', y='Quantidade de Restaurantes', color='Cidades', title='Top 7 cidades com restaurantes com média abaixo de 2.5', text_auto=True)
  fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) # -> Ajustes
  return fig

#4. Chart
def f_cuisines_city(df1):       
  cuisines_city = df1.loc[:,['City','Cuisines']].groupby('City').nunique().sort_values('Cuisines',ascending=False).reset_index()
  top_10_cuisines_city = cuisines_city.head(10)
  top_10_cuisines_city.rename(columns={'City':'Cidades','Cuisines':'Culinárias Distintas'}, inplace=True)
  fig = px.bar(top_10_cuisines_city, x='Cidades', y='Culinárias Distintas', color='Cidades', title='Top 10 cidades com mais restaurantes de culinárias distintas', text_auto=True)
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
st.title('Visão Cidades :night_with_stars:')

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
    fig = top_10_restaurant_city(df1)
    st.plotly_chart(fig, use_container_width=True)   
    
with st.container():
    col1, col2 = st.columns(2,gap='small')
    with col1:
        fig = top_7_restaurant(df1)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:   
        fig = bot_7_restaurant(df1)
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    fig = f_cuisines_city(df1)
    st.plotly_chart(fig, use_container_width=True)

    








