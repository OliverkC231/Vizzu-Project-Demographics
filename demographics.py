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
subregion = df['Subregion'].loc[df['Country'] == selected_country].drop_duplicates()
selected_subregion = st.sidebar.selectbox('Region:', subregion)

gender_list = df['Gender'].drop_duplicates()
selected_gender = st.sidebar.selectbox('Gender:', gender_list)

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
selected_year = st.sidebar.number_input('Year Born (1950-2024)', min_value=1950, max_value=2024, value=1950, step=1)
generation = get_generation(selected_year)

if st.sidebar.button('Create Story'):

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
            Data.filter(f"record['Country'] == '{selected_country}' && record['Year'] == '{selected_year}'"),
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
            Data.filter(f"record['Subregion'] == '{selected_subregion}' && record['Year'] == '{selected_year}'"),
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
            Data.filter(f"record['Subregion'] == '{selected_subregion}' && record['Year'] == '{selected_year}'"),
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
                    'color': 'Continent',
                    'label': 'Population',
                    'title': f"Total Number of People Born In The World In {selected_year}"

                }
            )
        )
    )
    story.add_slide(slide6)

    slide7 = Slide(
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
    story.add_slide(slide7)

    slide8 = Slide(
        Step(
            Data.filter(f"record['Generation'] == '{generation}' && record['Country'] == '{selected_country}' && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'size': 'Generation',
                    'geometry': 'circle',
                    'color': 'Generation',
                    'label': 'Population',
                    'title': f"Number of {selected_gender} {generation}'s in {selected_country}"
                }
            )
        )
    )
    story.add_slide(slide8)

    slide9 = Slide(
        Step(
            Data.filter(f"record['Country'] == '{selected_country}' && record['Gender'] == '{selected_gender}'"),
            Config.pie(
                {
                    'by': 'Generation',
                    'angle': 'Population',
                    'title': f"Distribution of {selected_gender}'s by Generation in {selected_country}"
                }
            )
        )
    )
    story.add_slide(slide9)
    
    slide10 = Slide(
        Step(
            Data.filter(f"record['Subregion'] == '{selected_subregion}' && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'label': 'Generation',
                    'color': 'Generation',
                    'title': f"Distribution of {selected_gender}'s by Generation in {selected_subregion}"
                }
            )
        )
    )
    story.add_slide(slide10)

    slide11 = Slide(
        Step(
            Data.filter(f"record['Gender'] == '{selected_gender}'"),
            Config.pie(
                {
                    'by': 'Generation',
                    'angle': 'Population',
                    'title': f"Distribution of {selected_gender}'s by Generation in the World"
                }
            )
        )
    )
    story.add_slide(slide11)
    
    # Switch on the tooltip that appears when the user hovers the mouse over a chart element.
    story.set_feature('tooltip', True)

    html(story._repr_html_(), width=width, height=height)

    st.download_button('Download HTML export', story.to_html(), file_name=f'demographics-{selected_country}.html', mime='text/html')
