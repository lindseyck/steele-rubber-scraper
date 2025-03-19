# Steele Rubber Scraper

This repository contains Python scripts for scraping automotive make data, image URLs, and combining CSV files from Steele Rubber.

## Scripts
- **01_scrape_steele_rubber_makes.py** – Scrapes available automotive makes from Steele Rubber's website.
- **02_scrape_steele_rubber_images_urls.py** – Scrapes image URLs and part numbers for different makes.
- **03_union_steele_rubber_files.py** – Merges CSV files containing image URLs into one dataset.

## Installation
Clone the repository:
```sh
git clone https://github.com/lindseyck/steele-rubber-scraper.git
cd steele-rubber-scraper
```

## Install Dependencies
```sh
pip install selenium webdriver-manager pandas requests
```
