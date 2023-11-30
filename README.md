# ASCE 7 Response Spectra Comparison Tool

## Overview
This tool is designed for users to compare the ASCE 7-22 response spectra for a given average shear wave velocity, Vs100, that was measured or estimated by correlation. Users can input specific geographic coordinates (latitude and longitude) and select various other inputs and the tool will retrieve the spectral ordinates from the USGS. The tool provides interactive visualizations, a simple map for location verification, and the ability to download the spectra of interest.
## Features
- **Data Scraping**: Automatically scrapes spectral ordinate data from the [USGS Seismic Design Web Services](https://earthquake.usgs.gov/ws/designmaps/) website.
- **User Input**: Allows users to input latitude and longitude and risk category, and other inputs.
- **Interactive Plots**: Visualize the spectral data for easy comparison.
- **Map Integration**: Provides a geographic map to validate the selected location.
- **Maximum Envelope Spectrum**: Generates a spectrum composed of the Vs100, 1.3*Vs100, and Vs100/1.3 as required for estimated shear wave velocity profiles. 
- **Data Download**: Enables users to download the spectral ordinates of the spectra of interest.

## Usage
Access the app with the URL below. Directions for its use are displayed there.

**To use the app**: [Spectra Comparison Tool](link.com).

## Modify the Code

### Prerequisites
- Python 3.11
- Pipenv for dependency management

### Setup
1. Clone the repository:
   ```
   git clone (url)
   ```
2. Navigate to your project directory:
   ```
   cd asce7_spectra_app
   ```
3. Install dependencies using Pipenv:
   ```
   pipenv install
   ```
4. Activate the Pipenv shell:
   ```
   pipenv shell
   ```
5. Start the Streamlit app:
   ```
   streamlit run source/main.py
   ```
6. To quit:
   ```
   ctrl+c
   ```


### Example/ Test run
To confirm that your setup worked, run the app and submit the default settings.

1. Open a new browser window. 
2. At the command line, enter `streamlit run source\main.py`. A browser window will open with the app.
3. Open the sidebar with the little arrow at upper left.
4. Leave the defaults. Select `Check Location` to confirm that the map updates to a point near Issaquah, WA.
5. Select `Submit` to add a plot with 4 spectra, a dataframe, and URLs to the main area.
6. You're now free to change the inputs in the sidebar for your project!


### License
This will be a private repo, right? Need to figure out how to deploy on local server.

## Disclaimer
### From the USGS, the source of the data:
This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the software.

### From the author:
This tool was developed to aid exploratory analysis of projects. It is subject to revision. Though developed thoughtfully, neither the functionality of the software nor the reliablity of the data are guaranteed. No warranty, expressed or implied, is made by the author. Users are urged to vet the data and information here against a unique source before relying on it for decision making.