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

gmaps = googlemaps.Client(key="AIzaSyDlV8XL107fRm2TFinDMrk7KIvQTe9sWxY")

def holiday_selector(choice):
    city, country = choice.split(", ")
    lat, lng = locations(city, country)
    return f"{city}, {country}\nLatitude: {lat}\nLongitude: {lng}", (lat, lng)

def create_places_map(location, places_result, title=""):
    m = folium.Map(location=[location[0], location[1]], zoom_start=11)
    for place in places_result['results']:
        folium.Marker(
            [place['geometry']['location']['lat'], place['geometry']['location']['lng']],
            popup=place['name']
        ).add_to(m)
    html_map = f"<h3>{title}</h3>" + m._repr_html_()
    return html_map

def holiday_with_all(choice):
    city_country, location = holiday_selector(choice)
    all_maps = []
    for place_type in ["bar", "restaurant", "night_club", "supermarket"]:
        nearby_places = get_places(location, place_type)
        map_html = create_places_map(location, nearby_places, title=place_type.capitalize())
        all_maps.append(map_html)

    url_hotel = url(city_country)
    driver = webdriver.Chrome()
    driver.get(url_hotel)
    time.sleep(0.5)
    hotels = hotel_scrap(driver)
    driver.quit()
    hotels_df = hotels_data(hotels)

    return [city_country] + all_maps + [hotels_df]

destinations = ["Denpasar, Indonesia", "Singapore, Singapore", "Bangkok, Thailand", "Ho chi min, Vietnam", "Manila, Phillippines"]
data_airport = {
    "Country": ["Bali", "Singapore", "Thailand", "Vietnam", "Philippines"],
    "Airport": ["DPS", "SIN", "BKK", "SGN", "MNL"]
}
airport = pd.DataFrame(data_airport)

with gr.Blocks(css=""".gradio-container {background-color: #e6f7ff;}""") as demo:
    gr.Markdown("# Welcome to your Holiday Planner")
    gr.Markdown(
        """
        Plan your next adventure with ease!  
        Choose a destination and instantly explore:  

        - Top **bars, restaurants, clubs, and supermarkets** nearby  
        - The best **hotels from Booking.com**  
        - Flight options to get you there  

        Your perfect holiday starts here — just pick a city and let us do the rest!
        """)

    gr.Markdown("# Select a Destination to Check Flight Prices")
    drop1 = gr.Dropdown(choices=airport["Country"].tolist(), label="Select country", value="Bali", interactive=True)
    generate_button = gr.Button("See best flights")
    output_df = gr.DataFrame()
    generate_button.click(fn=get_air, inputs=drop1, outputs=output_df)

    gr.Markdown("# Select a Destination to see the Current Weather")
    drop_weather_1 = gr.Dropdown(choices=airport["Country"].tolist(), label="Select country", value="Bali", interactive=True)
    output_current_weather_df = gr.DataFrame()
    drop_weather_1.change(
        fn=get_current_weather,
        inputs=drop_weather_1,
        outputs=[output_current_weather_df]
    )

    gr.Markdown("# Select a Destination to see the 7 Day Weather Forecast")
    drop_weather_2 = gr.Dropdown(choices=airport["Country"].tolist(), label="Select country", value="Bali", interactive=True)
    output_future_weather_df = gr.DataFrame()
    drop_weather_2.change(
        fn=get_future_weather,
        inputs=drop_weather_2,
        outputs=[output_future_weather_df]
    )

    gr.Markdown("# Select a Destination to Check Bars, Restaurants, Clubs, Supermarkets and Hotels")
    dropdown_city = gr.Dropdown(
        choices=destinations,
        label="Select a Destination",
        value="Destination"
    )
    output_info = gr.Markdown()

    with gr.Row():
        output_bar = gr.HTML()
        output_restaurant = gr.HTML()
    with gr.Row():
        output_club = gr.HTML()
        output_supermarket = gr.HTML()

    gr.Markdown("## Top Hotels on Booking.com")
    output_hotels = gr.Dataframe()

    dropdown_city.change(
        fn=holiday_with_all,
        inputs=dropdown_city,
        outputs=[output_info, output_bar, output_restaurant, output_club, output_supermarket, output_hotels]
    )

demo.launch()

