import requests  
from bs4 import BeautifulSoup  
import json  
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service as ChromeService  
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.common.exceptions import NoSuchElementException, TimeoutException  

def fetch_all_property_details(url):  
    property_listing = {  
        "bed": "NA",  
        "bath": "NA",  
        "sqft": "NA",
        "description": "",  
        "car_parking": "NA",  
        "type": "NA", 
        "fitness": "NA", 
        "swimming_pool": "NA",
        "floors": "NA",
        "total_floors": "NA",
        "furnishing": "NA",  
        "elevators": "NA",  
        "completion_year": "NA",  
        "security_staff": "NA",  
        "central_heating": "NA",  
        "centrally_air-conditioned": "NA",  
        "balcony_or_terrace": "NA"  
    }

    descriptions = []
    
    headers = {  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"  
    }  
    response = requests.get(url, headers=headers)  
    
    if response.status_code == 200:  
        soup = BeautifulSoup(response.content, 'html.parser')  
        
        try:  
            stats_div = soup.find('div', {'aria-label': 'Detail stats info'})  
            if stats_div:  
                if stat := stats_div.find('span', {'aria-label': 'Beds'}):  
                    property_listing["bed"] = stat.text.strip()  
                if stat := stats_div.find('span', {'aria-label': 'Baths'}):  
                    property_listing["bath"] = stat.text.strip()  
                if stat := stats_div.find('span', {'aria-label': 'Area'}):  
                    property_listing["sqft"] = stat.find('h4').text.strip() if stat.find('h4') else "NA"  
        except Exception:  
            pass  

        scripts = soup.find_all('script', {'type': 'application/ld+json'})  
        for script in scripts:  
            try:  
                data = json.loads(script.string)  
                # Check for the specific type and if a description is available   
                if data.get('@type') == "ItemPage" and 'mainEntity' in data and 'description' in data['mainEntity']:  
                    descriptions.append(data['mainEntity']['description'])  
            except json.JSONDecodeError:  
                continue  
            except KeyError:  
                continue  

        # print(descriptions)

        # Initialize WebDriver  
        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)  
        try:  
            driver.get(url)  
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))  

            try:  
                property_listing["type"] = driver.find_element(By.CSS_SELECTOR, "span[aria-label='Type']").text.strip()  
            except NoSuchElementException:  
                pass  
            try:  
                property_listing["furnishing"] = driver.find_element(By.CSS_SELECTOR, "span[aria-label='Furnishing']").text.strip()  
            except NoSuchElementException:  
                pass  
            try:  
                property_listing["elevators"] = driver.find_element(By.CSS_SELECTOR, "span[aria-label='Elevators']").text.strip()  
            except NoSuchElementException:  
                pass  
            try:  
                property_listing["completion_year"] = driver.find_element(By.CSS_SELECTOR, "span[aria-label='Year of Completion']").text.strip()  
            except NoSuchElementException:  
                pass  
            try:  
                property_listing["car_parking"] = driver.find_element(By.CSS_SELECTOR, "span[aria-label='Total Parking Spaces']").text.strip()
            except NoSuchElementException:  
                pass  
            try:  
                property_listing["total_floors"] = driver.find_element(By.CSS_SELECTOR, "span[aria-label='Total Floors']").text.strip()  
            except NoSuchElementException:  
                pass  

            amenities = [  
                "Security Staff", "Central Heating", "Centrally Air-Conditioned", "Balcony or Terrace", "Swimming Pool"  
            ]  
            for amenity in amenities:  
                try:  
                    elements = driver.find_elements(By.XPATH, f"//span[contains(text(), '{amenity}')]")  
                    property_listing[amenity.replace(" ", "_").lower()] = "Yes" if elements else "NA"  
                except NoSuchElementException:  
                    property_listing[amenity.replace(" ", "_").lower()] = "NA"

            try:  
                floorplan_elements = driver.find_elements(By.CSS_SELECTOR, 'div[aria-label="Floorplans tabs"] img')  
                if floorplan_elements:  
                    property_listing["floors"] = floorplan_elements[0].get_attribute('title') or "Title missing"  
                else:  
                    pass
            except NoSuchElementException:  
                print("No floorplans section found.")
            
            # Update some fields from the descriptions
            if property_listing['car_parking'] == "NA":
                if descriptions[0].find("parking"):
                    property_listing['car_parking'] = "Yes"
            if property_listing['swimming_pool'] == "NA":
                if descriptions[0].find("swimming"):
                    property_listing['swimming_pool'] = "Yes"
            if property_listing['fitness'] == "NA":
                if descriptions[0].find("gym"):
                    property_listing['fitness'] = "Yes"
            if property_listing['elevators'] == "NA":
                if descriptions[0].find("elevator"):
                    property_listing['elevators'] = "Yes"
            property_listing['description'] = descriptions[0]
        except TimeoutException:
            print("Timed out waiting for page to load")
        except Exception as e:
            print(f"An error occurred while loading the page: {e}")
        finally:  
            driver.quit()  
    
    else:  
        print("Failed to retrieve the webpage. Status code:", response.status_code)  

    return property_listing  


# # Test the function by providing the URL of a property listing  
# url = "https://www.bayut.com/property/details-10119730.html"  
# property_details = fetch_all_property_details(url)  
# print(property_details)
