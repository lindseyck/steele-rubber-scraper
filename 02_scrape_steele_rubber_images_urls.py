import os
import time
import csv
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# List of search terms pulled using 01_scrape_steele_rubber_makes script - run in batches for better performance
SEARCH_TERMS = [
                #'AM-General', 'American-Motors', 'Auburn', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Cord', 
                #'Crosley', 'DeSoto', 'Deusenburg', 'Dodge', 'Durant', 'Edsel', 'Ford', 'Frazer', 'GMC', 'Graham', 'Graham-Paige', 
                #'Honda', 'Hudson', 'Hummer', 'Hupmobile', 'International', 'Jeep', 'Kaiser', 'Kaiser-Jeep', 'Kissel', 'Lexus', 
                #'Lincoln', 'Mack', 'Marmon', 'Mercury', 'Mitsubishi', 'Nash', 'Nissan', 'Oakland', 'Oldsmobile', 'Packard', 
                'Peerless', 'Pierce-Arrow', 'Plymouth', 'Pontiac', 'Reo', 'Studebaker', 'Stutz', 'Toyota', 'Willys'
                ]

# Directory to save images
SAVE_DIR = "steele_rubber_images"
os.makedirs(SAVE_DIR, exist_ok=True)

# Maximum number of invalid pages before stopping
MAX_INVALID_PAGES = 3

def sanitize_filename(text):
    """Replace invalid filename characters with underscores."""
    return re.sub(r'[<>:"/\\|?*]', '_', text)

def get_image_data(url):
    """Fetch image URLs and alt text from a webpage using Selenium."""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set up WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f"Opening webpage: {url}")
        driver.get(url)
        time.sleep(5)  # Wait for images to load

        # Extract part numbers
        part_numbers = driver.find_elements(By.CLASS_NAME, "part-number")
        part_numbers_text = [part.text.strip().replace("p/n: ", "") for part in part_numbers]

        # Find all image elements
        images = driver.find_elements(By.TAG_NAME, "img")
        image_data = []

        for img in images:
            img_url = img.get_attribute("src")
            alt_text = img.get_attribute("alt")

            if img_url and ".jpg" in img_url:
                sanitized_alt = sanitize_filename(alt_text)  # Clean alt text for filename
                image_data.append((img_url, sanitized_alt))

        driver.quit()

        # Combine part numbers with image data (aligning based on list order)
        combined_data = []
        for i in range(min(len(part_numbers_text), len(image_data))):
            combined_data.append((part_numbers_text[i], image_data[i][0], image_data[i][1]))

        return combined_data

    except Exception as e:
        print(f"Error loading {url}: {e}")
        driver.quit()
        return []

def save_to_csv(data, filename):
    """Save part numbers, image URLs, and alt text to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Part Number", "Image URL", "Alt Text"]) 
        writer.writerows(data)

if __name__ == "__main__":
    for make in SEARCH_TERMS:
        print(f"\nScraping images for: {make}")

        all_image_data = set()  # Use a set to avoid duplicates
        invalid_pages = 0
        page_number = 1

        while invalid_pages < MAX_INVALID_PAGES:
            base_url = f"https://www.steelerubber.com/search?make={make}&ps=100&p={{}}"
            url = base_url.format(page_number)
            img_data = get_image_data(url)

            if img_data:
                all_image_data.update(img_data)
                invalid_pages = 0  # Reset invalid counter
            else:
                invalid_pages += 1  # Increment invalid page counter

            page_number += 1  # Move to next page

        if all_image_data:
            print(f"Found {len(all_image_data)} unique images for {make}. Saving URLs to CSV...")
            # Create a file name
            csv_filename = f'image_urls_{make}.csv'
            # Save the image data in a CSV file
            save_to_csv(all_image_data, csv_filename)
            print(f"Image URLs saved to {csv_filename}")
        else:
            print(f"No images found for {make}.")
