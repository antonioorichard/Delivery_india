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
#from streamlit import set_page_config
st.set_page_config(page_title = 'Visão Entregador', page_icon = '🛵', layout = 'wide' )
#Importar Dataframe*********************************
df = pd.read_csv('Dashboards/Delivery_india/train.csv')
#\Importar Dataframe--------------------------------


#Limpeza ******************************************
#df = pd.read_csv('train.csv')
df1 = df.copy()


#========================================
            # Funções
#=========================
    

# Clean completo
def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o dataframe
        
        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tiipo da coluna de dados
        3. Removação dos esplos das variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna e tempo ( remoção do texto da varável numérica )
       
       Input: Datafrarme
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

    df1 = df1.loc[df1['Weatherconditions'] != 'conditions NaN', :]
    df1 = df1.loc[df1['Weatherconditions'] != 'nan ', :]
    df1 = df1.loc[df1['Weatherconditions'] != 'nan', :]
    df1 = df1.loc[df1['Weatherconditions'] != 'conditions NaN ', :]
    df1 = df1.loc[df1['Weatherconditions'] != ' conditions NaN', :]
    df1 = df1.loc[df1['Weatherconditions'] != ' conditions NaN ', :]
    


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
    # Tirando condition do clima
    contador = 0
    while   contador != df1.shape[0]:
      df1.loc[contador,'Weatherconditions'] = df.loc[contador, 'Weatherconditions'].replace('conditions', '')
      contador = contador +1
    df1.loc[:,'Weatherconditions'] = df1.loc[:, 'Weatherconditions'].str.strip()
    df1 = df1.loc[df1['Weatherconditions'] != 'NaN', :]
        
        # Acresentando semana

    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )

    return(df1)




df1 = clean_code(df1)
#_________________________________________________________________
#                           função lista de entrega

def lista_de_entrega(df1 ,  ascend):
    """
    Esta função informa uma datafrarme em ordem de menor te de entrega ou maior tempo de entrega.
   
       Input: 
            Parameters:
                df1: Datafarme
                ascending: 'True' or 'False'
                        True: For more speed
                        False: for low speed or slow
        Output:
    """
    
    if ascend == True:
        df2 = df1.loc[:, ['Delivery_person_ID','City', 'Time_taken(min)']].groupby(['City','Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)'], ascending= ascend).reset_index()
        df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
        df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
        df_aux03 = df2.loc[df2['City'] == 'Semi_Urban', :].head(10)
        df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop =True)

        return(df3)
    else:
        df2 = df1.loc[:, ['Delivery_person_ID','City', 'Time_taken(min)']].groupby(['City','Delivery_person_ID']).max().sort_values(['City', 'Time_taken(min)'], ascending= ascend).reset_index()
        df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
        df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
        df_aux03 = df2.loc[df2['City'] == 'Semi_Urban', :].head(10)
        df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop =True)

        return(df3)

# ___________________________________
#                   Avaliações médias por entregador
def avaliacoes_mid_por_entregador(df1):
    """
    Função que apresenta um dataframe com as avalições 
    médias por entregador
    ___________________________________________________
    input:
        parameters:
            df1: dataframe
            
    output:
        parameters: 
            df1: dataframe com avaliaçõese médias por entregador
    
    """
    df_aux=df1.iloc[:, [3,12]].groupby(df1.iloc[:,12]).agg({'Delivery_person_Ratings':['mean', 'std']})
    df_aux.columns = ['Delivery_mean', 'Delivery_std']
    df_aux = df_aux.reset_index()
    return (df_aux)

#______________________________________
#               avaliação média por clima
def avaliacao_mid_por_clima(df1):
    """
    Função que apresenta um dataframe com as avalições 
    médias por entregador
    ___________________________________________________
    input:
        parameters:
            df1: dataframe
            
    output:
        parameters: 
            df1: dataframe com avaliaçõese médias por entregador
    """
    df_aux=df1.iloc[:, [3,11]].groupby(df1.iloc[:,11]).agg({'Delivery_person_Ratings':['mean', 'std']})
    df_aux.columns = ['Delivery_mean', 'Delivery_std']
    df_aux.reset_index()
    return(df_aux)
    
#======================
#          \Funções
#======================




#\VISÃO EMPRESA---------------------------------------
    #========================================
    #Barra Laterals
    #========================================

st.header('Marketplace - Visão do Entregadores')

#image = Image.open( 'Dashboards/Delivery_india/Delivery.jpg')
#st.sidebar.image(image, width = 120)
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

# FILTRO DE DATA


# FILTRO SLIDER
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas,:]

# FILTRO DE TRANSITO
linhas_selecionadas1 =  df1['Road_traffic_density'].isin( traffic_options)
df1 = df1.loc[linhas_selecionadas1,:]

# FILTRO DE CLIMA
# Options
#interessante tirar conditions dos nomes 
traffic_options1 = st.sidebar.multiselect( 
                     'Quais as condições do clima', 
                    df1['Weatherconditions'].unique(), 
                    default = df1['Weatherconditions'].unique(), 
)
#Options


linhas_selecionadas2 =  df1['Weatherconditions'].isin( traffic_options1)
df1 = df1.loc[linhas_selecionadas2,:]
#st.dataframe(df1)
# FILTRO SLIDER
st.sidebar.markdown('### Powered by Antonio Richard')
#========================================
#\Barra Lateral
#========================================

#========================================
#\Layout
#========================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial','Visão ' , 'Visão '])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1,  col2,  col3,  col4  = st.columns(4, gap = 'large')
        with col1:
            #'O entregador mais velho é
            #st.title('Maior de idade')
            maior_idade = df1.loc[:,'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)
        
        with col2:
            #O entregador mais novo é
            #st.title('Menor de idade')
            Menor_idade=df1.loc[:,'Delivery_person_Age'].min()
            col2.metric('Menor idade', Menor_idade)
        
        with col3:
            # Melhor condição de veículos
            #st.title('Melhor condição de veículos')
            condicao_veiculo = df1.loc[:,'Vehicle_condition'].max()
            col3.metric('Melhor condição veículo', condicao_veiculo)
            
        with col4:
            #'A melhor condição de veículo é
            #st.title('Pior condição de veículos')
            condicao_veiculo = df1.loc[:,'Vehicle_condition'].min()
            col4.metric('Pior condição', condicao_veiculo)

    with st.container():
        st.markdown("""---""")
        st.markdown('# Avaliações')
            
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### avalições medias por Entregador!')
            ava = df1.loc[:, ['Delivery_person_ID','Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(ava)
        
        with col2:
            st.markdown('##### Avaliação média por trânsito')
            df_aux = avaliacoes_mid_por_entregador(df1)
            st.dataframe(df_aux)
#____________________________________________________________________            
            st.markdown('#####  Avaliação média por clima')

            df_aux = avaliacao_mid_por_clima(df1)
            st.dataframe(df_aux)
            
            
    with st.container():
        st.markdown("""---""")
        st.title('velocidade de Entrega')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Top Entregadores mais rápidos')
            
            # Mais rápido
            
            df3= lista_de_entrega(df1, True)
            st.dataframe( df3)
       
        with col2:
            st.markdown('##### Top Entregadores mais lentos')
            
          
            df4 = lista_de_entrega(df1, False)
            st.dataframe( df4 )
            