import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import zipfile

# Step 1: Set up directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP_DIR = os.path.join(BASE_DIR, "zips")
CSV_DIR = os.path.join(BASE_DIR, "csvs")

os.makedirs(ZIP_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)

# Step 2: Scrape the page for .zip links
BASE_URL = "https://mis.nyiso.com/public/" 
LIST_URL = "https://mis.nyiso.com/public/P-58Blist.htm"

print(f"Fetching page: {LIST_URL}")
response = requests.get(LIST_URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Adjusting the URL joining correctly
zip_links = [urljoin(BASE_URL + '/', a['href']) for a in soup.find_all('a', href=True) if a['href'].endswith('.zip')]

print(f"Found {len(zip_links)} zip files.")

# Step 3: Download each .zip and extract
for link in zip_links:
    zip_filename = os.path.basename(link)
    zip_path = os.path.join(ZIP_DIR, zip_filename)

    # Download the .zip file if it doesn't exist
    if not os.path.exists(zip_path):
        print(f"Downloading {zip_filename}...")
        try:
            r = requests.get(link)
            r.raise_for_status()
            with open(zip_path, 'wb') as f:
                f.write(r.content)
            print(f"Saved {zip_filename}")
        except Exception as e:
            print(f"Failed to download {zip_filename}: {e}")
            continue
    else:
        print(f"Skipping {zip_filename} (already exists).")

    # Step 4: Extract contents
    print(f"Extracting {zip_filename}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(CSV_DIR)
        print(f"Extracted {zip_filename} into /csvs/")
    except zipfile.BadZipFile as e:
        print(f"Error extracting {zip_filename}: {e}")

print("Done.")
