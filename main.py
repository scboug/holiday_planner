import gradio as gr
import googlemaps
import folium
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from Google_API import locations, get_places, places_map
from Web_Scraping import hotel_scrap, hotels_data

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

    url_hotel = 'https://www.booking.com/searchresults.en-gb.html?ss=Bali&ssne=Bali&ssne_untouched=Bali&efdco=1&label=gen173nr-10CAsoaEIea2FudmF6LXZpbGxhZ2UtcmVzb3J0LXNlbWlueWFrSAlYBGhQiAEBmAEzuAEHyAEM2AED6AEB-AEBiAIBqAIBuAK9w5HFBsACAdICJDNiZmQzYjdmLTkxM2QtNGQwMS1iYjRjLWQzNDYyMTI3NDExZNgCAeACAQ&sid=f3d7c8a7a671b3d104acc7004462101b&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=835&dest_type=region&checkin=2025-09-01&checkout=2025-09-02&group_adults=1&no_rooms=1&group_children=0'
    driver = webdriver.Chrome()
    driver.get(url_hotel)
    time.sleep(5)
    hotels = hotel_scrap(driver)
    driver.quit()
    hotels_df = hotels_data(hotels)

    return [city_country] + all_maps + [hotels_df]

destinations = ["Denpasar, Indonesia"]

with gr.Blocks() as demo:
    gr.Markdown("# Holiday Planner")
    gr.Markdown("Choose a destination to see all the information you'll be looking for!")

    dropdown_city = gr.Dropdown(
        choices=destinations,
        label="Select Destination",
        value="Cancun, Mexico"
    )

    output_info = gr.Markdown()
    with gr.Row():
        output_bar = gr.HTML()
        output_restaurant = gr.HTML()
    with gr.Row():
        output_club = gr.HTML()
        output_supermarket = gr.HTML()

    output_hotels = gr.Dataframe(label="Top Hotels (Booking.com)")
    dropdown_city.change(
        fn=holiday_with_all,
        inputs=dropdown_city,
        outputs=[output_info, output_bar, output_restaurant, output_club, output_supermarket, output_hotels]
    )

demo.launch()

