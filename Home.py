import streamlit as st
import plotly.express  as px

from PIL import Image

st.set_page_config(page_title='Home',
                   page_icon='🍛')


# image_path = 'D:/repos/FTC/'
image = Image.open('logo.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')

st.sidebar.markdown('''___''')

st.write("# Curry Company Growth Dashboard")
st.markdown(
    '''
    Growth Dashboard was built to track growth metrics for Deliverers and Restaurants.
    ### How to use this Growth Dashboard?
    - Company View:
    
        - Management View: General behavioral metrics.
        - Tactical View: Weekly growth metrics.
        - Geographical View: Geolocation insights.
    - Deliverer View:
        - Weekly growth metrics tracking.
    - Restaurant View:
        - Weekly restaurant growth indicators.
    ### Ask for help
    - Data Science Team on Discord
        - @daniel_asgomes
    ''')