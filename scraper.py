import requests
import csv
from bs4 import BeautifulSoup

search_terms = ['engineer','developer']
exclude_terms = ['staff', 'principal', 'senior', 'sr.']













headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}



def scrape_job_data(url, writer):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        sections = soup.find_all('section', class_='level-0')

        for section in sections:
            job_title_tags = section.find_all('a', string=lambda text: text and any(tag in text.lower() for tag in search_terms))
            for job_title_tag in job_title_tags:
                job_title = job_title_tag.text.strip()
                link = job_title_tag['href']

              
                if not any(keyword in job_title.lower() for keyword in exclude_terms):
                    writer.writerow({'Job Title': job_title, 'Link': 'https://boards.greenhouse.io'+link})

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

# Read URLs from companies.csv
with open('companies.csv', 'r', newline='', encoding='utf-8') as companies_file:
    reader = csv.reader(companies_file)
    next(reader)  # Skip header row
    urls = [row[0] for row in reader]

# Create and open a new CSV file to write the scraped data
with open('scraped_job_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Job Title', 'Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through each URL and scrape job data
    for url in urls:
        scrape_job_data(url, writer)

print("Scraped data written to scraped_job_data.csv successfully.")
