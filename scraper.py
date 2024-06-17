import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def fetch_data_with_selenium(url):
    """
    Fetches HTML content from the given URL using Selenium to render JavaScript.
    """
    options = webdriver.ChromeOptions()
    options.headless = True  # Run headless to avoid opening a browser window
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    try:
        # Increase wait times and wait for key elements to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".price, .phone"))
        )
        
        # Scroll to bottom to load more elements
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Allow time for content to load after scrolling
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        html = driver.page_source
        driver.quit()
    return BeautifulSoup(html, 'html.parser')

def parse_apartments_data(html):
    """
    Parses HTML content to extract apartments data including price and location.
    """
    apartments = []
    for apartment in html.select('.placard'):
        title = apartment.select_one('.placardTitle, .title').get_text(strip=True) if apartment.select_one('.placardTitle, .title') else "No Title"
        link = apartment.select_one('a')['href'].strip() if apartment.select_one('a') else "No Link"
        price = apartment.select_one('.price, .rent').get_text(strip=True) if apartment.select_one('.price, .rent') else "No Price"
        location = apartment.select_one('.property-address, .location').get_text(strip=True) if apartment.select_one('.property-address, .location') else "No Location"
        contact = apartment.select_one('.phone, .contact').get_text(strip=True) if apartment.select_one('.phone, .contact') else "No Contact"
        
        apartments.append({
            "title": title,
            "link": link,
            "price": price,
            "location": location,
            "contact": contact
        })
    return apartments

def save_data(data, filename, folder='data'):
    """
    Saves data to a JSON file in the specified folder.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, filename)
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)

def fetch_all_pages(base_url, start_page, end_page):
    """
    Fetches data from all pages in the specified range.
    """
    for page in range(start_page, end_page + 1):
        url = f"{base_url}?page={page}"
        print(f"Fetching data from {url}")
        html = fetch_data_with_selenium(url)
        if html:
            page_data = parse_apartments_data(html)
            filename = f"houston_apartments_page_{page}.json"
            save_data(page_data, filename)
            print(f"Data for page {page} saved successfully.")
        else:
            print(f"Failed to fetch data from page {page}")

def main():
    base_url = 'https://www.apartments.com/houston-tx/'
    fetch_all_pages(base_url, 1, 5)  # Fetch the first 5 pages

if __name__ == "__main__":
    main()
