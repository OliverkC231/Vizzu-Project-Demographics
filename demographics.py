from streamlit.components.v1 import html
import ssl
import streamlit as st
import pandas as pd
from ipyvizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step

# Set the app title and configuration
st.set_page_config(page_title='World Population Streamlit Story', layout='centered')
st.title('🗺️ Demographics of the World 🗺️')

# Fix SSL context
ssl._create_default_https_context = ssl._create_unverified_context

# Define the dimensions for the visualization
width = 600
height = 450

# Load and prepare the data
df = pd.read_csv('data.csv', encoding='ISO-8859-1')

# Sidebar filters
country_list = df['Country'].drop_duplicates()
selected_country = st.sidebar.selectbox('Country:', country_list)

# Determine the subregion for the selected country
subregion = df['Type'].loc[df['Country'] == selected_country]
selected_subregion = st.sidebar.selectbox('Region:', subregion)

gender_list = df['Gender'].drop_duplicates()
selected_gender = st.sidebar.selectbox('Gender:', gender_list)

# Change selectbox for year to number_input with range
selected_year = st.sidebar.number_input('Year Born', min_value=1950, max_value=2024, value=1950, step=1)

# Create a button to generate the story
if st.sidebar.button('Create Story'):
    # Filter data based on selections
    filtered_data = df[(df['Year'] == selected_year)]

    # Initialize the ipyvizzu Data object
    vizzu_data = Data()
    vizzu_data.add_df(filtered_data)

    # Initialize the story
    story = Story(data=vizzu_data)

    # Slide 1: No. of people with the same sex, born in the same year, same country
    slide1 = Slide(
        Step(
            Data.filter(f"record['Country'] == '{selected_country}' && record['Gender'] == '{selected_gender}'"),
            Config(
                {

                    'color': 'Gender',
                    'size': 'Population',
                    'geometry': 'circle',
                    'label': 'Population',
                    'title': f"Number of {selected_gender}s Born In {selected_year} ({selected_country})"
                }
            )
        )
    )
    story.add_slide(slide1)

    slide2 = Slide(
        Step(
            Data.filter(f"record['Country'] == '{selected_country}'"),
            Config(
                {
                    'color': 'Gender',
                    'size': 'Population',
                    'geometry': 'circle',
                    'label': 'Population',
                    'title': f"Number of Males and Females Born In {selected_country} In {selected_year}"
                }
            )
        )
    )
    story.add_slide(slide2)

    slide3 = Slide(
        Step(
            Data.filter(f"record['Country'] == '{selected_country}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Population',
                    'label': 'Population',
                    'title': f"Total Number of People Born In {selected_country} In {selected_year}"

                }
            )
        )
    )
    story.add_slide(slide3)

    slide4 = Slide(
        Step(
            Data.filter(f"record['Type'] == '{selected_subregion}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Country',
                    'label': 'Population',
                    'title': f"Total Number of People Born In {selected_subregion} In {selected_year}"

                }
            )
        )
    )
    story.add_slide(slide4)

    slide5 = Slide(
        Step(
            Data.filter(f"record['Type'] == '{selected_subregion}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Population',
                    'label': 'Population',
                    'title': f"Total Number of People Born In {selected_subregion} In {selected_year}"

                }
            )
        )
    )
    story.add_slide(slide5)

    slide6 = Slide(
        Step(
            Data.filter(f"record['Year'] == '{selected_year}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Population',
                    'label': 'Population',
                    'title': f"Total Number of People Born In {selected_year} Worldwide"

                }
            )
        )
    )
    story.add_slide(slide6)
    
    # Switch on the tooltip that appears when the user hovers the mouse over a chart element.
    story.set_feature('tooltip', True)

    html(story._repr_html_(), width=width, height=height)

    st.download_button('Download HTML export', story.to_html(), file_name=f'demographics-{selected_country}.html', mime='text/html')
