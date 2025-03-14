import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime

class BusInfo:
    def __init__(self, bus_name, departure_time, arrival_time):
        self.bus_name = bus_name
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def __str__(self):
        return f"Bus Name: {self.bus_name}, Departure Time: {self.departure_time}, Arrival Time: {self.arrival_time}"

def validate_travel_date(travel_date):
    try:
        return datetime.strptime(travel_date, "%d-%b-%Y").strftime("%d-%b-%Y")
    except ValueError:
        return "Invalid"

def get_url(from_city_name, from_city_id, to_city_name, to_city_id, travel_date):
    return f"https://www.redbus.in/bus-tickets/{from_city_name}-to-{to_city_name}?fromCityName={from_city_name}&fromCityId={from_city_id}&srcCountry=IND&toCityName={to_city_name}&toCityId={to_city_id}&destCountry=IND&onward={travel_date}&opId=0&busType=Any"

def fetch_bus_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    bus_list = []
    
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "result-section")))

        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(20):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        result_section = soup.find("div", id="result-section")
        
        if result_section:
            bus_items = result_section.find("ul", class_="bus-items")
            if bus_items:
                for entry in bus_items.find_all("li", class_="row-sec"):
                    bus_name = entry.find("div", class_="travels").text.strip() if entry.find("div", class_="travels") else "N/A"
                    departure_time = entry.find("div", class_="dp-time").text.strip() if entry.find("div", class_="dp-time") else "N/A"
                    arrival_time = entry.find("div", class_="bp-time").text.strip() if entry.find("div", class_="bp-time") else "N/A"
                    
                    bus_list.append(BusInfo(bus_name, departure_time, arrival_time))
    finally:
        driver.quit()

    return bus_list

if __name__ == "__main__":
    from_city_name = input("Enter the from city name: ")
    from_city_id = input("Enter the from city ID: ")
    to_city_name = input("Enter the to city name: ")
    to_city_id = input("Enter the to city ID: ")
    travel_date = validate_travel_date(input("Enter the travel date (DD-MMM-YYYY): "))

    if travel_date == "Invalid":
        print("Invalid date format. Please enter in DD-MMM-YYYY format.")
    else:
        url = get_url(from_city_name, from_city_id, to_city_name, to_city_id, travel_date)
        bus_data = fetch_bus_data(url)

        if bus_data:
            i = 1
            for bus in bus_data:
                print(f"{i} - {bus}")
                i += 1
        else:
            print("No bus data found.")
