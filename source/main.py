# An app to plot the ASCE 7-22 response spectra
# given the user selected location and site class(es).

# Import libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import scraper
import functions
import ASCE
import plotting
import make_dataframe

# Title for app.
st.header('ASCE 7-22 Response Spectra Plotter')

# Set a session state.
if 'lat' not in st.session_state:
    st.session_state['lat'] = None
if 'lon' not in st.session_state:
    st.session_state['lon'] = None
if 'risk_category' not in st.session_state:
    st.session_state['risk_category'] = None
if 'title' not in st.session_state:
    st.session_state['title'] = None
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = None
if 'vs100_slider' not in st.session_state:
    st.session_state['vs100_slider'] = None

# Get initial user input
if st.session_state['user_input'] is None:
    # Add a welcome message and instructions
    st.write('Please submit required data in sidebar to the left.')

    # User input location, confirm on map
    with st.sidebar:
        # SIDEBAR: Tell user to start here.
        st.header('Start by Entering Options Here')

        # SIDEBAR: latitude and longitude inputs.
        lat = st.text_input('Enter latitude', value=47.56)
        lon = st.text_input('Enter longitude', value=-122.01)

        # SIDEBAR: submit button for lat, lon
        check_location = st.button('Check Location')

        if check_location and lat and lon:
            try:
                lat_float = float(lat)
                lon_float = float(lon)
                loc = pd.DataFrame({
                    'lat': [lat_float],
                    'lon': [lon_float]
                    })
                st.map(data=loc, zoom=8)
            except ValueError:
                st.error("Please enter valid latitude and longitude values.")

        # SIDEBAR: use a form to get user inputs
        st.header('After confirming location, select spectrum options')
        with st.form('user_inputs'):
            # SIDEBAR: input risk category, only 1.
            risk_category = st.radio(
                'Select risk category',
                ['I', 'II', 'III', 'IV'],
                index=2 #Default to III
                )

            # SIDEBAR: name the location of the project.
            title = st.text_input('Project Location', value="MyProjectCity")

            # SIDEBAR: submit button
            user_input = st.form_submit_button("SUBMIT")

            # Remember the user inputs that were submitted
            if user_input:
                st.session_state['user_input'] = user_input
                st.session_state['lat']=lat
                st.session_state['lon']=lon
                st.session_state['risk_category'] = risk_category
                st.session_state['title'] = title

# Once there is a dictionary of user inputs, proceed with processing.
# List the keys in the session_state dictionary
keys = ['user_input', 'lat', 'lon', 'risk_category', 'title']

if all(st.session_state.get(key) is not None for key in keys):
    def do_all_the_processing():
        # Get the value of the slider
        vs100 = st.session_state.vs100_slider
        site_class_user = ASCE.asceTable(vs100)
        st.write(f"The selected Vs100 = {vs100}, Site Class {site_class_user}")

        # calculate 1.3* and /1.3
        vs100_multiplied = round(vs100 * 1.3)
        vs100_divided = round(vs100 // 1.3)

        # fetch site classes for the over/under
        site_class_over = ASCE.asceTable(vs100_multiplied)
        site_class_under = ASCE.asceTable(vs100_divided)
        st.write(f'Vs100 * 1.3 is = {vs100_multiplied}, Site Class {site_class_over}')
        st.write(f'Vs100 / 1.3 is = {vs100_divided}, Site Class {site_class_under}')

        # Make list of site class, site class over, site class under
        all_site_classes = [site_class_user, site_class_over, site_class_under]

        # Get the set of unique site classes.
        site_classes = functions.remove_duplicates(all_site_classes)

        # Construct the URLs
        urls = []
        for site_class in site_classes:
            url = functions.construct_url(
                st.session_state.lat,
                st.session_state.lon,
                st.session_state.risk_category,
                site_class,
                st.session_state.title
            )
            urls.append((url, site_class))

        # When URLs are ready, scrape data
        all_data = []
        for url, site_class in urls:
            periods, ordinates = scraper.scrape_data(url)
            if periods and ordinates:
                all_data.append({
                    'Site Class': site_class,
                    'Periods': periods,
                    'Ordinates': ordinates})

        # Make a human-reader friendly dataframe.
        my_df = make_dataframe.make_dataframe(all_data)
        
        # Plot the user's spectra.
        fig = go.Figure()
        fig, my_df = plotting.plot_spectra(fig, all_data, my_df, st.session_state.title)
    
        # MAIN AREA: display spectra plot.
        st.plotly_chart(fig)

        # MAIN AREA: display datarame of spectral ordinates.
        st.write('The dataframe contains the spectral ordinates of the plotted data')
        st.dataframe(my_df)

        # MAIN AREA: write out URLs and data source.
        url_list = [url for url, _ in urls]
        url_string = "\n".join(url_list)
        st.write('The data was gathered from the USGS website using these URLs:', url_string)

    # Get the slider value
    st.write('Select the average shear wave velocity in feet per second')
    vs100 = st.slider(
        'Select Vs100 (fps)',
        1,
        5000,
        1500,
        step=1,
        key='vs100_slider',
        on_change=do_all_the_processing
        )

# MAIN AREA: show a disclaimer.
st.write('This tool was developed to aid exploratory analysis of projects.' +
            'It is subject to revision. Though developed thoughtfully, ' +
            'neither the functionality of the software nor the reliablity of ' + 
            'the data are guaranteed. No warranty, expressed or implied, is ' +
            'made by the author. Users are urged to vet the data and ' +
            'information here against a unique source before relying on it ' +
            'for decision making.')