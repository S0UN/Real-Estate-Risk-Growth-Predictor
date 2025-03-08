from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_zillow_price(address):
    """Searches Zillow for an address and extracts the property price."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    service = Service("chromedriver.exe")  # Update path as needed
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("Opening Zillow...")
        driver.get("https://www.zillow.com/")
        
        # Wait for and locate the search box using the placeholder text
        print(f"Searching for: {address}")
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter an address, neighborhood, city, or ZIP code']"))
        )
        search_box.send_keys(address)
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results to load
        time.sleep(3)
            
        # Extract price
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-testid='price']"))
            )
            price = price_element.text
        except:
            price = "Price not found"

        current_url = driver.current_url
        return {"Address": address, "Price": price, "Link": current_url}

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {"Address": address, "Price": "Error", "Link": ""}
    finally:
        driver.quit()

if __name__ == "__main__":
    address_input = input("Enter an address: ")
    result = get_zillow_price(address_input)
    print(f"\n🏠 Address: {result['Address']}\n💰 Price: {result['Price']}\n🔗 Link: {result['Link']}")