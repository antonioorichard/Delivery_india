# Librarys*************************
    ## Importar map
import folium
from streamlit_folium import folium_static
    ## Importar imagens
from PIL import Image
    ## Streamlit - Dashbord interativo online
import streamlit as st
    ## Númerico
import numpy as np
    ##Dataframe
import pandas as pd
    ## Gráficos
import plotly.express as px
import plotly.graph_objects as go 
    ## Calcula a distância de pontos latitude e longetude
#!pip install haversine
#import haversine
#from haversine import haversine

# \Librarys-----------------------
st.set_page_config( page_title = 'Visão da Empresa', page_icon = '📈', layout = 'wide' )

#Importar Dataframe*********************************
df = pd.read_csv('Dataset/train.csv')
#df = pd.read_csv('../Dataset/train.csv')

#\Importar Dataframe--------------------------------



#---------------------------------------------------
# Funções 
#--------------------------------------------------



#Limpeza ******************************************
def clean_date(df1):

    """ Está função tem a rsponsabilidade de limpar o dattaframe
        1. Removação dos dados NaN
        2. Mudança do tipo da coluna de dados 
        3. Remomvação dos espaços das variáveis de texto
        4. Formatação da colun de datas 
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
        
        Input: Dataframe
        Output: Dataframe
    
    
    """
    # 1.
    linhas_selecionadas = (df1['Delivery_person_Age']!= 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1 = df1.loc[df1['City'] != 'NaN', :]
    df1 = df1.loc[df1['City'] != 'NaN ', :]

    df1 = df1.loc[df1['Festival'] != 'NaN', :]
    df1 = df1.loc[df1['Festival'] != 'NaN ', :]

    df1 = df1.loc[df1['Road_traffic_density'] != 'NaN', :]
    df1 = df1.loc[df1['Road_traffic_density'] != 'NaN ', :]
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)


    #2.
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    #3

    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format ='%d-%m-%Y')

    #4

    linhas_selecionadas = (df1['multiple_deliveries']!= 'NaN ')
    df1.drop(7754, inplace=True)
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries']= df1['multiple_deliveries'].astype(int)

    #5. Remove o espaço por exemplo 'NaN ', fica 'NaN'

    df1 = df1.reset_index(drop = True)
    for i in range(len(df1)):
      df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()
    # removendo de oufra forma
    df1.loc[:,'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:,'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:,'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:,'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:,'City'] = df1.loc[:, 'City'].str.strip()

    contador = 0
    while   contador != df1.shape[0]:
      df1.loc[contador,'Time_taken(min)'] = int(df.loc[contador, 'Time_taken(min)'].replace('(min) ', ''))
      contador = contador +1

    # Acresentando semana

    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )

    cols = ['Restaurant_latitude','Restaurant_longitude', 'Delivery_location_latitude','Delivery_location_longitude']
    
    return(df1)
#--------------------------------
#\Funções 
#--------------------------------



#-------------------------Inicio da Estrutura lógica do código ------------------------------ 
df1 = df.copy()
# Limpeza de dados
df1 = clean_date(df1)


# STREAMLIT
                        #*********VISÃO EMPRESA**********
                    #Gráfico 📊 Quantidade de entrega por dia 


#========================================
#Barra Lateral
#========================================

st.header('Marketplace - Visão do Cliente')

#image = Image.open( 'Dashboards/Delivery_india/Delivery.jpg')
st.sidebar.image('Logo_scooter_delivery.png', width = 220)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Faster Delivery in Town')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Select a due date (Selecione uma data limite)')
date_slider = st.sidebar.slider( 
    'Até qual o valor ?', 
                  value= pd.datetime(2022,4,13),
                  min_value = pd.datetime(2022, 2, 11),
                  max_value = pd.datetime(2022,4, 6), 
                  format = 'DD-MM-YYYY'              
                 )
#st.header(date_slider)
st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect( 
                     'Quais as condições do trânsito', 
                    ['Low', 'Medium', 'High', 'Jam'], 
                    default = ['Low', 'Medium', 'High', 'Jam'])
st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')
# FILTRO DE DATA


# FILTRO SLIDER
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas,:]

# FILTRO DE TRANSITO
linhas_selecionadas1 =  df1['Road_traffic_density'].isin( traffic_options)
df1 = df1.loc[linhas_selecionadas1,:]
st.dataframe(df1)

# FILTRO SLIDER
#========================================
#             \Barra Lateral
#========================================


#========================================
#           **** Layout Streamlit ****
#========================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial','Visão Tática' , 'Visão Geográfica'])
with tab1:
    with st.container(): 
        #Order Metric
        st.markdown('# Amo meu criador')
        cols = ['ID', 'Order_Date']
        # Selecao de linhas
        df_aux = df1.loc[:,cols].groupby('Order_Date').count().reset_index()
        # desenhar o gráfio de linhas
        fig = px.bar(df_aux, x = 'Order_Date', y = 'ID')
        st.plotly_chart(fig, use_container_width = True)
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(' #  Traffic Order Share')
            df_aux=df1.loc[:,['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
            df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
            df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
            df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
            figu = px.pie(df_aux, values = 'entregas_perc', names = 'Road_traffic_density') 
            st.plotly_chart(figu, use_container_width =  True)

        with col2:
            st.markdown(' #  Traffic Order City')
            df_aux = df1.loc[:, ['ID',  'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
            df_aux = df_aux.loc[df_aux['City']!= 'NaN', :]
            df_aux = df_aux.loc[df_aux['Road_traffic_density']!= 'NaN', :]
            figur = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
            st.plotly_chart(figur, use_container_width = True)
with tab2:  
    with st.container():
        st.markdown('# Order by Week')
        # Quantidade de pedidos por Semana
        df2 = df1.copy()
        df2['week_of_year'] = df2['Order_Date'].dt.strftime( "%U" )
        # dt é necessário pois o comando strftime não é atribuído em objetos Series, dt transforma em strings
        df_aux = df2.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
        # gráfico
        fig = px.line( df_aux, x='week_of_year', y='ID' )
        st.plotly_chart(fig, use_container_width = True)
    with st.container():
        st.markdown('# Order Share by Week')
        df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
        df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
        df_aux = pd.merge(df_aux01, df_aux02, how = 'inner')
        df_aux['order_by_deliver'] = df_aux01['ID'] / df_aux02['Delivery_person_ID']
        fig = px.line(df_aux, x = 'week_of_year', y = 'order_by_deliver')
        st.plotly_chart(fig, use_container_width = True)
with tab3:    
    st.markdown('# Country Maps')
    #\ Layout -----------------
    df_aux= df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    df1 = df1.loc[df1['City'] != 'NaN', :]
    df1 = df1.loc[df1['Road_traffic_density'] != 'NaN', :]

    map = folium.Map()
    for index, location_info in df_aux.iterrows():
      folium.Marker([location_info['Delivery_location_latitude'],
                    location_info['Delivery_location_longitude']], popup = location_info [['City', 'Road_traffic_density']]).add_to(map)
    folium_static(map, width = 1024, height = 600)
# ============================================
              #\***STREAMLIT***
# ============================================
