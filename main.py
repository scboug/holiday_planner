import gradio as gr
import googlemaps
import folium
from selenium import webdriver
import time
import pandas as pd
from Google_API import locations, get_places, places_map
from Web_Scraping import hotel_scrap, hotels_data, url
from Flights_function_and_output import get_flights, get_air
from weather_function import get_future_weather, get_current_weather

gmaps = googlemaps.Client(key="AIzaSyDlV8XL107fRm2TFinDMrk7KIvQTe9sWxY") #Google API key.

def holiday_selector(choice):
    """
    Parses a location string (e.g. Bangkok, Thailand) and returns its coordinates.
    """
    city, country = choice.split(", ")
    lat, lng = locations(city, country)
    return f"{city}, {country}\nLatitude: {lat}\nLongitude: {lng}", (lat, lng)

def create_places_map(location, places_result, title=""):
    """
    Creates an interactive map with markers for given places. Returns the map in HTML format.
    """
    m = folium.Map(location=[location[0], location[1]], zoom_start=11)
    for place in places_result['results']:
        folium.Marker(
            [place['geometry']['location']['lat'], place['geometry']['location']['lng']],
            popup=place['name']
        ).add_to(m)
    html_map = f"<h3>{title}</h3>" + m._repr_html_()
    return html_map

def holiday_with_all(choice):
    """
    Generates location information for the given city and country.
    Creates 4 interactive maps with markers for bars, restaurants, nightclubs and supermarkets.
    Web scrapes and creates a table of hotel information of the given city and country.
    """
    city_country, location = holiday_selector(choice) #returns city information in coordinates.
    all_maps = []
    for place_type in ["bar", "restaurant", "night_club", "supermarket"]:
        nearby_places = get_places(location, place_type) #fetches nearby places (bars and restaurants).
        map_html = create_places_map(location, nearby_places, title=place_type.capitalize()) #Creates an HTML map.
        all_maps.append(map_html)

    url_hotel = url(city_country) #Gets the correct URL for the correct location.
    driver = webdriver.Chrome()
    driver.get(url_hotel)
    time.sleep(0.5)
    hotels = hotel_scrap(driver) #Scrapes all the hotel listings.
    driver.quit()
    hotels_df = hotels_data(hotels) #Turns the scrape into a dataframe.

    return [city_country] + all_maps + [hotels_df]

destinations = ["Denpasar, Indonesia", "Singapore, Singapore", "Bangkok, Thailand",
                "Ho chi min, Vietnam", "Manila, Philippines"] #List used for drop down menu.

data_airport = {
    "Country": ["Bali", "Singapore", "Thailand", "Vietnam", "Philippines"],
    "Airport": ["DPS", "SIN", "BKK", "SGN", "MNL"]
}
airport = pd.DataFrame(data_airport) #Dataframe of countries associated to airports.

with gr.Blocks(css=""".gradio-container {background-color: #e6f7ff;}""") as demo: #Creates the website page.
    gr.Markdown("# Welcome to your Holiday Planner") # Title of the page.
    gr.Markdown(
        """
        Plan your next adventure with ease!  
        Choose a destination and instantly explore:  

        - Top **bars, restaurants, clubs, and supermarkets** nearby  
        - The best **hotels from Booking.com**  
        - Flight options to get you there  

        Your perfect holiday starts here — just pick a city and let us do the rest!
        """) #Introduction of the page.

    gr.Markdown("# Select a Destination to Check Flight Prices")
    drop1 = gr.Dropdown(choices=airport["Country"].tolist(),
                        label="Select country", value="Bali", interactive=True) #Drop down box.
    generate_button = gr.Button("See best flights") #Button below drop down box.
    output_df = gr.DataFrame() #Dataframe of airports.
    generate_button.click(fn=get_air, inputs=drop1, outputs=output_df) #When the button is clicked flights to the
    # chosen country are displayed in a dataframe.

    gr.Markdown("# Select a Destination to see the Current Weather")
    drop_weather_1 = gr.Dropdown(choices=airport["Country"].tolist(),
                                 label="Select country", value="Bali", interactive=True) #Drop down box of destinations.
    output_current_weather_df = gr.DataFrame() # Data of the current weather of the selected country.
    drop_weather_1.change(
        fn=get_current_weather,
        inputs=drop_weather_1,
        outputs=[output_current_weather_df]
    ) # The dataframe output automatically updates as the country is changed in the dropdown box.

    gr.Markdown("# Select a Destination to see the 7 Day Weather Forecast")
    drop_weather_2 = gr.Dropdown(choices=airport["Country"].tolist(),
                                 label="Select country", value="Bali", interactive=True) # Dropdown box
    output_future_weather_df = gr.DataFrame() # Data of the future weather of the selected country.
    drop_weather_2.change(
        fn=get_future_weather,
        inputs=drop_weather_2,
        outputs=[output_future_weather_df]
    ) # The dataframe output automatically updates as the country is changed in the dropdown box.

    gr.Markdown("# Select a Destination to Check Bars, Restaurants, Clubs, Supermarkets and Hotels")
    dropdown_city = gr.Dropdown(
        choices=destinations,
        label="Select a Destination",
        value="Destination"
    ) # Dropdown box
    output_info = gr.Markdown()

    with gr.Row(): # Puts the two maps vertically next to each other.
        output_bar = gr.HTML()
        output_restaurant = gr.HTML()
    with gr.Row(): # Puts the two maps vertically next to each other.
        output_club = gr.HTML()
        output_supermarket = gr.HTML()

    gr.Markdown("## Top Hotels on Booking.com")
    output_hotels = gr.Dataframe()

    dropdown_city.change(
        fn=holiday_with_all,
        inputs=dropdown_city,
        outputs=[output_info, output_bar, output_restaurant, output_club, output_supermarket, output_hotels]
    ) # When the dropdown is changed it updates maps and scrapes for hotels for the new given location.

demo.launch() #closes the webpage.

