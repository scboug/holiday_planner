import gradio as gr
import googlemaps
import folium
from Google_API import locations, get_places, places_map
#from Web_Scraping import hotel_scrap, hotels_data

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

def holiday_with_all_maps(choice):
    city_country, location = holiday_selector(choice)
    all_maps = []
    for place_type in ["bar", "restaurant", "night_club", "supermarket"]:
        nearby_places = get_places(location, place_type)
        map_html = create_places_map(location, nearby_places, title=place_type.capitalize())
        all_maps.append(map_html)
    return [city_country] + all_maps

destinations = ["Denpasar, Indonesia"]

with gr.Blocks() as demo:
    gr.Markdown("## Holiday Planner")
    gr.Markdown("Choose a destination to see coordinates and maps of nearby places:")

    dropdown_city = gr.Dropdown(
        choices=destinations,
        label="Select Destination",
        value="Cancun, Mexico"
    )

    output_info = gr.Markdown()
    output_bar = gr.HTML()
    output_restaurant = gr.HTML()
    output_club = gr.HTML()
    output_supermarket = gr.HTML()

    dropdown_city.change(
        fn=holiday_with_all_maps,
        inputs=dropdown_city,
        outputs=[output_info, output_bar, output_restaurant, output_club, output_supermarket]
    )

demo.launch()

