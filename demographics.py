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
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
        width: 100%;
    }
    .title {
        font-size: 2.5em;
        margin-top: 0;
        margin-bottom: 0.5em;
    }
    </style>
    <div class="centered">
        <h1 class="title">You in the World</h1>
    </div>
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

# Create columns for the selections
col1, col2, col3 = st.columns(3)

with col1:
    country_list = df['Country'].drop_duplicates()
    selected_country = st.selectbox('Country:', country_list)

abr_country = df['ISO3_code'].loc[df['Country'] == selected_country].values[0]

# Determine the subregion for the selected country
subregion = df['Subregion'].loc[df['Country'] == selected_country].drop_duplicates().values[0]

continent = df['Continent'].loc[df['Country'] == selected_country].drop_duplicates().values[0]

with col2:
    gender_list = df['Gender'].drop_duplicates()
    selected_gender = st.selectbox('Gender:', gender_list)

gender2 = df['Gender2'].loc[df['Country'] == selected_country].values[0]

g_type = df['G_Type'].loc[df['Country'] == selected_country].values[0]

# Function to match year with generation
def get_generation(year):
    if 1946 <= year <= 1964:
        return "Baby Boomer"
    elif 1965 <= year <= 1980:
        return "Gen X"
    elif 1981 <= year <= 1996:
        return "Millennial"
    elif 1997 <= year <= 2012:
        return "Gen Z"
    else: 
        return "Gen A"

with col3:
    # Number input for year with automatic generation matching
    selected_year = st.slider('Year Born', min_value=1950, max_value=2024, value=1980)
    generation = get_generation(selected_year)

if st.button('Create Story'):

    # Wrap the presentation in a centered div
    st.markdown('<div class="centered">', unsafe_allow_html=True)

    # Initialize the ipyvizzu Data object
    vizzu_data = Data()
    vizzu_data.add_df(df)

    # Initialize the story
    story = Story(data=vizzu_data)

    def format_population(population):
        if population >= 1e9:
            return f"{population / 1e9:.1f}B"
        elif population >= 1e6:
            return f"{population / 1e6:.1f}M"
        elif population >= 1e3:
            return f"{population / 1e3:.1f}K"
        else:
            return str(population)

    # Slide 1: No. of people with the same sex, born in the same year, same country
    pop1 = df[(df['Year'] == selected_year) & (df['Country'] == selected_country) & (df['Gender'] == selected_gender)]['Population'].sum()
    title1 = f"You are one of {format_population(pop1)} {g_type} born in {selected_year} ({abr_country})"

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
                    'title': title1
                }
            )
        )
    )
    story.add_slide(slide1)

    pop2 = df[(df['Year'] == selected_year) & (df['Country'] == selected_country)]['Population'].sum()
    title2 = f"You are one of {format_population(pop2)} people born in {selected_year} ({abr_country})"

    slide2 = Slide(
        Step(
            Data.filter(f"record['Country'] == '{selected_country}' && record['Year'] == '{selected_year}'"),
            Config(
                {
                    'color': 'Gender',
                    'size': 'Population',
                    'geometry': 'circle',
                    'label': 'Population',
                    'title': title2
                }
            )
        )
    )
    story.add_slide(slide2)

    pop3 = df[(df['Subregion'] == subregion) & (df['Year'] == selected_year) & (df['Gender'] == selected_gender)]['Population'].sum()
    title3 = f"You are one of {format_population(pop3)} {g_type} born in {selected_year} ({subregion})"

    slide3 = Slide()
    slide3.add_step(
        Step(
            Data.filter(f"record['Subregion'] == '{subregion}' && record['Year'] == {selected_year} && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Country',
                    'label': 'ISO3_code',
                    'legend': None,
                    'title': title3
                }
            )
        )
    )
    slide3.add_step(
        Step(
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Country',
                    'label': 'Population',
                    'legend': None,
                    'title': title3
                }
            )
        )
    )
    story.add_slide(slide3)

    pop4 = df[(df['Continent'] == continent) & (df['Year'] == selected_year) & (df['Gender'] == selected_gender)]['Population'].sum()
    title4 = f"You are one of {format_population(pop4)} {g_type} born in {selected_year} ({continent})"

    slide4 = Slide()
    slide4.add_step(
        Step(
            Data.filter(f"record['Continent'] == '{continent}' && record['Year'] == {selected_year} && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Country',
                    'label': 'ISO3_code',
                    'title': title4
                }
            )
        )
    )
    slide4.add_step(
        Step(
        Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Country',
                    'label': 'Population',
                    'title': title4
                }
            )
        )
    )
    story.add_slide(slide4)

    pop5 = df[(df['Year'] == selected_year) & (df['Gender'] == selected_gender)]['Population'].sum()
    title5 = f"You are one of {format_population(pop5)} {g_type} born in {selected_year} in the world"

    slide5 = Slide()
    slide5.add_step(
        Step(
            Data.filter(f"record['Year'] == '{selected_year}' && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Continent',
                    'label': 'Continent',
                    'title': title5
                }
            )
        )
    )
    slide5.add_step(
        Step(
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Continent',
                    'label': 'Population',
                    'title': title5
                }
            )
        )
    )
    story.add_slide(slide5)

    pop6 = df[(df['Country'] == selected_country) & (df['Generation'] == generation) & (df['Gender'] == selected_gender)]['Population'].sum()
    title6 = f"You are one of {format_population(pop6)} {gender2} {generation}s born ({abr_country})"

    slide6 = Slide(
        Step(
            Data.filter(f"record['Country'] == '{selected_country}' && record['Generation'] == '{generation}' && record['Gender'] == '{selected_gender}'"),
            Config.bar(
                {
                    'x': 'Population',
                    'color': 'Generation',
                    'title': title6
                }
            )
        )
    )
    story.add_slide(slide6)

    slide7 = Slide(
        Step(
            Data.filter(f"record['Country'] == '{selected_country}' && record['Generation'] && record['Gender'] == '{selected_gender}'"),
            Config.stackedBar(
                {
                    'x': 'Population',
                    'color': 'Generation',
                    'stackedBy': 'Generation',
                    'title': f"Distribution of {g_type} born since 1950 ({abr_country})"
                }
            )
        )
    )
    story.add_slide(slide7)

    slide8 = Slide()
    slide8.add_step(
        Step(
            Data.filter(f"record['Subregion'] == '{subregion}' && record['Generation'] && record['Gender'] == '{selected_gender}'"),
            Config.bar(
                {
                    'y': 'Population',
                    'y': 'ISO3_code',
                    'color': 'Country',
                    'title': f"Distribution of of all {g_type} born since 1950 ({subregion})"
                }
            )
        )
    )
    slide8.add_step(
        Step(
            Data.filter(f"record['Subregion'] == '{subregion}' && record['Generation'] && record['Gender'] == '{selected_gender}'"),
            Config.stackedBar(
                {
                    'x': 'Population',
                    'y': 'ISO3_code',
                    'stackedBy': 'Generation',
                    'color': 'Generation',
                    'title': f"Distribution of all {g_type} born since 1950 ({subregion})"
                }
            )
        )
    )
    story.add_slide(slide8)

    slide9 = Slide()
    slide9.add_step(
        Step(
            Data.filter(f"record['Continent'] == '{continent}' && record['Generation'] && record['Gender'] == '{selected_gender}'"),
            Config.bar(
                {
                    'x': 'Population',
                    'y': 'Subregion',
                    'color': 'Country',
                    'title': f"Distribution of all {g_type} born since 1950 ({continent})"
                }
            )
        )
    )
    slide9.add_step(
        Step(
            Data.filter(f"record['Continent'] == '{continent}' && record['Generation'] && record['Gender'] == '{selected_gender}'"),
            Config.stackedBar(
                {
                    'x': 'Population',
                    'y': 'Subregion',
                    'stackedBy': 'Generation',
                    'color': 'Generation',
                    'title': f"Distribution of all {g_type} born since 1950 ({continent})"
                }
            )
        )
    )
    story.add_slide(slide9) 

    slide10 = Slide()
    slide10.add_step(
        Step(
            Data.filter(f"record['Generation'] && record['Gender'] == '{selected_gender}'"),
            Config.bar(
                {
                    'x': 'Continent',
                    'y': 'Population',
                    'color': 'Generation',
                    'title': f"Distribution of all {g_type} born since 1950 Worldwide"
                }
            )
        )
    )
    slide10.add_step(
        Step(
            Data.filter(f"record['Generation'] && record['Gender'] == '{selected_gender}'"),
            Config.stackedBar(
                {
                    'x': 'Continent',
                    'y': 'Population',
                    'stackedBy': 'Generation',
                    'color': 'Generation',
                    'title': f"Distribution of all {g_type} born since 1950 worldwide"
                }
            )
        )
    )
    story.add_slide(slide10)

    slide11 = Slide(
        Step(
            Data.filter(f"record['Generation'] && record['Gender'] == '{selected_gender}'"),
            Config.bubble(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Generation',
                    'label': 'Generation',
                    'title': f"Distribution of all {selected_gender}s born since 1950 Worldwide"
                }
            )
        )
    )
    story.add_slide(slide11)

    # Switch on the tooltip that appears when the user hovers the mouse over a chart element.
    story.set_feature('tooltip', True)

    html(story._repr_html_(), width=width, height=height)

    st.download_button('Download HTML export', story.to_html(), file_name=f'demographics-{selected_country}.html', mime='text/html')

    # Close the centered div
    st.markdown('</div>', unsafe_allow_html=True)
