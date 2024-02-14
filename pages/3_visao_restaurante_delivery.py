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
import haversine
from haversine import haversine

# \Librarys-----------------------
st.set_page_config(page_title = 'Visão dos Restaurantes', page_icon = ' 🍲🍴 ', layout = 'wide' )

#Importar Dataframe*********************************
df = pd.read_csv('Dataset/train.csv')
#\Importar Dataframe--------------------------------


#Limpeza ******************************************
#df = pd.read_csv('train.csv')
df1 = df.copy()
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
# Acresentando semana

df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )

cols = ['Restaurant_latitude','Restaurant_longitude', 'Delivery_location_latitude','Delivery_location_longitude']


#\VISÃO EMPRESA---------------------------------------
#========================================
#Barra Laterals
#========================================

st.header('Marketplace - Visão do Restaurante')

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
#st.dataframe(df1)
# FILTRO SLIDER
st.sidebar.markdown('### Powered by Antonio Richard')

# ==========================
# Layout no Streamlit
# ==========================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])
with tab1:
    with st.container( height = None, border = True):
        col1, col2, col3, col4, col5, col6 = st.columns(6) 
        with col1:
            col1.metric("Entregadores \n únicos", len(df1['Delivery_person_ID'].unique()))
            with st.expander("more"):
                st.write(" Entregas únicas.  ")
        with col2:
            #haversine((latitude, longetude), (latitude, longetude))
            df1['distace'] = df1.loc[0:10, cols].apply(lambda x:
                                      haversine(
                                          (x['Restaurant_latitude'], x['Restaurant_longitude']               ),
                                          (x['Delivery_location_latitude'], x['Delivery_location_longitude'] )
                                               ),
                          axis = 1    )

            avg_distance =np.round( df1['distace'].mean(), 2)
            col2.metric('A distancia média das entregas é: {:.2f} Km', avg_distance)
            with st.expander("more"):
                st.write(" Distância média das entregas. ")
            
        
            
        with col3:
            df_aux =( df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)':['mean','std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
           
            df_aux = np.round(df_aux.loc[df_aux['Festival'] == 'Yes ', 'avg_time'], 2)
            col3.metric('Tempo médio de entrega no festival',df_aux )
            with st.expander("more"):
                st.write("Tempo médio de entrega no festivavl.")
            
            #st.title('e')
        with col4:
            df_aux =( df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)':['mean','std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            
           
            df_aux = np.round(df_aux.loc[df_aux['Festival'] == 'Yes ', 'std_time'], 2)
            col4.metric('Desvio padrão de entrega no festival', df_aux)
            with st.expander("more"):
                st.write("Desvio padrão de entrega no festival.")
            
        with col5:
            df_aux =( df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)':['mean','std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
        
            df_aux = np.round(df_aux.loc[df_aux['Festival'] == 'No ', 'avg_time'], 2)
            col5.metric('Média de entrega sem festival', df_aux)
            with st.expander("more"):
                st.write(" Média de entrega sem festival")
            
        with col6:
            df_aux =( df1.loc[:,['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)':['mean','std']}))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
                 
           
            df_aux = np.round(df_aux.loc[df_aux['Festival'] == 'No ', 'std_time'], 2)
            col6.metric('Desvio padrão de entrega sem festival', df_aux)
            
            with st.expander("more"):
                st.write("Desvio padrão de entrega sem festival ")
#        st.title('Overall Metrics')
        st.markdown("""---""")
    
    with st.container( border = True):
            
            col1, col2 =  st.columns(spec = [1.3 , 0.8 ], gap = "large")
            with col1:
                # Gráfico de barras
                cols= [ 'City', 'Time_taken(min)']
                df_aux = df1.loc[:, cols].groupby(['City']).agg({'Time_taken(min)': ['mean', 'std']})

                df_aux.columns= ['avg_time', 'std_time']

                df_aux = df_aux.reset_index()

                fig = go.Figure()
                fig.add_trace(go.Bar(name= 'Control',
                                      x = df_aux['City'],
                                      y = df_aux['avg_time'],
                                      error_y = dict(type = 'data', array = df_aux['std_time'])))

                st.plotly_chart(fig)
            with col2:
                st.markdown("## Tempo médio e o desvio padrão de entrega por cidade.")
                

               
            
    st.markdown("""---""")
    
    
    with st.container():
        
        col1, col2 =  st.columns(spec = [1.3 , 0.8 ], gap = "large")
        with col1:     


           # Gráfico de Sunburst
            cols =  ['City', 'Time_taken(min)', 'Road_traffic_density']
            df_aux= df1.loc[:,cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})

            df_aux.columns = ['avg_time', 'std_time']

            df_aux = df_aux.reset_index()

            fig = px.sunburst(df_aux, path = ['City', 'Road_traffic_density'], values = 'avg_time',
                              color = 'std_time', color_continuous_scale = 'RdBu',
                              color_continuous_midpoint = np.average(df_aux['std_time']))
            st.plotly_chart(fig)
        with col2:
            
            st.markdown('## Tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.')

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("## Tempo médio e desvio padrão do tempo de entrega por cidade e por tipo de pedido.")
            cols = ['City', 'Time_taken(min)', 'Type_of_order']
            df_aux = df1.loc[:,cols].groupby(['City' , 'Type_of_order']).agg({'Time_taken(min)':['mean', 'std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)
        
        with col2:
            # Gráfico de Pizza
            
            cols = ['Delivery_location_latitude','Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']

            df1['distance'] = df1.loc[:, cols].apply(lambda x:
                                  haversine(
                                      (x['Restaurant_latitude'], x['Restaurant_longitude']               ),
                                      (x['Delivery_location_latitude'], x['Delivery_location_longitude'] )
                                           ),
                          axis = 1    )


            avg_distance = df1.loc[:,['City', 'distance']].groupby('City').mean().reset_index()

            
            fig= go.Figure(data= [go.Pie(labels = avg_distance['City'], values = avg_distance['distance'], pull = [0.03, 0.1, 0.03])])
            st.plotly_chart(fig)    
            st.markdown("## Distância média entre restaurantes e entregas por cidade.")
# ==========================
# \Layout no Streamlit
# ==========================
