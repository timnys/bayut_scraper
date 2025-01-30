import csv
import fetch_property_details
import multiprocessing

def read_urls(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def process_url(url):
    try:
        print(f"Processing {url}")
        details = fetch_property_details.fetch_all_property_details(url)
        return details
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def main():
    urls = read_urls('urls.txt')

    # Open the CSV file for writing
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = [
            "url", "currency", "price", "location", "bed", "bath", "sqft",
            "description", "car_parking", "type", "purpose", "trucheck_date",
            "reference_no", "average_rent", "completion_status", "added_on",
            "fitness", "developer", "usage", "ownership", "swimming_pool",
            "floors", "total_floors", "furnishing", "elevators",
            "completion_year", "security_staff", "central_heating",
            "centrally_air-conditioned", "balcony_or_terrace"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        file.flush()

        # Function to write results to CSV
        def write_result(details):
            if details is not None:
                writer.writerow(details)
                file.flush()  # Ensure data is written to disk

        # Determine the number of processes
        cores = multiprocessing.cpu_count()
        num_processes = max(1, cores // 2)
        print(f"Using {num_processes} processes out of {cores} cores.")

        with multiprocessing.Pool(processes=num_processes) as pool:
            # Start the processes
            for url in urls:
                pool.apply_async(process_url, args=(url,), callback=write_result)
            # Close the pool and wait for the work to finish
            pool.close()
            pool.join()

if __name__ == '__main__':
    main()
