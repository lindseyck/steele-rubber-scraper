# Steele Rubber Scraper

This repository contains Python scripts for scraping automotive make data, image URLs, and merging CSV files from Steele Rubber.

## Features
- Scrapes automotive makes from Steele Rubber's website.
- Extracts image URLs for each make.
- Merges multiple CSV files into a single dataset.

## Prerequisites
- Python 3.x
- pip

## Installation
Clone the repository:
```sh
git clone https://github.com/lindseyck/steele-rubber-scraper.git
cd steele-rubber-scraper
```

Install dependencies:
```sh
pip install -r requirements.txt
```

## Usage
### Step 1: Scrape Available Car Makes
```sh
python 01_scrape_steele_rubber_makes.py
```
This outputs a list of makes to populate the 02_scrape_steele_rubber_images_urls file.

### Step 2: Scrape Image URLs
Update the `SEARCH_TERMS` in `02_scrape_steele_rubber_images_urls.py`, then run:
```sh
python 02_scrape_steele_rubber_images_urls.py
```

### Step 3: Union CSV Files
After scraping, union all CSV files:
```sh
python 03_union_steele_rubber_files.py
```
