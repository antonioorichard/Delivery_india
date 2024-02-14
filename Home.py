#=================
#        Library
#=================
import streamlit as st
from PIL import Image
#____________________________________________________________
#             Sidebar Home



st.set_page_config(page_title = 'Home', page_icon = '🏡', layout = 'wide' )

#________________________________________________________________________________________

#image_path = 'C:/Users\Antonio Richard/OneDrive - acad.ifma.edu.br/Documentos/A Sala de aprendizado/repos/JupyterLab/Dashboards/Delivery_india/'

#image = Image.open(image_path + 'Delivery.jpg')
image = Image.open('Logo_scooter_delivery.png')
st.sidebar.image(image, width = 250)

#========================================
#Barra Laterals
#========================================
st.sidebar.markdown('Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")
    
st.write("Curry Company Growth Dashboard")

st.markdown(

        """
        Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes. 
        ### Como utilizar esse Growth Dashboard?
        - Visão da Empresa:
            -  Visão Gerencial: 
            -  Visão Tática:
            -  Visão Geográfica:
        - Visão do Entregador:
            - Acompanhamento dos indicadores semanais de crescimento
        - Visão dos Restaurantes:
            - Indicadores semanis de crescimento dos restaurantes 
            
        ### Ask for Help
        
        - Time de Data Science no Discord
            - @antonio_richard

        """)
#========================================
#\Barra Lateral
#========================================