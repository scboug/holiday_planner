import requests

import pandas as pd

import json



#bali best flights leaving 26/08/26
#from heathrow to bali airport
#note that limited number of requests for this api at time of writing only 67 request left
url = "https://www.searchapi.io/api/v1/search"
params = {
  "engine": "google_flights",
  "flight_type": "round_trip",
  "departure_id": "LHR",
  "arrival_id": "DPS",
  "outbound_date": "2025-08-26",
  "return_date": "2025-09-02",
  "api_key": "p4YtMCnbkUrJTG2xAzRwkqsb",
  "currency": "GBP"
}

response = requests.get(url, params=params)


df = json.loads(response.text)


records = []
for option in df["best_flights"]:
    for f in option["flights"]:
        records.append({

            "Departure Date": f["departure_airport"]["date"],
            "Departure Time": f["departure_airport"]["time"],


            "Airline": f["airline"],

            "Duration in minutes": f["duration"],

            "Price (£)": option["price"],

        })

df = pd.DataFrame(records)
print(df)