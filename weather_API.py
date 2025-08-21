#Weather API

import pip
pip.main(['install', ' openmeteo-requests'])

import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry




# Use API
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 22.6486,
	"longitude": 88.3411,
	"daily": ["temperature_2m_max", "wind_speed_10m_mean"],
	"current": ["cloud_cover", "wind_speed_10m", "relative_humidity_2m"],
	"timezone": "GMT",
}
responses = openmeteo.weather_api(url, params=params)


# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")





# Current Statistics about the weather at Location
current = response.Current()
current_cloud_cover = current.Variables(0).Value()
current_wind_speed_10m = current.Variables(1).Value()
current_relative_humidity_2m = current.Variables(2).Value()


print(f"Current cloud cover: {current_cloud_cover}%")
print(f"Current wind speed:{round(current_wind_speed_10m,2)}km/h")
print(f"Current humidity: {current_relative_humidity_2m}%")

#Forecast statistics for next 7 days
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_wind_speed_10m_mean = daily.Variables(1).ValuesAsNumpy()

daily_data = {"Date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
).tz_localize(None)}

daily_data["Maximum temperature°C"] = daily_temperature_2m_max
daily_data["Wind speed"] = daily_wind_speed_10m_mean

daily_dataframe = pd.DataFrame(data = daily_data)
print("\Forecast data\n", daily_dataframe)


