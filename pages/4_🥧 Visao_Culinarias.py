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
st.set_page_config(page_title='Visão Culinárias',page_icon='🥧', layout='wide')
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
#1. dataframe
def f_top_restaurant(df1):
  df1 = (df1.loc[:,['Restaurant_ID','Restaurant_Name','Country_Name','City','Cuisines','Average_Cost_for_two','Aggregate_rating','Votes']]
                          .groupby('Restaurant_ID')
                          .max()
                          .sort_values(['Aggregate_rating','Restaurant_ID'],ascending=[False,True])
                          .reset_index())
  df1 = df1.head(top_restaurant_silder)
  return df1

#2. Chart
def f_top_10_restaurant (df1):
  top_restaurant = df2.loc[:,['Cuisines','Aggregate_rating']].groupby('Cuisines').mean().sort_values('Aggregate_rating',ascending=False).reset_index()
  top_10_restaurant = top_restaurant.head(top_restaurant_silder)
  top_10_restaurant.rename(columns={'Cuisines':'Culinárias','Aggregate_rating':'Média de Avaliações'},inplace=True)
  fig = px.bar(top_10_restaurant, x='Culinárias', y='Média de Avaliações', color='Culinárias', title=f'Top {top_restaurant_silder} melhores tipos de culinárias', text_auto='.2s')
  fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) # -> Ajustes
  return fig

#3. Chart
def f_bot_10_restaurant(df1):
  bot_restaurant = df2.loc[:,['Cuisines','Aggregate_rating']].groupby('Cuisines').mean().sort_values('Aggregate_rating',ascending=False).reset_index()
  bot_10_restaurant = bot_restaurant.tail(top_restaurant_silder)
  bot_10_restaurant.rename(columns={'Cuisines':'Culinárias','Aggregate_rating':'Média de Avaliações'},inplace=True)
  fig = px.bar(bot_10_restaurant, x='Culinárias', y='Média de Avaliações', color='Culinárias', title=f'Top {top_restaurant_silder} piores tipos de culinárias', text_auto='.2s')
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

#4. Criando um df reserva
df2 = df1.copy()
#-------------------------------------------------Códigos---------------------------------------------#
st.title('Visão Tipo de Culinárias :night_with_stars:')

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
top_restaurant_silder = st.sidebar.slider(
  'Até qual valor?',
  value=10,
  min_value=1,
  max_value=20)

st.sidebar.markdown("""---""")

cuisines_options = st.sidebar.multiselect(
    'Seleciones as culinárias desejadas para verificação',
    ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
       'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
       'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
       'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
       'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç'],
    default = ['Home-made','Japanese','BBQ','Brazilian','Arabian','American','Italian','Chinese'])

st.sidebar.markdown('## Powered by Carneiro :sunglasses:')

#------Filtro de Países----#
linhas_selecionadas = df1['Country_Name'].isin(countries_options)
df1 = df1.loc[linhas_selecionadas, :]

linhas_selecionadas = df2['Country_Name'].isin(countries_options)
df2 = df2.loc[linhas_selecionadas, :]

#---Filtro de Culinárias---#
linhas_selecionadas = df1['Cuisines'].isin(cuisines_options)
df1 = df1.loc[linhas_selecionadas, :]

#=======================================#
#Layout
#=======================================#
with st.container():
  st.markdown('## Melhores Restaurantes dos Principais tipos Culinários :100:')
  col1,col2,col3,col4,col5 = st.columns(5,gap='small')
  with col1:
    st.metric(label='Central Grocery', value='Italia', delta='4,9/5,0')

  with col2:
    st.metric(label='Fat Cat', value='EUA', delta='4,9/5,0')

  with col3:
    st.metric(label='Mandi@36', value='Arabia', delta='4,7/5,0')

  with col4:
    st.metric(label='Samurai', value='Japão', delta='4,9/5,0')

  with col5:
    st.metric(label='Kanaat Lokantası', value='Caseira', delta='4,0/5,0')

with st.container():
  st.markdown(f'## Top {top_restaurant_silder} Restaurantes')
  df1 = f_top_restaurant(df1)
  st.dataframe(df1)
  
with st.container():
  col1,col2 = st.columns(2,gap='small')

  with col1:
    fig = f_top_10_restaurant (df1)
    st.plotly_chart(fig, use_container_width=True)
    
  with col2:
    fig = f_bot_10_restaurant(df1)
    st.plotly_chart(fig, use_container_width=True)
    









































