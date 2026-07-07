import os
import csv
import requests
import time
import re

def sanitize_filename(name):
    # Remove characters that are invalid in Windows/Linux filenames
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def download_pdfs(csv_file='question_papers.csv', download_dir='PDFs'):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Starting downloads. PDFs will be saved to the '{download_dir}' folder...")
    
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader) # Skip header row
        
        for i, row in enumerate(reader, start=1):
            if len(row) < 4:
                continue
                
            title, adv_no, date, link = row
            
            if link == 'Not Available' or not link.startswith('http'):
                print(f"[{i}] Skipping: No valid link for '{title}'")
                continue
                
            # Create a safe filename
            safe_title = sanitize_filename(title)[:100]  # Limit length
            safe_adv = sanitize_filename(adv_no).replace(' ', '_')
            
            filename = f"{i}_{safe_adv}_{safe_title}.pdf"
            filepath = os.path.join(download_dir, filename)
            
            # Skip if file already exists (allows resuming if interrupted)
            if os.path.exists(filepath):
                print(f"[{i}] Already downloaded: {filename}")
                continue
                
            print(f"[{i}] Downloading: {filename}")
            try:
                # Add a timeout so it doesn't hang indefinitely on a bad connection
                response = requests.get(link, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    with open(filepath, 'wb') as pdf_file:
                        pdf_file.write(response.content)
                else:
                    print(f"    -> Failed with status {response.status_code}")
                    
            except Exception as e:
                print(f"    -> Error downloading: {e}")
                
            # Add a small delay (1 second) between requests to avoid overloading the server 
            # and preventing your IP from getting blocked.
            time.sleep(1)
            
    print("All downloads finished!")

if __name__ == "__main__":
    download_pdfs()
