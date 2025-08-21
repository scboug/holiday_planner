import requests

import pandas as pd

import json



# Runs API to find best flights
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



#creates dataframe of best flights

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

