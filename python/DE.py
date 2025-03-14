import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class BrandInfo:
    def __init__(self, brand_name, brand_link):
        self.brand_name = brand_name
        self.brand_link = brand_link

    def __str__(self):
        return f"Brand Name: {self.brand_name}, Link: {self.brand_link}"

def fetch_brands(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  # Global wait for elements
    
    brand_list = []
    
    try:
        driver.get(url)
        time.sleep(5)  # Allow page to load fully
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        brand_section = soup.find("div", class_="brand-list")
        
        if brand_section:
            for entry in brand_section.find_all("a", class_="brand-item"):
                brand_name = entry.text.strip()
                brand_link = entry["href"] if entry.has_attr("href") else "N/A"
                brand_list.append(BrandInfo(brand_name, brand_link))
        else:
            print("Error: 'brand-list' class not found on the page.")
            print("Page source snippet:", driver.page_source[:1000])
    
    finally:
        driver.quit()
    
    return brand_list

if __name__ == "__main__":
    url = "https://multicraft.ca/en/brand/subbrands?code=artscrafts"
    brand_data = fetch_brands(url)
    
    if brand_data:
        for i, brand in enumerate(brand_data, 1):
            print(f"{i} - {brand}")
    else:
        print("No brand data found or website structure has changed.")
