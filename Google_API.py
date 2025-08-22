import googlemaps
import folium

gmaps = googlemaps.Client(key="AIzaSyDlV8XL107fRm2TFinDMrk7KIvQTe9sWxY")

def locations(city, country):
    """
    Get latitude and longitude of city and country using Google Maps API.
    Returns a tuple float (latitude, longitude).
    """
    location = gmaps.geocode(city + ", " + country)
    lat = location[0]['geometry']['location']['lat']
    lng = location[0]['geometry']['location']['lng']
    return lat, lng

def get_places(location, type):
    """
    Retrieves places from Google Maps API.
    location = latitude, longitude
    type = type of place to retrieve e.g. bar, restaurant, nightclub or supermarket.
    Returns a JSON like dictionary from Google Maps API containing information about local places.
    """
    places = gmaps.places_nearby(
        location=(location[0], location[1]),
        radius=20000,
        type=type
    )
    return places

def places_map(location, places):
    """
    Create an interactive folium map of local places.
    location = latitude, longitude
    places = type of place to retrieve e.g. bar, restaurant, nightclub or supermarket.
    returns a folium map
    """
    map = folium.Map(location=[location[0], location[1]], zoom_start=11)
    for place in places['results']:
        folium.Marker(
            [place['geometry']['location']['lat'], place['geometry']['location']['lng']],
            popup=place['name']
        ).add_to(map)
    return map






