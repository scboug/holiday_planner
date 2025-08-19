import googlemaps
import folium

gmaps = googlemaps.Client(key="AIzaSyDlV8XL107fRm2TFinDMrk7KIvQTe9sWxY")

def locations(city, country):
    location = gmaps.geocode(city + country)
    lat = location[0]['geometry']['location']['lat']
    lng = location[0]['geometry']['location']['lng']
    return lat, lng

def places(location, type):
    places = gmaps.places_nearby(
        location=(location[0], location[1]),
        radius=20000,
        type=type
    )
    return places

def places_map(location, places):
    map = folium.Map(location=[location[0], location[1]], zoom_start=11)
    for place in places['results']:
        folium.Marker(
            [place['geometry']['location']['lat'], place['geometry']['location']['lng']],
            popup=place['name']
        ).add_to(map)
    return map





