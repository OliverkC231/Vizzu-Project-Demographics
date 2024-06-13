from streamlit.components.v1 import html
import ssl
import streamlit as st 
import pandas as pd
from ipyvizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step

ssl._create_default_https_context = ssl._create_unverified_context

# Set the app title and 
st.set_page_config(page_title='World Population Streamlit Story', layout='centered')
st.title('🗺️ Demographics of the World 🗺️') 
st.subheader('An interactive ipyvizzu-story in Streamlit')

width = 650
height = 500

# Creates Dataframe from Countries list.csv
data = Data()
df = pd.read_csv('Countries list.csv')
data.add_df(df)

country = df['Country']
country_select = st.sidebar.selectbox('Select Your Country or Area:', country)
region = df['Type'].loc[df['Country'] == country_select]
region_select = st.sidebar.selectbox('Your Region:', region)

# Dropdown menu for gender
gender = st.sidebar.selectbox(
    'Gender:', ('Male','Female')
)
# Age saved as int
age = st.sidebar.number_input('Age:', min_value=0, max_value=122)


if st.sidebar.button("Create Story"):
    width=570
    height=400

    df_country = df[df['Country'] == country_select]
    data.add_df(df_country)
    st.dataframe(df_country)

    style = Style(
        {
            "plot": {
                "yAxis": {
                    "label": {
                        "fontSize": "1em",
                        "paddingRight": "1.2em",
                    },
                    "title": {"color": "#ffffff00"},
                },
                "xAxis": {
                    "label": {
                        "angle": "2.5",
                        "fontSize": "0.8em",
                        "paddingRight": "0em",
                        "paddingTop": "1em",
                    },
                    "title": {"fontSize": "1em", "paddingTop": "2.5em"},
                },
            },
            "logo": {"width": "5em"},
        }
    )

    

    # Create story object, add data and style settings to it
    story = Story(data=data, style=style)
    
    # Set the size of the HTML element
    # that appears within the notebook
    story.set_size(width, height)
    
    # Switch on the tooltip that appears
    # when the user hovers the mouse over a chart element
    story.set_feature("tooltip", True)
    
    
    # Each slide here is a page in the final interactive story
    # Add the first slide
    slide1 = Slide(
        Step(
            Config.bar({
                'x': 'Total Population', 'title': 'Population of ' + country_select
            })
        )
    )
    # Add the slide to the story
    story.add_slide(slide1)

    # Switch on the tooltip that appears when the user hovers the mouse over a chart element.
    story.set_feature('tooltip', True)

    html(story._repr_html_(), width=width, height=height)

    st.download_button('Download HTML export', story.to_html(), file_name=f'demographics-of-the-world-{country}.html', mime='text/html')


