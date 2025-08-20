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

URL = 'https://www.booking.com/searchresults.en-gb.html?ss=Bali&ssne=Bali&ssne_untouched=Bali&efdco=1&label=gen173nr-10CAsoaEIea2FudmF6LXZpbGxhZ2UtcmVzb3J0LXNlbWlueWFrSAlYBGhQiAEBmAEzuAEHyAEM2AED6AEB-AEBiAIBqAIBuAK9w5HFBsACAdICJDNiZmQzYjdmLTkxM2QtNGQwMS1iYjRjLWQzNDYyMTI3NDExZNgCAeACAQ&sid=f3d7c8a7a671b3d104acc7004462101b&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=835&dest_type=region&checkin=2025-09-01&checkout=2025-09-02&group_adults=1&no_rooms=1&group_children=0'
driver = webdriver.Chrome()
driver.get(URL)
time.sleep(5)

def hotel_scrap(driver):
    hotels = []
    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")
    for card in cards[:30]:
        try:
            name = card.find_element(By.CSS_SELECTOR, "div[data-testid='title']").text
        except:
            name = "N/A"
        try:
            price = card.find_element(By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price']").text
        except:
            price = "N/A"
        try:
            rating = card.find_element(By.CSS_SELECTOR, "div[data-testid='review-score']").text
        except:
            rating = "N/A"
        hotels.append((name, price, rating))
    return hotels

def hotels_data(hotels):
    h = pd.DataFrame(hotels)
    h[2] = h[2].str.extract(r"(\d+(?:\.\d+)?)")
    h = h.rename(columns={
        0: 'Hotel Name',
        1: 'Price per 1 person per night',
        2: 'Booking.com rating'
    })
    return h

hotels = hotel_scrap(driver)
hotels_df = hotels_data(hotels)
hotels_df.to_csv("hotels_data.csv", index = False, header = True)
driver.close()
driver.quit()

