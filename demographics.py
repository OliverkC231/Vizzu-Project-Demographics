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

# Create form
with st.form(key='story_form'):

    country_list = df['Country'].drop_duplicates()
    selected_country = st.selectbox('Country:', country_list)

    abr_country = df['ISO3_code'].loc[df['Country'] == selected_country].values[0]

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
    title1 = f"You are one of {format_population(pop1)} {selected_gender}s born in {selected_year} ({abr_country})"

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
    title2 = f"There were {format_population(pop2)} people born in {selected_year} ({abr_country})"

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
    title3 = f"You are one of {format_population(pop3)} {selected_gender}s born in {selected_year} ({subregion})"

    slide3 = Slide(
        Step(
            Data.filter(f"record['Subregion'] == '{subregion}' && record['Year'] == {selected_year} && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Country',
                    'label': 'Country',
                    'title': title3
                }
            )
        )
    )
    story.add_slide(slide3)

    pop4 = df[(df['Continent'] == continent) & (df['Year'] == selected_year) & (df['Gender'] == selected_gender)]['Population'].sum()
    title4 = f"You are one of {format_population(pop4)} {selected_gender}s born in {selected_year} ({continent})"

    slide4 = Slide(
        Step(
            Data.filter(f"record['Continent'] == '{continent}' && record['Year'] == {selected_year} && record['Gender'] == '{selected_gender}'"),
            Config(
                {
                    'size': 'Population',
                    'geometry': 'circle',
                    'color': 'Country',
                    'label': 'Country',
                    'title': title4
                }
            )
        )
    )
    story.add_slide(slide4)

    pop5 = df[(df['Year'] == selected_year) & (df['Gender'] == selected_gender)]['Population'].sum()
    title5 = f"You are one of {format_population(pop5)} {selected_gender}s born in {selected_year} in the World"

    slide5 = Slide(
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
    story.add_slide(slide5)

    pop6 = df[(df['Country'] == selected_country) & (df['Generation'] == generation) & (df['Gender'] == selected_gender)]['Population'].sum()
    title6 = f"You are one of {format_population(pop6)} {selected_gender} {generation}s born ({abr_country})"

    slide6 = Slide(
        Step(
            Data.filter(f"record['Country'] == '{selected_country}' && record['Generation'] == '{generation}' && record['Gender'] == '{selected_gender}'"),
            Config.bar(
                {
                    'x': 'Population',
                    'color': 'Generation',
                    'label': 'Generation',
                    'title': title6
                }
            )
        )
    )
    story.add_slide(slide6)

    slide7= Slide(
        Step(
            Data.filter(f"record['Country'] == '{selected_country}' && record['Generation'] && record['Gender'] == '{selected_gender}'"),
            Config.stackedBar(
                {
                    'x': 'Population',
                    'color': 'Generation',
                    'stackedBy': 'Generation',
                    'label': 'Generation',
                    'title': f"Distribution of everyone born since 1950 ({abr_country})"
                }
            )
        )
    )
    story.add_slide(slide7)


    

    # Switch on the tooltip that appears when the user hovers the mouse over a chart element.
    story.set_feature('tooltip', True)

    html(story._repr_html_(), width=width, height=height)

    st.download_button('Download HTML export', story.to_html(), file_name=f'demographics-{selected_country}.html', mime='text/html')

    # Close the centered div
    st.markdown('</div>', unsafe_allow_html=True)
