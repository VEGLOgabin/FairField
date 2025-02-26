# Web Scraper for Fairfield Chair

This project is a web scraper built using **Python**, **Playwright**, and **BeautifulSoup** to extract category, collection, and product data from the [Fairfield Chair](https://www.fairfieldchair.com/) website.

## Features
- Extracts categories, subcategories, collections, and product links from the website.
- Saves extracted data as JSON files for further processing.
- Implements retry mechanisms for handling page load failures.
- Uses Playwright for efficient headless browsing and BeautifulSoup for parsing HTML content.

## Installation
Ensure you have Python installed (>=3.7), then install the required dependencies:

```sh
pip install playwright beautifulsoup4 lxml
playwright install
```

## Usage
### 1. Extract Categories and Collections
Run the following command to scrape category and collection data:

```sh
python fair_field_spider.py
```
This will generate a JSON file: `utilities/category-collection.json` containing extracted categories and collections.

### 2. Extract Product Links
After running the first step, execute the command below to extract product links:

```sh
python script.py
```
This will generate a JSON file: `utilities/products-links.json` containing extracted product links.

## How It Works
1. **Extract Categories & Collections**
   - Scrapes the main menu for available categories and collections.
   - Saves data in `category-collection.json`.

2. **Extract Product Links**
   - Reads collection links from `category-collection.json`.
   - Visits each collection page and scrapes product links.
   - Saves data in `products-links.json`.

## Error Handling
- Implements retry logic for failed page loads.
- Uses `TimeoutError` handling to avoid script crashes.
- Ensures smooth execution even with missing elements.

## Dependencies
- Python (>=3.7)
- Playwright
- BeautifulSoup
- lxml

## License
This project is licensed under the MIT License.

## Author
Developed by **[VEGLO H. Gabin](https://github.com/VEGLOgabin)**

