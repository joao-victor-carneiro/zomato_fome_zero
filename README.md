# zomato_fome_zero
# 1. Contexto do Problema de Negócio
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

# 2. O Desafio

Para ter o melhor entendimento do negócio para conseguir tomar as melhores decisões
estratégicas e alavancar ainda mais a Fome Zero, e para isso, ele precisa que seja
feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir
dessas análises, para responder às seguintes perguntas:

## Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## País

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

## Cidade

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
Conteúdo licenciado para João Victor Nogueira carneiro -
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
aceitam pedidos online?

## Restaurantes

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os
restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?

## Tipos de Culinária

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

# 3. Premissas assumidas para análise
1. Market place foi o modelo de negócio assumido.
2. Os três principais visões do negócio foram: visão geral, visão país, visão cidades, visão restaurantes e visão culinária.

O CEO também pediu que fosse gerado um dashboard que permitisse que ele
visualizasse as principais informações das perguntas que ele fez. O CEO precisa
dessas informações o mais rápido possível, uma vez que ele também é novo na
empresa e irá utilizá-las para entender melhor a empresa Fome Zero para conseguir
tomar decisões mais assertivas.
O trabalho é utilizar os dados que a empresa Fome Zero possui e responder as
perguntas feitas do CEO e criar o dashboard solicitado.

# Estratégia de solução

Em Visão Geral podemos verificar alguns quantitativos, como:

1. Restaurantes Cadastrados;
2. Países Cadastrados;
3. Cidades Cadastradas;
4. Avaliações Feitas na Plataforma;
5. Tipos de Culinárias Oferecidas;
6. Localizações.

Em Visão Países, podemos verificar algumas métricas, como:

1. Quantidade de Restaurantes Registrados por País;
2. Quantidade de Cidades Registradas por País;
3. Quantidade Média de Avaliações por País;
4. Preço Médio de um Prato para Duas Pessoas por País.

Em Visão Cidades:

1. Top 10 Cidades com Mais Restaurantes Registrados na Base de Dados;
2. Top 7 Cidades com Restaurantes com Média de Avaliação acima de 4.0;
3. Top 7 Cidades com Restaurantes com Média de Avaliação abaixo de 2.5;
4. Top 10 Cidades com Mais Restaurantes com Culinária Distinta.

Em Visão Culinárias:

1. Os Melhores Restaurantes com os 5 Tipos Culinários Mais Populares;
2. Um Dataframe que Mostra até os 20 Melhores Restaurantes Registrados;
3. Top 10 Melhores Tipos Culinários;
4. Top 10 Piores Tipos Culinários.
   
# Conclusão
Você recebeu um desafio de Ciência de Dados próximo dos desafios reais das
empresas e você irá utilizar todo o conhecimento adquirido no curso FTC -
Analisando Dados com Python para resolvê-lo.
Os problemas nas empresas chegam em forma de perguntas abertas,
desestruturadas e sem nenhuma dica sobre como resolver, então, utilizar os
conhecimentos adquiridos no curso serão fundamentais para o seu sucesso na sua
jornada como um profissional de Ciência de Dados.
É papel do Cientista de Dados entender a causa raiz, planejar o desenvolvimento e
criar a melhor solução para o problema de negócio.
Aproveite esse desafio para colocar em prática tudo que você aprendeu ao longo do
curso! E caso tenha alguma dificuldade, utilize o poder da Comunidade DS:
Publique ela dentro do canal do curso no Discord para discutir com a galera as suas
dúvidas
