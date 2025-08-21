#at time of posting 57 searches left

import requests
import gradio as gr
import json
import pandas as pd

def get_flights(arrival_id):
'''
Function that runs the API to see best flights from london heathrow to a countries corresponding airport
'''
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "google_flights",
        "flight_type": "round_trip",
        "departure_id": "LHR",
        "arrival_id": arrival_id,
        "outbound_date": "2025-08-26",
        "return_date": "2025-09-02",
        "api_key": "p4YtMCnbkUrJTG2xAzRwkqsb",
        "currency": "GBP"
    }

    response = requests.get(url, params=params)
    data = response.json()

    records = []
    for option in data.get("best_flights", []):
        for f in option.get("flights", []):
            records.append({
                "Departure Date": f["departure_airport"].get("date", ""),
                "Departure Time": f["departure_airport"].get("time", ""),
                "Airline": f.get("airline", ""),
                "Duration (min)": f.get("duration", ""),
                "Price (£)": option.get("price", ""),
            })

    return pd.DataFrame(records)


# Countries and corresponding airport codes of there largest airports
data_airport = {
    "Country": ["Bali", "Singapore", "Thailand", "Vietnam", "Philippines"],
    "Airport": ["DPS", "SIN", "BKK", "SGN", "MNL"]
}
airport = pd.DataFrame(data_airport)


def get_air(location):
   '''
Function finds the airport code for the selected country and uses this to run an API which finds the best flights 
'''
    # Find the airport code for selected country
    apt = airport.loc[airport["Country"] == location, "Airport"].values[0]
    return get_flights(apt)


with gr.Blocks() as demo:
    drop1 = gr.Dropdown(choices=airport["Country"].tolist(), label="Select country", value="Bali", interactive=True)
    generate_button = gr.Button("See best flights")
    output_df = gr.DataFrame()
    generate_button.click(fn=get_air, inputs=drop1, outputs=output_df)

demo.launch()

