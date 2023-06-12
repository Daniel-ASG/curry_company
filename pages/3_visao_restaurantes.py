# ----------------- Libraries -----------------

from haversine        import haversine
from PIL              import Image
from streamlit_folium import folium_static

import folium
import plotly.graph_objects as go
import plotly.express       as px
import numpy                as np
import pandas               as pd
import streamlit            as st


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


def distance(df1):
    cols = ['Restaurant_latitude', 'Restaurant_longitude', 
            'Delivery_location_latitude', 'Delivery_location_longitude']
    df1['distance'] = df1[cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                          (x['Delivery_location_latitude'], x['Delivery_location_longitude'])),
                                      axis=1)
    avg_distance = round(df1.distance.mean(), 2)
    return avg_distance
    
    
def avg_std_delivery_time(df1, festival, op):
    '''
    This function calculates the average and standard deviation of the delivery time.
    Parameters:
        -Input:
            - df: Dataframe with the data needed for the calculation
            - festival: the delivery period
                - 'Yes': with festival
                - 'No': without festival
            - op:
                'avg_time': calculates the average time
                'std_time': calculates the standard deviation of time
        -Output:
            -df: Dataframe with 2 columns and 1 row
    '''
    cols = ['Time_taken(min)', 'Festival']
    aux = (df1.loc[df1.Festival == festival, cols]
              .groupby('Festival')
              .agg({'Time_taken(min)': ['mean', 'std']}))
    aux.columns = ['avg_time', 'std_time']
    aux = round(aux.loc[:, op], 2)
    return aux


def avg_std_time_grapf(df1):
    aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
    aux.columns = ['avg_time', 'std_time']
    aux = aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control',
                         x=aux.City,
                         y=aux.avg_time,
                         error_y=dict(type='data',
                                      array=aux.std_time)))
    fig.update_layout(barmode='group')
    return fig


def delivery_time_per_city_order_type(df1):
    cols = ['Time_taken(min)', 'City', 'Type_of_order']
    aux = (df1[cols].groupby(['City', 'Type_of_order'])
                    .agg({'Time_taken(min)': ['mean', 'std']}))
    aux.columns = ['avg_time', 'std_time']
    aux = aux.reset_index()
    return aux


def avg_delivery_time_by_city(df1):
    cols = ['Restaurant_latitude', 'Restaurant_longitude', 
            'Delivery_location_latitude', 'Delivery_location_longitude']
    avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
    fig = go.Figure(data=[go.Pie(labels=avg_distance.City, 
                                 values=avg_distance.distance, 
                                 pull=[0, 0.1, 0])])
    return fig


def avg_rating_per_traffic(df1):
    aux = df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']].\
              groupby(['City', 'Road_traffic_density']).\
              agg({'Time_taken(min)': ['mean', 'std']})
    aux.columns = ['avg_time', 'std_time']
    aux = aux.reset_index()
    fig = px.sunburst(aux, 
                      path=['City', 'Road_traffic_density'],
                      values='avg_time',
                      color='std_time',
                      color_continuous_scale='RdBu',
                      color_continuous_midpoint=np.average(aux.std_time))
    return fig
# ----------------- Start of the logical code structure -----------------

st.set_page_config(page_title='Restaurant View',
                   page_icon='🍽️',
                   layout="wide")

# -----------------
# Import Dataset
# -----------------
df = pd.read_csv('dataset/train.csv')

# -----------------
# Cleaning Dataset
# -----------------
df1 = clean_code(df)


st.header('Marketplace - Restaurants View')
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
tab1, tab2, tab3 = st.tabs(['Management View', '_', '_'])
with tab1:
    with st.container():
    # Order Metric
        st.markdown('# Overall Metrics')
        col1, col2, col3, col4, col5, col6 = st.columns(6, gap='large')
        with col1:
            quantidade = df1.Delivery_person_ID.nunique()
            col1.metric('Unique deliverers', quantidade)
        with col2:
            avg_distance = distance(df1)
            col2.metric('Average distance', avg_distance)          
        with col3:
            aux = avg_std_delivery_time(df1, 'Yes', 'avg_time')
            col3.metric('Avg delivery time - festival', aux)
        with col4:
            aux = avg_std_delivery_time(df1, 'Yes', 'std_time')
            col4.metric('Std delivery time - festival', aux)            
        with col5:
            aux = avg_std_delivery_time(df1, 'No', 'avg_time')
            col5.metric('Avg delivery time - w/o festival', aux)
        with col6:
            aux = avg_std_delivery_time(df1, 'No', 'std_time')
            col6.metric('Std delivery time - w/o festival', aux)            
    with st.container():
        st.markdown('''---''')
        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.header('Delivery time by city')
            fig = avg_std_time_grapf(df1)
            st.plotly_chart(fig)
        with col2:
            st.header('Delivery time per city and order type')
            aux = delivery_time_per_city_order_type(df1)
            st.dataframe(aux)                                                 
    with st.container():
        st.markdown('''---''')
        st.markdown('# Average delivery time by city')
        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.markdown('##### Average delivery time per city')
            fig = avg_delivery_time_by_city(df1)
            st.plotly_chart(fig)
        with col2:
            st.markdown('##### Average rating per traffic')
            fig = avg_rating_per_traffic(df1)
            st.plotly_chart(fig)