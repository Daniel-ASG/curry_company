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


def order_metric(df1):
    cols = ['ID', 'Order_Date']
    aux = (df1[cols].groupby('Order_Date')
                    .count()
                    .rename(columns={'ID':'Order_quantity'})
                    .reset_index())
    fig = px.bar(aux, x='Order_Date', y='Order_quantity')
    return fig


def traffic_order_share(df1):
    cols = ['ID', 'Road_traffic_density']
    aux = (df1[cols].groupby('Road_traffic_density')
                    .count()
                    .reset_index()
                    .rename(columns={'ID':'Order_quantity'}))
    aux = aux[aux['Road_traffic_density'] != 'NaN']
    fig = px.pie(aux, 
                 values='Order_quantity', 
                 names='Road_traffic_density', 
                 title='Order distribution per Road_traffic_density',
                 color_discrete_sequence=px.colors.qualitative.Plotly)
    return fig


def traffic_order_city(df1):
    cols = ['ID', 'Road_traffic_density', 'City']
    aux = (df1[cols].groupby(['Road_traffic_density', 'City'])
                    .count()
                    .reset_index()
                    .rename(columns={'ID':'volume_of_orders'}))
    aux = aux[aux['City'] != 'NaN']
    aux = aux[aux['Road_traffic_density'] != 'NaN']
    fig = px.scatter(aux , 
                     x="City", 
                     y="Road_traffic_density", 
                     size="volume_of_orders", 
                     color='City',
                     size_max=70,
                     color_discrete_sequence=px.colors.qualitative.Plotly)
    return fig


def order_by_week(df1):
    cols = ['ID', 'Order_Date']
    aux = df1[cols]
    aux['Week'] = aux.Order_Date.dt.strftime('%U')
    aux = (aux.groupby('Week')
              .count()
              .reset_index()
              .rename(columns={'ID':'Order_quantity'}))
    aux.Week = aux.Week.astype(int)
    fig = px.line(aux, x='Week', y='Order_quantity')
    return fig


def Order_share_by_week(df1):
    cols = ['ID', 'Order_Date', 'Delivery_person_ID']
    aux = df1[cols]
    aux['Week'] = aux.Order_Date.dt.strftime('%U')
    aux = (aux.groupby('Week')
              .agg({'ID':'count', 'Delivery_person_ID':'nunique'})
              .reset_index()
              .rename(columns={'ID':'volume_of_orders', 'Delivery_person_ID':'Deliverers_quantity'}))
    aux['Orders_per_deliverers'] = aux.volume_of_orders / aux.Deliverers_quantity
    aux.Week = aux.Week.astype(int)
    fig = px.line(aux, x='Week', y='Orders_per_deliverers')
    return fig


def country_maps(df1):
        cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
        aux = (df1[cols].groupby(['City', 'Road_traffic_density'])
                        .median()
                        .reset_index())
        aux = aux[aux['City'] != 'NaN']
        aux = aux[aux['Road_traffic_density'] != 'NaN']
        m = folium.Map(location=[aux.Delivery_location_latitude.mean(),
                                 aux.Delivery_location_longitude.mean()],
                       zoom_start=7,
                       control_scale=True)
        for index, location_info in aux.iterrows():
            folium.Marker(location=[location_info['Delivery_location_latitude'],
                                    location_info['Delivery_location_longitude']],
                          popup=location_info[['City', 'Road_traffic_density']]).add_to(m)
        folium_static(m, width=1024, height=600)
        return None
# ----------------- Start of the logical code structure -----------------

st.set_page_config(page_title='Company View',
                   page_icon='📈',
                   layout="wide")

# -----------------
# Import Dataset
# -----------------
df = pd.read_csv('dataset/train.csv')

# -----------------
# Cleaning Dataset
# -----------------
df1 = clean_code(df)


st.header('Marketplace - Company View')

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
st.sidebar.markdown('### Powered by Comunidade DS')

# date filter
rows = df1.Order_Date < date_slider
df1 = df1.loc[rows,:]

# traffic filter
rows = df1.Road_traffic_density.isin(traffic_options)
df1 = df1.loc[rows,:]




# #########################
# Layout in Streamlit
# #########################
tab1, tab2, tab3 = st.tabs(['Management View', 'Tactical View', 'Geographical View'])
with tab1:
    with st.container():
        # Order Metric
        st.markdown('# Orders by day')
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header('Traffic Order Share')
            fig = traffic_order_share(df1)
            st.plotly_chart(fig, use_container_width=True)            
        with col2:
            st.header('Traffic Order City')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)
with tab2:
    with st.container():
        st.markdown('# Order by week')
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
    with st.container():
        st.markdown('# Order share by week')
        fig = Order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
with tab3:
    st.markdown('# Country Maps')
    country_maps(df1)
    