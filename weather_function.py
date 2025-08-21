import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import googlemaps
import folium
import requests
import gradio as gr


gmaps = googlemaps.Client(key="AIzaSyDlV8XL107fRm2TFinDMrk7KIvQTe9sWxY")
#data about airports
data_airport = {
    "Country": ["Bali", "Singapore", "Thailand", "Vietnam", "Philippines"],
    "Airport": ["DPS", "SIN", "BKK", "SGN", "MNL"],
    "Airport City":["Denpasar","Singapore","Bangkok","Ho Chi Minh City","Manila"
]
}
airport = pd.DataFrame(data_airport)

def locations(city, country):
    location = gmaps.geocode(city + country)
    lat = location[0]['geometry']['location']['lat']
    lng = location[0]['geometry']['location']['lng']
    return lat, lng

def get_current_weather(country):
    #find coordinates
    city = airport.loc[airport["Country"] == country, "Airport City"].values[0]
    latlong=locations(city,country)

    #Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latlong[0],
        "longitude": latlong[1],
        "current": ["cloud_cover", "wind_speed_10m", "relative_humidity_2m"],
        "timezone": "GMT",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location
    response = responses[0]

    # Current stats
    current = response.Current()
    current_cloud_cover = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    current_relative_humidity_2m = current.Variables(2).Value()

    # Build DataFrame properly
    weath_data = {
        "Cloud Cover (%)": [current_cloud_cover],
        "Wind Speed (km/h)": [round(current_wind_speed_10m)],
        "Humidity (%)": [current_relative_humidity_2m]
      }
    today_data = pd.DataFrame(weath_data)

    return today_data

def get_future_weather(country):
    # Find coordinates
    city = airport.loc[airport["Country"] == country, "Airport City"].values[0]
    latlong = locations(city, country)

    # Setup Open-Meteo client
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # API request
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latlong[0],
        "longitude": latlong[1],
        "daily": ["temperature_2m_max", "wind_speed_10m_mean"],
        "current": ["cloud_cover", "wind_speed_10m", "relative_humidity_2m"],
        "timezone": "GMT",
    }
    responses = openmeteo.weather_api(url, params=params)
    # Process first location
    response = responses[0]
    # Forecast stats 7 days
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_wind_speed_10m_mean = daily.Variables(1).ValuesAsNumpy()

    daily_data = {"Date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    ).tz_localize(None).date}

    daily_data["Maximum temperature°C"] = daily_temperature_2m_max
    daily_data["Wind speed(km/h)"] = daily_wind_speed_10m_mean

    daily_dataframe = pd.DataFrame(data=daily_data)
    daily_dataframe["Maximum temperature°C"]=daily_dataframe["Maximum temperature°C"].round(0).astype(int)
    daily_dataframe["Wind speed(km/h)"]=daily_dataframe["Wind speed(km/h)"].round(0).astype(int)

    return daily_dataframe

