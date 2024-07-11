from streamlit.components.v1 import html
import ssl
import streamlit as st
import pandas as pd
from ipyvizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step

# Set the app title and configuration
st.set_page_config(page_title='World Population Streamlit Story', layout='centered')

# Center the title using HTML and CSS
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 2.5em;
        margin-top: 0;
        margin-bottom: 0.5em;
    }
    </style>
    <h1 class="title">You and Your Contemporaries in the World</h1>
    """,
    unsafe_allow_html=True
)


# Fix SSL context
ssl._create_default_https_context = ssl._create_unverified_context

# Define the dimensions for the visualization
width = 600
height = 450

# Load and prepare the data
df = pd.read_csv('data.csv', encoding='ISO-8859-1')

# Create form
with st.form(key='story_form'):

    country_list = df['Country'].drop_duplicates()
    selected_country = st.selectbox('Country:', country_list)

    # Determine the subregion for the selected country
    subregion = df['Subregion'].loc[df['Country'] == selected_country].drop_duplicates().values[0]

    continent = df['Continent'].loc[df['Country'] == selected_country].drop_duplicates().values[0]

    gender_list = df['Gender'].drop_duplicates()
    selected_gender = st.selectbox('Gender:', gender_list)

    # Function to match year with generation
    def get_generation(year):
        if 1946 <= year <= 1964:
            return "Baby Boomers"
        elif 1965 <= year <= 1980:
            return "Generation X"
        elif 1981 <= year <= 1996:
            return "Millennial Generation"
        elif 1997 <= year <= 2012:
            return "Generation Z"
        else: 
            return "Generation Alpha"
    

    # Number input for year with automatic generation matching
    selected_year = st.slider('Year Born', min_value=1950, max_value=2024, value=1980)
    generation = get_generation(selected_year)

    # Create a submit button
    submit_button = st.form_submit_button(label='Create Story')

if submit_button:

    # Initialize the ipyvizzu Data object
    vizzu_data = Data()
    vizzu_data.add_df(df)

    # Initialize the story
    story = Story(data=vizzu_data)

    # Slide 1: No. of people with the same sex, born in the same year, same country
    slide1 = Slide(
        Step(
            Data.filter(f"record['Year'] == '{selected_year}' && record['Country'] == '{selected_country}' && record['Gender'] == '{selected_gender}'"),
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
            Data.filter(f"record['Country'] == '{selected_country}' && record['Year'] == '{selected_year}'"),
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
            Data.filter(f"record['Subregion'] == '{subregion}' && record['Year'] == {selected_year} && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Country',
                    'label': 'Country',
                    'title': f"Population of {selected_gender}s in {subregion} In {selected_year}"
                }
            )
        )
    )
    story.add_slide(slide3)

    slide3 = Slide(
        Step(
            Data.filter(f"record['Continent'] == '{continent}' && record['Year'] == {selected_year} && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Country',
                    'label': 'Country',
                    'title': f"Population of {selected_gender}s in {continent} In {selected_year}"
                }
            )
        )
    )
    story.add_slide(slide3)

    slide5 = Slide(
        Step(
            Data.filter(f"record['Year'] == '{selected_year}' && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Continent',
                    'label': 'Population',
                    'title': f"Total Number of People Born In {selected_year} Worldwide"

                }
            )
        )
    )
    story.add_slide(slide5)

    # Switch on the tooltip that appears when the user hovers the mouse over a chart element.
    story.set_feature('tooltip', True)

    html(story._repr_html_(), width=width, height=height)

    st.download_button('Download HTML export', story.to_html(), file_name=f'demographics-{selected_country}.html', mime='text/html')
