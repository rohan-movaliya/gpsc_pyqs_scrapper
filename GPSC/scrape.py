import requests
from bs4 import BeautifulSoup

url = 'https://gpsc.gujarat.gov.in/QuestionPaper?name=questionpaperprelimwithans'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("Fetching data from the website...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(f"\n--- Page Title ---")
    print(soup.title.string if soup.title else "No title found")
    
    print("\n--- Data Structure (Table Columns) ---")
    tables = soup.find_all('table')
    if tables:
        print(f"Found {len(tables)} table(s) on the page.")
        # Let's look at the headers of the first table to see what data is stored
        headers = tables[0].find_all('th')
        if headers:
            for th in headers:
                print(f"- {th.get_text(strip=True)}")
        else:
            print("No column headers found in the table.")
            
        # Preview the first row of data
        print("\n--- First Row Data Preview ---")
        rows = tables[0].find_all('tr')
        if len(rows) > 1:
            first_row_cols = rows[1].find_all('td')
            for td in first_row_cols:
                print(f"- {td.get_text(strip=True)}")
    else:
        print("No tables found. The data might be structured using divs or lists.")
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
