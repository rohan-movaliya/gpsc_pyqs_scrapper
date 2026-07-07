import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv

def scrape_to_csv(output_file='question_papers.csv'):
    url = 'https://gpsc.gujarat.gov.in/QuestionPaper?name=questionpaperprelimwithans'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("Fetching data from the website...")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table')
        
        if not tables:
            print("No data tables found on the page.")
            return

        table = tables[0]
        rows = table.find_all('tr')
        
        print(f"Found {len(rows) - 1} records. Saving to {output_file}...")
        
        # Open the CSV file for writing
        with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            # Write the header row
            writer.writerow(['Title', 'Advertisement No', 'Date', 'Download Link'])
            
            # Write the data rows
            for row in rows[1:]:  # Skip header row
                columns = row.find_all('td')
                
                if len(columns) >= 4:
                    title = columns[0].get_text(strip=True)
                    adv_no = columns[1].get_text(strip=True)
                    date = columns[2].get_text(strip=True)
                    
                    download_cell = columns[3]
                    link_tag = download_cell.find('a')
                    
                    if link_tag and link_tag.get('href'):
                        href = link_tag.get('href')
                        full_link = urllib.parse.urljoin(url, href)
                    else:
                        full_link = 'Not Available'
                    
                    # Write record to CSV
                    writer.writerow([title, adv_no, date, full_link])
                    
        print(f"Data successfully saved to {output_file}!")
    else:
        print(f"Failed to fetch page. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_to_csv()
