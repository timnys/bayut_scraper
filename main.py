import csv
import fetch_property_details

def read_urls(file_path):  
    with open(file_path, 'r') as file:  
        return [line.strip() for line in file if line.strip()]  


def main():  
    urls = read_urls('urls.txt')  
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:  
        fieldnames = ["url", "currency", "price", "location",
                      "bed", "bath", "sqft", "description", "car_parking", "type", "purpose", "trucheck_date", 
                      "reference_no", "average_rent", "completion_status", "added_on", "fitness",
                      "developer", "usage", "ownership",
                      "swimming_pool", "floors", "total_floors", "furnishing",  
                      "elevators", "completion_year", "security_staff",  
                      "central_heating", "centrally_air-conditioned", "balcony_or_terrace"]  
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)  
        writer.writeheader()  
        
        for url in urls:  
            print(url)
            details = fetch_property_details.fetch_all_property_details(url)  
            writer.writerow(details) 

if __name__ == '__main__':  
    main()  