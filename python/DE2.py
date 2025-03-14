import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class ProductInfo:
    def __init__(self, product_name, product_code, availability):
        self.product_name = product_name
        self.product_code = product_code
        self.availability = availability

    def __str__(self):
        return f"Product Name: {self.product_name}, Product Code: {self.product_code}, Availability: {self.availability}"

def fetch_products(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  # Global wait for elements
    
    product_list = []
    
    try:
        driver.get(url)
        time.sleep(5)  # Allow page to load fully
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        product_sections = soup.find_all("li", class_="skuSummary")
        
        if product_sections:
            for entry in product_sections:
                product_name = entry.find("div", class_="skuSummary-desc").text.strip() if entry.find("div", class_="skuSummary-desc") else "N/A"
                product_code = entry.find("p", class_="summary-id").text.strip() if entry.find("p", class_="summary-id") else "N/A"
                availability = entry.find("div", class_="row").find_all("p")[1].text.strip() if entry.find("div", class_="row") else "N/A"
                
                product_list.append(ProductInfo(product_name, product_code, availability))
        else:
            print("Error: No products found on the page.")
            print("Page source snippet:", driver.page_source[:1000])
    
    finally:
        driver.quit()
    
    return product_list

if __name__ == "__main__":
    url = "https://multicraft.ca/en/brand/subbrands?code=artscrafts"
    product_data = fetch_products(url)
    
    if product_data:
        for i, product in enumerate(product_data, 1):
            print(f"{i} - {product}")
    else:
        print("No product data found or website structure has changed.")
