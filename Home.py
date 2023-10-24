import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='🏠 Home',
    )


#image_path = 'C:/Users/João Vitor/Documents/repos/zomato/'
image = Image.open('zomato_logo1.png')
st.sidebar.image(image, width=270)

st.sidebar.header('FOME ZERO')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Powered by Carneiro :sunglasses:')

st.write('# FOME ZERO ZOMATO DASHBOARD')

st.markdown(
    """
    O Zomato Dashboard foi construído para verificar a qualidade dos diferente tipo de culinárias
    existentes no 15 países em que a Zomato atua.
    ### Como usar o Zomato Dashboard?
    1. Em Visão Geral podemos verificar alguns quantitativos, como:
        - Restaurantes Cadastrados;
        - Países Cadastrados;
        - Cidades Cadastradas;
        - Avaliações Feitas na Plataforma;
        - Tipos de Culinárias Oferecidas;
        - Localizações.

    2. Em Visão Países, podemos verificar algumas métricas, como:
        - Quantidade de Restaurantes Registrados por País;
        - Quantidade de Cidades Registradas por País;
        - Quantidade Média de Avaliações por País;
        - Preço Médio de um Prato para Duas Pessoas por País.

    3. Em Visão Cidades:
        - Top 10 Cidades com Mais Restaurantes Registrados na Base de Dados;
        - Top 7 Cidades com Restaurantes com Média de Avaliação acima de 4.0;
        - Top 7 Cidades com Restaurantes com Média de Avaliação abaixo de 2.5;
        - Top 10 Cidades com Mais Restaurantes com Culinária Distinta.

    4. Em Visão Culinárias:
        - Os Melhores Restaurantes com os 5 Tipos Culinários Mais Populares;
        - Um Dataframe que Mostra até os 20 Melhores Restaurantes Registrados;
        - Top 10 Melhores Tipos Culinários;
        - Top 10 Piores Tipos Culinários.

    ### Ask for help
    - @joaovictorcarneiro_

    """
)

