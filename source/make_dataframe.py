import pandas as pd

def make_dataframe(all_data):
    '''
    A function to make a human-friendly table of the scraped site class data.
    Input:
        fig: an array of scraped data containing site class, periods, and Sa.
    Output: 
        A dataframe with 
            header: unique Site Classes in the scraped data set
            col0: periods for spectra
            col1: the 'measured' spectrum ordinates
            col2: the 'composite' spectrum ordinates
    '''
    # Get periods from first site class since same for all.
    periods = all_data[0]['Periods'] if all_data else []
    my_df = pd.DataFrame({'Periods': periods})

    # Add columns for each site class.
    for data in all_data:
        site_class = data['Site Class']
        ordinates = data['Ordinates']
        my_df[site_class] = ordinates
        
    return my_df