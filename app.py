#   -------------------------------------   #
###    ---------   MODULES   ---------    ###
#   -------------------------------------   #

# Streamlit Modules
import streamlit as st
from streamlit_folium import st_folium

# Map Modules
import geopandas as gpd
import folium
from folium.plugins import Draw
from shapely.geometry import shape
import branca.colormap as cm

# Data Modules
import pandas as pd
import numpy as np

# Essential Modules
import json

# Setup imports
from setup import df as setup_df
from setup import wards_df as wards_df





#    -------------------------------------------   #
###    ---------   FUNCTION SETUP   ---------    ###
#    -------------------------------------------   #

def display_group(df, area):
    ret = df.groupby(area).agg({
        "chicago_energy_rating": "sum",
        "id": "count"
    }).reset_index()
    ret.columns = [area, "Total_Energy_Rating", "Total_Buildings"]
    ret['Mean_Rating'] = ret.apply(lambda x: round(x["Total_Energy_Rating"]/x["Total_Buildings"], 2), axis=1)
    return ret

def make_shape(geo):
    try:
        if pd.isna(geo):
            return None
        if isinstance(geo, dict):
            return shape(geo)
        if isinstance(geo, str):
            geo = geo.strip()
            if not geo or geo.lower() in ['nan', 'null']:
                return None
            geo = json.loads(geo)
            return shape(geo)
        return None
    except Exception as e:
        print(f"Skipping invalid geometry: {geo} — {e}")
        return None





#    ------------------------------------------   #
###    ---------   WEBSITE SETUP   ---------    ###
#    ------------------------------------------   #

st.set_page_config(layout="wide", page_title="Dylan's URP 535 Final", page_icon="🏙️")
st.header("Understanding the State of Energy Efficiency in Chicago")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Home", "Context", "Data Collection", "Ethical Considerations", "Data Visualization", "Findings"])





#    ------------------------------------------   #
###    -----------   HOME PAGE   -----------    ###
#    ------------------------------------------   #
with tab1:
    col1, col2 = st.columns([3,5])
    with col1:
        st.header("Hello!   I'm Dylan Ingui.")
        st.write("I am a junior at the University of Michigan studying Urban Technology with a minor in \
            User Experience Design.")
        st.write("I come from a background in high performance building, and the purpose of my work is to \
            promote and practice energy efficiency in urban contexts.  This project was created as a way to understand and visualize \
            the landscape of energy efficiency in Chicago.")
    with col2:
        st.image('images/Thermal_Image.jpg', width=500)
    st.write("------------------------------------------------------------------------------")





#    --------------------------------------------   #
###    ---------   PROJECT CONTEXT   ---------    ###
#    --------------------------------------------   #
with tab2:
    st.header("Contextualizing Energy Efficiency in America")
    col1, col2 = st.columns([3,5])
    with col1:
        st.image('images/Draft_Chicago_Energy_Rating_Placard.jpg', width=450)
    with col2:
        st.write("In recent years, there has been an emerging trend targeting energy efficiency standards in the urban built environment across American cities. \
                New York City gives large buildings an energy limit through [Local Law 97](https://www.nyc.gov/site/buildings/codes/ll97-greenhouse-gas-emissions-reductions.page#:~:text=Local%20Law%2097%20allows%20for,Questions%20and%20LL97%20RECs%20Policy.),\
                and taxes large building owners that refuse to comply.  Boston's [BERDO 2.0](https://www.iesve.com/discoveries/view/40249/berdo-2-0-decarbonizing-boston) \
                and DC's [BEPS](https://buildinginnovationhub.org/resource/regulation-basics/?gad_source=1&gclid=CjwKCAjw8IfABhBXEiwAxRHlsCHfp_HKfMvclnSkz7fMnW7demaNLFQ3MlWtc43EwZUbwqz2srFZYBoCfaMQAvD_BwE) programs were \
                introduced to place strict emissions thresholds on certain building types.  Finally, San Francisco's [Climate Action Plan](https://sfplanning.org/project/san-francisco-climate-action-plan#about) \
                focuses more on electrification and decarbonization rather than on emission caps.")
        
        st.write("Chicago, however, is still in the earlier stages of formal climate legislation.  One of their current initatives is an effort \
                to promote energy efficiency through the [Chicago Energy Rating](https://www.chicago.gov/city/en/progs/env/ChicagoEnergyRating.html) system.  \
                The program requires buildings over 50,000 square feet to report their energy consumption to the city.  The city then provides these buildings an energy \
                rating from one to four stars.")
        
        st.write("This project will utilize the [Chicago Data Portal](https://data.cityofchicago.org/) to explore patterns between each energy efficiency and building permit data over time \
                as a means to understand the concentration of energy efficiency efforts or lack thereof.")
    st.write("------------------------------------------------------------------------------")





#    ---------------------------------------------   #
###    -----------   METHODS PAGE   -----------    ###
#    ---------------------------------------------   #
with tab3:
    st.header("Data Collection Methodology")
    st.write("All three data sources were found under Chicago's Open Data Portal.  This means that all three datasets are public and free to access via file or api.")
    
    st.write("The first dataset used was [Chicago's Energy Benchmarking](https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c/about_data). \
            This dataset contains Chicago Energy Ratings with year of report, property information, Chicago energy rating, energy star score, location data, and more. \
            The dataset was cleaned by removing columns with missing report dates (data_year), location (longitude and/or latitude), or energy reports.")
    
    st.write("The second dataset used contained [Building Permits](https://data.cityofchicago.org/Buildings/Building-Permits/ydr8-5enu/about_data). \
            This dataset contains building permit data with permit information, address information, location data, and more. \
            The data was initially seperately pulling 50,000 completed new construction permits and over 26,000 completed retrofit/alteration construction permits. \
            Both dataframes were cleaned by removing dozens of columns pertaining to contractor contact information as these columns were irrelevant to the scope of the project. \
            From here, the dataframes were concatenated or added together, then stripped of all their columns except for their id number (id), permit type (permit_type), and location (latitude, longitude, and location).")

    st.write("The third and final dataset used contained Chicago's [Ward Boundaries](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Wards-2023-/p293-wvbd/about_data). \
            This dataset only contained columns with ward number, geometry, area, length, and last edited date.")
    
    st.write("At this point, there were three dataframes.  To ensure that the coordinates of each dataset's buildings matched up, the longitude and latitudes of both the \
            energy benchmarking and building permit datasets ")





#    ---------------------------------------------------   #
###    ------------   ETHICS AND GOALS   ------------    ###
#    ---------------------------------------------------   #
with tab4:
    st.header("Ethical Considerations")
    st.write("While these datasets don't contain any personal information, the grouping of buildings by ward prevents any address or contractor information from being accidentally shared. \
            The purpose of this project is to provide a macro-overview of the city's energy efficiency trends as a way to understand it further, and this doesn't require address information. \
            Another consideration is to remind ourselves that because this is a dataset required of only large buildings (50,000+ sf), certain areas with smaller buildings on average might be \
            underreported or represented.  Lower income wards may especially be impacted due to the correlation between lower-income neighborhoods and disinvestment rates. \
            Existing or other energy efficient buildings such as Passive Houses or WELL certified buildings may be left out of this data as a result of this despite being extremely sustainable. \
            However, as a means of understanding energy efficiency in the city, utilizing the data that is present is also important as a means of visualizing gaps in the city's energy efficient building stock. \
            By highlighting what areas are sustainably thriving from the city's perspective, this project provides a valuable perspective in understanding the cross-section of Chicago's existing energy infrastructure, policy, and investment.")




#    ----------------------------------------------------   #
###    ---------   DATA VISUALIZATION PAGE   ---------    ###
#    ----------------------------------------------------   #
with tab5:
    col1, col2 = st.columns([1, 2])





    #    --------------------------------------------   #
    ###    -------------   SELECTS   -------------    ###
    #    --------------------------------------------   #
    # Year slider
    min_year = setup_df['data_year'].min()
    max_year = setup_df['data_year'].max()

    with col1:
        st.write("------------------------------------------------------------------------------")
        
        year = st.slider(
            "Select Year",
            min_value=min_year,
            max_value=max_year,
            step=1
        )

        # Permit data select
        permit = st.selectbox(
            "Select Data Visualized",
            ("All Permits", "Retrofit Permits", "Newbuild Permits"),
        )

        # Select dislayed metric
        display = st.selectbox(
            "Select Displayed Metric:",
            ("Total Projects Built", "Average Energy Rating")
        )

        # Print what user is viewing
        st.write("You're viewing:", permit, " with a Chicago energy efficiency score since", str(year), '.')
        st.write("The gradient displayed is based on", display, " and is visualized by Chicago's ward .")
        st.write("------------------------------------------------------------------------------")




    #    --------------------------------------------   #
    ###    -----------   DATA FILTER   -----------    ###
    #    --------------------------------------------   #

    # Filter by year and permit type
    permit_dict = {"Retrofit Permits" : "PERMIT - RENOVATION/ALTERATION", "Newbuild Permits" : "PERMIT - NEW CONSTRUCTION"}
    if permit == "All Permits":
        df_map = setup_df[setup_df['data_year'] <= year]
    else:
        df_map = setup_df[
            (setup_df['data_year'] <= year) &
            (setup_df['permit_type'] == permit_dict[permit])
        ]

    grouped = display_group(df_map, 'ward')
    merged = wards_df.merge(grouped, on="ward")
    merged['geometry'] = merged['the_geom'].apply(make_shape)
    merged = gpd.GeoDataFrame(merged, geometry="geometry", crs="EPSG:4326")





    #    --------------------------------------------   #
    ###    --------   MAP VISUALIZATION   --------    ###
    #    --------------------------------------------   #
    if display == "Total Projects Built":
        color_by = "Total_Buildings"
        percents = [0, .04, .25, .5, .9]
    else:
        color_by = "Mean_Rating"
        percents = [0, .3, .5, .7, .9]

    # Get min and max
    min_val = merged[color_by].min()
    max_val = merged[color_by].quantile(0.95)

    # Create threshold manually
    thresholds = [min_val + (max_val - min_val) * p for p in percents]

    # Colors!
    if display == "Total Projects Built":
        colors = ['#e7efff', '#a4bbea', '#6c90d9', '#3b6bca', '#002f8c']
        caption = "Total Projects by Ward"
    else:
        colors = ['#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#31a354']
        caption = "Average Energy Rating by Ward"

    # Create a step colormap
    colormap = cm.StepColormap(
        colors=colors,
        index=thresholds,
        vmin=min_val,
        vmax=max_val,
        caption=caption
    )





    #    --------------------------------------------   #
    ###    --------   MAP VISUALIZATION   --------    ###
    #    --------------------------------------------   #

    with col2:
        # Create map (centered around Chicago)
        m = folium.Map(location=[41.875, -87.63], zoom_start=9.5)
        
        ticks = 5
        equal_ticks = np.linspace(min_val, max_val, ticks + 1)

        # Add GeoJson layer
        folium.GeoJson(
            merged,
            style_function=lambda feature: {
                "fillColor": colormap(feature["properties"][color_by]),
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.6,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["ward", "Mean_Rating", "Total_Buildings"],
                aliases=["Ward", "Average Energy Rating", "Total Projects Built"]
            )
        ).add_to(m)
        
        colormap.add_to(m)

        # Display map in Streamlit
        st_data = st_folium(m, width=800, height=500)





#    --------------------------------------------   #
###    ----------   FINDINGS PAGE   ----------    ###
#    --------------------------------------------   #
with tab6:
    st.header('Project Findings')
    col1, col2 = st.columns([2,5])
    with col1:
        st.image("images/Tot_Ret_2023.png", width=500)
    with col2:
        st.write("In 2023, which is the most recent data available, areas like Chicago's downtown area (wards 42, 27, and 2) is a clear standout in both total buildings \
                and average energy rating.  Other wards with waterfront access similarly have a larger amount of total buildings, but don't have very high average energy \
                ratings.  This can all be attested to Chicago's waterfront containing a higher density of large buildings for both commercial and residential usage.  \
                Because the Chicago Energy Rating requires all buildings over 50,000 square feet to report their energy consumption, these areas likely contain a larger \
                number of smaller renovations and large new builds that didn't incorporate energy efficiency but had to report their building's energy consumption regardless.")
        
    col1, col2 = st.columns([5,2])
    with col1:
        st.write("A finding that was surprising, however, was that despite not having quite as many total buildings, ward 41, which includes O'Hare International Airport, \
                and ward 20, which includes south side, have fairly high average energy ratings, even meeting that of Chicago's vibrant downtown area.  Some potential \
                reasons behind ward 41's success could be a marketing strategy on behalf of O'Hare or nearby hotels utilizing the selling points and amenities that \
                come with energy efficient buildings like filtered fresh air and reduced amounts of dust.  Ward 20, however, is more likely due to a policy or \
                legislation reason.  Especially with a recent focus on climate equity in grant funding and nonprofits, ward 20, which has a high disinvestment \
                and vacancy rate, is likely to be required to meet more energy efficient standards as a result of LIHTC requirements.")
    with col2:
        st.image("images/Avg_All_2023.png", width=500)