import requests  
from bs4 import BeautifulSoup  
import json  
import re
import math 

# Fetch the total number of pages
def fetch_total_number_of_pages(page_url):  
    headers = {  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}  
    response = requests.get(page_url, headers=headers)  

    if response.status_code == 200:  
        soup = BeautifulSoup(response.content, 'html.parser')  
        summary_text = soup.find('span', {'aria-label': 'Summary text'}).text  
        match = re.search(r'(\d+,\d+|\d+) Properties', summary_text)  
        print(match)
        if match:  
            number_of_properties = int(match.group(1).replace(',', ''))
            print("Total number of properties:", number_of_properties)
            return math.ceil(number_of_properties / 24)
        else:  
            print("Could not find total number of properties.")
            return None
    else:  
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return None

def fetch_property_urls(page_url):  
    headers = {  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}  
    response = requests.get(page_url, headers=headers)  

    urls = []  

    if response.status_code == 200:  
        soup = BeautifulSoup(response.content, 'html.parser')  
        
        # Find all script tags of type application/ld+json  
        scripts = soup.find_all('script', {'type': 'application/ld+json'})  
        
        for script in scripts:  
            try:  
                data = json.loads(script.string)  
                if data['@type'] == ["Place", "ItemList"]:  
                    for item in data['itemListElement']:  
                        if item['@type'] == "ItemPage":  
                            urls.append(item['url'])  # Append each found URL to urls list  
            except json.JSONDecodeError:  
                continue  
            except KeyError:  
                continue  

        print(len(urls))
        return urls
    else:  
        print("Failed to retrieve the webpage. Status code:", response.status_code)  
        return []

# Example usage:  

def main():  
    base_url = "https://www.bayut.com/for-sale/property/dubai"  
    num_of_pages = fetch_total_number_of_pages(f'{base_url}/?completion_status=ready')
    
    with open("urls.txt", "w") as file:  
        for page_num in range(1, num_of_pages + 1):  
            if page_num == 1:  
                url = f'{base_url}/?completion_status=ready'  
            else:  
                url = f'{base_url}/page-{page_num}/?completion_status=ready'  

            print(f"Fetching data from: {url}")  
            page_urls = fetch_property_urls(url)  
            if page_urls:  
                for page_url in page_urls:  
                    file.write(page_url + "\n")
                

if __name__ == '__main__':  
    main()  