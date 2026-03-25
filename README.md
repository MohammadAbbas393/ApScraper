# ApScraper

A Python web scraper that pulls apartment listing prices from multiple sources and exports the data to a CSV file for easy side-by-side comparison. Built to solve a personal problem finding off-campus housing.

## Features

- Scrapes apartment listings from multiple websites
- Pulls title, location, price, and contact info for each listing
- Exports everything to a clean CSV file
- Focused on the Houston area (easy to adapt for other cities)

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/MohammadAbbas393/ApScraper
cd ApScraper

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the scraper
python scraper.py
```

The script will run and save results to a `listings.csv` file in the project folder.

## Output

The CSV file includes the following columns:

| Column | Description |
|---|---|
| title | Listing name or headline |
| location | Address or neighborhood |
| price | Monthly rent |
| contact | Phone number or email if listed |
| source | Which site the listing came from |

## Requirements

- Python 3.8+
- requests
- BeautifulSoup4

Install them with:

```bash
pip install requests beautifulsoup4
```

## Notes

Web scraping depends on the structure of the target sites. If a site updates its layout, the scraper may need adjustments. Always check that scraping is allowed by the site's terms of service before running.

