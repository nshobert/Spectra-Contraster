import scraper

# Construct the URL to be passed to scraper.
def construct_url(latitude, longitude, riskCategory, siteClass, title):
    base_url = "https://earthquake.usgs.gov/ws/designmaps/asce7-22.json?"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'riskCategory': riskCategory,
        'siteClass': siteClass,
        'title': title
    }
    return base_url + '&'.join(f"{key}={value}" for key, value in params.items())

# Function to remove duplicate site classes from a list of all site classes.
def remove_duplicates(lst):
    seen = set()
    seen_add = seen.add
    return [x for x in lst if not (x in seen or seen_add(x))]

# Function to test construct_url function  
def main():
    # Example inputs - replace with user inputs from Streamlit widgets
    latitude = 34
    longitude = -118
    riskCategory = "III"
    siteClass = "C"
    title = "Example"

    url = construct_url(latitude, longitude, riskCategory, siteClass, title)
    print("the constructed URL is: ", url)
    periods, ordinates = scraper.scrape_data(url)

    if periods and ordinates:
        print("Periods:", periods)
        print("Ordinates:", ordinates)
    else:
        print("Failed to retrieve data.")

if __name__ == "__main__":
    main()