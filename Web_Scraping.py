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

def hotel_scrap(driver):
    """
    Scrapes hotel information including name, price and rating.
    Returns list of tuples each tuple contains one hotel information.
    """
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
    """
    Converts a list of scraped hotels to a dataframe.
    Returns a dataframe containing hotel information.
    """
    h = pd.DataFrame(hotels)
    h[2] = h[2].str.extract(r"(\d+(?:\.\d+)?)")
    h = h.rename(columns={
        0: 'Hotel Name',
        1: 'Price per 1 person per night',
        2: 'Booking.com rating'
    })
    return h

def url(location):
    """
    Selects the correct URL for the correct location.
    Returns the correct URL.
    """
    if "Singapore, Singapore" in location:
        return ("https://www.booking.com/searchresults.en-gb.html?ss=Singapore%2C+Singapore&efdco=1&label=en-gb-booking-"
                "desktop-hRhoqrdHw8G4B1ptg7ui8AS652796016378%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3A"
                "lp9045940%3Ali%3Adec%3Adm&aid=2311236&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=-73635&dest_type=cit"
                "y&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_p"
                "ageview_id=f9b947a7ba2c0fa0&ac_meta=GhBmOWI5NDdhN2JhMmMwZmEwIAAoATICZW46BHNpbmdAAEoAUAA%3D&checkin=2025-"
                "10-01&checkout=2025-10-02&group_adults=1&no_rooms=1&group_children=0")
    elif "Denpasar, Indonesia" in location:
        return ("https://www.booking.com/searchresults.en-gb.html?ss=Denpasar%2C+Bali%2C+Indonesia&ssne=Singapore&ssne_"
                "untouched=Singapore&efdco=1&label=en-gb-booking-desktop-hRhoqrdHw8G4B1ptg7ui8AS652796016378%3Apl%3Ata%3"
                "Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9045940%3Ali%3Adec%3Adm&aid=2311236&lang=en-gb&sb=1&"
                "src_elem=sb&src=searchresults&dest_id=-2676772&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode"
                "=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=483d47e904a6176e&ac_meta=GhA0OD"
                "NkNDdlOTA0YTYxNzZlIAAoATICZW46BWRlbnBhQABKAFAA&checkin=2025-10-01&checkout=2025-10-02&group_adults=1&"
                "no_rooms=1&group_children=0")
    elif "Bangkok, Thailand" in location:
        return ("https://www.booking.com/searchresults.en-gb.html?ss=Bangkok%2C+Bangkok+Province%2C+Thailand&ssne="
                "Denpasar&ssne_untouched=Denpasar&label=en-gb-booking-desktop-hRhoqrdHw8G4B1ptg7ui8AS652796016378%3Apl"
                "%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9045940%3Ali%3Adec%3Adm&aid=2311236&lang=en-"
                "gb&sb=1&src_elem=sb&src=searchresults&dest_id=-3414440&dest_type=city&ac_position=0&ac_click_type=b&ac_"
                "langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=52a9486a85330001&ac_meta"
                "=GhA1MmE5NDg2YTg1MzMwMDAxIAAoATICZW46B0Jhbmdrb2tAAEoAUAA%3D&checkin=2025-10-01&checkout=2025-10-02&group"
                "_adults=1&no_rooms=1&group_children=0")
    elif "Ho chi min, Vietnam" in location:
        return ("https://www.booking.com/searchresults.en-gb.html?ss=Ho+Chi+Minh+City%2C+Ho+Chi+Minh+Municipality%2C+"
                "Vietnam&ssne=Bangkok&ssne_untouched=Bangkok&label=en-gb-booking-desktop-hRhoqrdHw8G4B1ptg7ui8AS6527960"
                "16378%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp9045940%3Ali%3Adec%3Adm&aid=2311236"
                "&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-3730078&dest_type=city&ac_position=0&ac_click_"
                "type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=385d488c9816"
                "0134&ac_meta=GhAzODVkNDg4Yzk4MTYwMTM0IAAoATICZW46BmhvIGNoaUAASgBQAA%3D%3D&checkin=2025-10-01&checkout="
                "2025-10-02&group_adults=1&no_rooms=1&group_children=0")
    else:
        return ("https://www.booking.com/searchresults.en-gb.html?ss=Manila%2C+Metro+Manila%2C+Philippines&ssne=Ho+Chi+"
                "Minh+City&ssne_untouched=Ho+Chi+Minh+City&label=gen173nr-10CAEoggI46AdIM1gEaFCIAQGYATO4AQfIAQzYAQPoAQH4"
                "AQGIAgGoAgG4AoWUnMUGwAIB0gIkMzI0YzcxZmEtZGIzZi00MjBiLTljNTctNDBiZTYwMjlkMWU42AIB4AIB&sid=b175797941fc1"
                "c9cc2675c36c45c176c&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=-2437894&dest_type=city&a"
                "c_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_"
                "pageview_id=7c17544246ca0ab0&ac_meta=GhA3YzE3NTQ0MjQ2Y2EwYWIwIAAoATICZW46Bm1hbmlsYUAASgBQAA%3D%3D&"
                "checkin=2025-10-01&checkout=2025-10-02&group_adults=1&no_rooms=1&group_children=0")

