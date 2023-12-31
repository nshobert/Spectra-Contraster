# An app to plot the ASCE 7-22 response spectra
# given the user selected location and site class(es).

# Import libraries
import streamlit as st
import hmac
import pandas as pd
import plotly.graph_objects as go
import scraper
import functions
import ASCE
import plotting
import make_dataframe

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.
# Define a function to show plot, dataframe, and URLs
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

# Title for app.
st.header('ASCE 7-22 Response Spectra Plotter')

# Check if user has submitted initial input.
if st.session_state.get('user_input'):
    # Display the slider and update it's value in session state.
    vs100_slider = st.slider(
        'Select Vs100 (fps)',
        1, 5000,
        value=st.session_state.get('vs100_slider', 1500), # Use default 1500 if none
        step=1,
        key='vs100_slider'
    )

    if vs100_slider != st.session_state.get('vs100_slider', 1500):
        st.session_state['vs100_slider'] = vs100_slider
        
    # when the slider is changed,
    do_all_the_processing()

# Set a session state.
if 'lat' not in st.session_state:
    st.session_state['lat'] = 47.5678
if 'lon' not in st.session_state:
    st.session_state['lon'] = -122.0123
if 'risk_category' not in st.session_state:
    st.session_state['risk_category'] = 'III'
if 'title' not in st.session_state:
    st.session_state['title'] = 'MyProjectCity'
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = None

# Get initial user input
if st.session_state['user_input'] is None:
    # Add a welcome message and instructions
    st.write('Please submit required data in sidebar to the left.')

# User input location, confirm on map
with st.sidebar:
    st.header('Start by Entering Options Here')

    # SIDEBAR: get latitude and longitude if none, or show defaults.
    st.session_state['lat'] = st.text_input(
        'Enter latitude',
        value=st.session_state['lat']
    )
    st.session_state['lon'] = st.text_input(
        'Enter longitude',
        value=st.session_state['lon']
    )

    # SIDEBAR: submit button for lat, lon
    check_location = st.button('Check Location')

    if check_location:
        try:
            lat_float = float(st.session_state['lat'])
            lon_float = float(st.session_state['lon'])
            loc = pd.DataFrame({'lat': [lat_float], 'lon': [lon_float]})
            st.map(data=loc, zoom=8)
        except ValueError:
            st.error("Please enter valid latitude and longitude values.")

    # SIDEBAR: use a form to get user inputs
    st.header('After confirming location, select spectrum options')
    with st.form('user_inputs'):
        # SIDEBAR: input risk category, only 1.
        risk_categories = ['I', 'II', 'III', 'IV']
        st.session_state['risk_category'] = st.radio(
            'Select risk category',
            risk_categories,
            index=risk_categories.index(st.session_state['risk_category'])
        )
        
        # SIDEBAR: name the location of the project.
        st.session_state['title'] = st.text_input(
            'Project Location',
            value= st.session_state['title']
        )

        # SIDEBAR: submit button
        user_input = st.form_submit_button("SUBMIT")

        # Remember the user inputs that were submitted
        if user_input:
            st.session_state['user_input'] = True

# MAIN AREA: show a disclaimer.
st.write('This tool was developed to aid exploratory analysis of projects.' +
            'It is subject to revision. Though developed thoughtfully, ' +
            'neither the functionality of the software nor the reliablity of ' + 
            'the data are guaranteed. No warranty, expressed or implied, is ' +
            'made by the author. Users are urged to vet the data and ' +
            'information here against a unique source before relying on it ' +
            'for decision making.')