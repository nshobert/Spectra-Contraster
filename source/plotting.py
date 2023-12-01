import plotly.graph_objects as go

# Define the plotting function and style
'''
Input:
    fig: an initialized figure, e.g. fig1 = go.Figure()
    df: a dataframe with column 0 called 'Date' and other columns the series of interest.
Output: 
    A plot of the 'measured' and 'estimated' composite spectra

'''
def plot_spectra(fig, all_data, my_df, title):
    # Add the spectrum for the user's 'measured' site class.
    fig.add_trace(
        go.Scatter(
            x=all_data[0]['Periods'],
            y=all_data[0]['Ordinates'],
            name=f"Site Class {all_data[0]['Site Class']} if Vs100 measured"
        )
    )

    # Make the composite spectrum
    # Use the periods from first site class since all the same.
    periods = all_data[0]['Periods'] if all_data else []

    # Get max spectral acceleration at each period.
    max_ords = [max(data['Ordinates'][i] for data in all_data) for i in range(len(periods))]
    
    # Add the composite spectrum to the plot.
    fig.add_trace(
        go.Scatter(
            x=periods,
            y=max_ords,
            name='Composite Spectrum if Vs100 estimated',
            line=dict(dash='dash')
        )
    )

    # Add the composite spectrum to the dataframe.
    my_df['Composite'] = max_ords


    # Set x axis to log and add labels.
    fig.update_xaxes(
            type='log',
            title='Period (s)'
        )
    
    fig.update_yaxes(
            title='Spectral Acceleration (g)'
        )
    
    fig.update_layout(
        title=f'Multiperiod Response Spectra for {title}',
        hovermode='x unified'
    )
 
    return(fig, my_df)