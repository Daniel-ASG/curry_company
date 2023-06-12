# ----------------- Libraries -----------------

from haversine        import haversine
from PIL              import Image
from streamlit_folium import folium_static

import folium
import plotly.express  as px
import numpy           as np
import pandas          as pd
import streamlit       as st


# ==========================================================
#                       Functions
# ==========================================================

def clean_code(df1):
    '''
    This function has the responsibility of clearing the dataframe.

    Cleaning types:
        1. Removing NaN data
        2. Changing the type of the data column
        3. Remove spaces from text variables
        4. Formatting the given column
        5. Clean up time column (remove text from numerical variable)
        
    Input: Dataframe
    Output: Dataframe
    '''
    # Remove space from string
    df1.ID = df1.ID.str.strip()
    df1.Road_traffic_density = df1.Road_traffic_density.str.strip()
    df1.Festival = df1.Festival.str.strip()
    df1.City = df1.City.str.strip()
    df1.Type_of_vehicle = df1.Type_of_vehicle.str.strip()
    df1.Type_of_order = df1.Type_of_order.str.strip()
    df1.Delivery_person_Age = df1.Delivery_person_Age.str.strip()
    df1.multiple_deliveries = df1.multiple_deliveries.str.strip()

    # Converting text/category/string to integers
    linhas_sem_NaN = df1.Delivery_person_Age != 'NaN'
    df1 = df1.loc[linhas_sem_NaN, :].copy()
    df1.Delivery_person_Age = df1.Delivery_person_Age.astype(int)

    linhas_sem_NaN = df1.multiple_deliveries != 'NaN'
    df1 = df1.loc[linhas_sem_NaN, :].copy()
    df1.multiple_deliveries = df1.multiple_deliveries.astype(int)

    # Converting text/category/string to float
    df1.Delivery_person_Ratings = df1.Delivery_person_Ratings.astype(float)

    # Converting text/category/string to Datetime
    df1.Order_Date = pd.to_datetime(df1.Order_Date, format='%d-%m-%Y')

    # Command to remove text from numbers
    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.extract(r'(\d+)').astype(int)

    # Command to remove unnecessary text
    df1.Weatherconditions = df1.Weatherconditions.str.replace('conditions ', '')

    # Removal of lines containing 'NaN
    df1 = df1.loc[df1.Road_traffic_density != 'NaN', :].copy()
    df1 = df1.loc[df1.City != 'NaN', :].copy()
    df1 = df1.loc[df1.Festival != 'NaN', :].copy()
    return df1


def top_delivers(df1, top_ascending):
    cols = ['Delivery_person_ID', 'City', 'Time_taken(min)']
    df_aux = (df1.loc[:, cols]
                 .groupby(['City', 'Delivery_person_ID'])
                 .mean()
                 .sort_values('Time_taken(min)', ascending=top_ascending)
                 .reset_index().head(10))
    df_aux01 = df_aux.loc[df_aux.City == 'Metropolitian', :].head(10)
    df_aux02 = df_aux.loc[df_aux.City == 'Semi-Urban', :].head(10)
    df_aux03 = df_aux.loc[df_aux.City == 'Urban', :].head(10)
    aux = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return aux

# ----------------- Start of the logical code structure -----------------

st.set_page_config(page_title='Deliverers View',
                   page_icon='🚚',
                   layout="wide")

# -----------------
# Import Dataset
# -----------------
df = pd.read_csv('dataset/train.csv')

# -----------------
# Cleaning Dataset
# -----------------
df1 = clean_code(df)


st.header('Marketplace - Deliverers View')

# #########################
#         Sidebar
# #########################
# image_path = 'D:/repos/FTC/'
image = Image.open('logo.jpg')
st.sidebar.image(image, width=120)
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')

st.sidebar.markdown('''___''')
st.sidebar.markdown('## select the cut-off date')
date_slider = st.sidebar.slider('Up to what value?',
                                value=pd.datetime(2022,4,13),
                                min_value=pd.datetime(2022,2,11),
                                max_value=pd.datetime(2022,4,6),
                                format='DD-MM-YYYY')

st.sidebar.markdown('''___''')
traffic_options = st.sidebar.multiselect('What are the traffic conditions?',
                                         df1.Road_traffic_density.unique().tolist(),
                                         default=df1.Road_traffic_density.unique().tolist())

st.sidebar.markdown('''___''')
weather_options = st.sidebar.multiselect('What are the weather conditions?',
                                         df1.Weatherconditions.unique().tolist(),
                                         default=df1.Weatherconditions.unique().tolist())

st.sidebar.markdown('''___''')
st.sidebar.markdown('### Powered by Comunidade DS')

# date filter
rows = df1.Order_Date < date_slider
df1 = df1.loc[rows,:]

# traffic filter
rows = df1.Road_traffic_density.isin(traffic_options)
df1 = df1.loc[rows,:]

# weather filter
rows = df1.Weatherconditions.isin(weather_options)
df1 = df1.loc[rows,:]




# #########################
# Layout in Streamlit
# #########################
tab1, tab2, tab3 = st.tabs(['Management View', '_', '_'])
with tab1:
    with st.container():
        # Order Metric
        st.markdown('# Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            maior = df1.Delivery_person_Age.max()
            col1.metric('Age of the oldest deliverer', maior)
        with col2:
            menor = df1.Delivery_person_Age.min()
            col2.metric('Age of the youngest deliverer', menor)
        with col3:
            maior = df1.Vehicle_condition.max()
            col3.metric('Better vehicle condition', maior)
        with col4:
            menor = df1.Vehicle_condition.min()
            col4.metric('Worst vehicle condition', menor)
    with st.container():
        st.markdown('''---''')
        st.markdown('# Ratings')
        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.markdown('##### Average rating per deliverer')
            cols = ['Delivery_person_Ratings', 'Delivery_person_ID']
            aux = round(df1[cols].groupby('Delivery_person_ID').mean().reset_index(), 2)
            st.dataframe(aux)
        with col2:
            st.markdown('##### Average rating per traffic')
            cols = ['Delivery_person_Ratings', 'Road_traffic_density']
            aux = round(df1[cols].groupby('Road_traffic_density').agg(['mean', 'std']), 2)
            aux.columns = ['Delivery_person_Ratings_mean', 'Delivery_person_Ratings_std']
            aux.reset_index()
            st.dataframe(aux)
            
            st.markdown('##### Average rating per weather condition')
            cols = ['Delivery_person_Ratings', 'Weatherconditions']
            aux = round(df1[cols].groupby('Weatherconditions').agg(['mean', 'std']), 2)
            aux.columns = ['Delivery_person_Ratings_mean', 'Delivery_person_Ratings_std']
            aux.reset_index()
            st.dataframe(aux)
    with st.container():
        st.markdown('''---''')
        st.markdown('# Delivery Speed')
        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.markdown('##### Top Fastest Deliverers')
            top = top_delivers(df1, True)
            st.dataframe(top)
        with col2:
            st.markdown('##### Top Slowest Deliverers')
            top = top_delivers(df1, False)
            st.dataframe(top)