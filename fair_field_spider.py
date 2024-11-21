




from playwright.sync_api import sync_playwright, TimeoutError
import time
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

import json
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os



           
            
def extract_collections(soup):
    """Extract collections from the parsed HTML soup."""
    category_data = soup.find("div", class_="dropdown menu-top-item cursor-pointer h-100 d-flex align-items-center py-0")



    if category_data:
        collections_list = category_data.find_all("a", class_ = "menu-item")
        if collections_list:
            category_collection_data = []
            for item in collections_list:
                img = item.find("img")
                if img:
                    continue
                
                href = item.get("href")
                if "shop-by-product/" in href:
                    path_data = href.split("shop-by-product/")[-1]
                    path_data = path_data.split("/")
                    if len(path_data) == 2:

                        category_name = path_data[0].title()
                        sub_category_name = category_name
                        collection_name = path_data[1].replace('-', " ").title()
                        collection_link = "https://www.fairfieldchair.com" + href

                        data = {
                            "Category_name": category_name,
                            "Sub_category_name": sub_category_name,
                            "Collection_name": collection_name,
                            "Collection_link": collection_link
                        }

                        category_collection_data.append(data)

                    if len(path_data) == 3:

                        category_name = path_data[0].title()
                        sub_category_name = path_data[1].replace('-', " ").title()
                        collection_name = path_data[-1].replace('-', " ").title()
                        collection_link = "https://www.fairfieldchair.com" + href

                        data = {
                            "Category_name": category_name,
                            "Sub_category_name": sub_category_name,
                            "Collection_name": collection_name,
                            "Collection_link": collection_link
                        }

                        category_collection_data.append(data)

                if "shop-by-room/" in href:
                    path_data = href.split("shop-by-room/")[-1]
                    path_data = path_data.split("/")
                    if len(path_data) == 2:

                        category_name = path_data[0].title()
                        sub_category_name = category_name
                        collection_name = path_data[1].replace('-', " ").title()
                        collection_link = "https://www.fairfieldchair.com" + href

                        data = {
                            "Category_name": category_name,
                            "Sub_category_name": sub_category_name,
                            "Collection_name": collection_name,
                            "Collection_link": collection_link
                        }

                        category_collection_data.append(data)

                    if len(path_data) == 3:

                        category_name = path_data[0].title()
                        sub_category_name = path_data[1].replace('-', " ").title()
                        collection_name = path_data[-1].replace('-', " ").title()
                        collection_link = "https://www.fairfieldchair.com" + href

                        data = {
                            "Category_name": category_name,
                            "Sub_category_name": sub_category_name,
                            "Collection_name": collection_name,
                            "Collection_link": collection_link
                        }

                        category_collection_data.append(data)
  

                if "commercial/" in href:
                    path_data = href.split("commercial/")[-1]
                    path_data = path_data.split("/")
                    if len(path_data) == 2:

                        category_name = path_data[0].title()
                        sub_category_name = category_name
                        collection_name = path_data[1].replace('-', " ").title()
                        collection_link = "https://www.fairfieldchair.com" + href

                        data = {
                            "Category_name": category_name,
                            "Sub_category_name": sub_category_name,
                            "Collection_name": collection_name,
                            "Collection_link": collection_link
                        }

                        category_collection_data.append(data)

                    if len(path_data) == 3:

                        category_name = path_data[0].title()
                        sub_category_name = path_data[1].replace('-', " ").title()
                        collection_name = path_data[-1].replace('-', " ").title()
                        collection_link = "https://www.fairfieldchair.com" + href

                        data = {
                            "Category_name": category_name,
                            "Sub_category_name": sub_category_name,
                            "Collection_name": collection_name,
                            "Collection_link": collection_link
                        }

                        category_collection_data.append(data)


            return category_collection_data
    return []

def scrape_category_data(page, website_url):
    """Navigate to a category page and extract collection data."""
    page.goto(website_url)
    try:
        time.sleep(10)
        html_content = page.content()
        soup = BeautifulSoup(html_content, 'lxml')
        collections = extract_collections(soup)
        
        return collections
    except TimeoutError:
        print(f"TimeoutError: Failed to load collections ")
        return []

def menu_scraper():
    all_collections = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        website_url = "https://www.fairfieldchair.com/products/residential/shop-by-product/seating/banquettes/straight-back-armless-banquette-60-1270-60-l?pageSize=96&page=1&sortKey=name&sortDirection=ASC"
        
        collections = scrape_category_data(page, website_url)
        all_collections = collections

        with open('utilities/category-collection.json', 'w', encoding='utf-8') as f:
            json.dump(all_collections, f, ensure_ascii=False, indent=4)

        print("Data saved to 'utilities/category-collection.json'")
        browser.close()


def load_page_with_retry(page, collection_link, retries=5, delay=5):
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1} to load the page...")
            page.goto(collection_link)
            time.sleep(10) 
            
            if "Products" in page.content():  
                print("Page loaded successfully.")
                html_content = page.content()
                soup = BeautifulSoup(html_content, 'lxml')
  
                return soup
            else:
                print("Necessary content not found, retrying...")
        except Exception as e:
            print(f"Error loading page: {e}, retrying...")
        time.sleep(delay)  
    print("Failed to load the page after retries.")
    return False

def scrape_all_collection_products(page, category_name, sub_category_name, collection_name, collection_link):
    """Navigate to a collection page and extract collection products."""
    print(f"Scraping products for collection: {collection_name}")
    products = []
    try:
        page_number = 1
        soup = load_page_with_retry(page, collection_link)
        if soup:
            print("Page is ready for scraping.")
            product_list = soup.find_all("a", attrs={"target": "_self"})

            current_page_products = [
                    'https://www.fairfieldchair.com' + item.get('href') 
                    for item in product_list 
                    if item.get('href', '').startswith('/products/')
            ] 
            print(len(current_page_products))

            products.extend(current_page_products)

            # print(products)
            pages = soup.find("ul", class_ = "pagination")
            if pages:
                li = pages.find_all("a", class_ = "page-link")
                last_page = li[-2].text.strip()
                total_pages = int(last_page)
            else:
                total_pages = 1

            while page_number < total_pages:
                page_number += 1

                link = f"{collection_link}?page={page_number}"
                soup = load_page_with_retry(page, link)
                if soup:
                    print("Page is ready for scraping.")
                    product_list = soup.find_all("a", attrs={"target": "_self"})

                    current_page_products = [
                            'https://www.fairfieldchair.com' + item.get('href') 
                            for item in product_list
                            if item.get('href', '').startswith('/products/')
                            ] 
                    print(len(current_page_products))

                    products.extend(current_page_products)


                    pages = soup.find("ul", class_ = "pagination")
                    if pages:
                        li = pages.find_all("a", class_ = "page-link")
                        last_page = li[-2].text.strip()
                        total_pages = int(last_page)

                else:
                    print("Exiting due to loading failure.")

            return [
            {
                "category_name": category_name,
                "sub_ccategory_name": sub_category_name,
                "collection_name": collection_name,
                "product_link": product
            }
            for product in products
        ]


        else:
            print("Exiting due to loading failure.")
        


    except PlaywrightTimeoutError:
        print(f"TimeoutError: Failed to load products for {collection_name} at {collection_link}")
        return []


def collections_scraper():
    """Scrape products for all collections listed in the category-collection.json file."""
    all_collections_data = []
    output_dir = 'utilities'
    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            with open(os.path.join(output_dir, 'category-collection.json'), 'r', encoding='utf-8') as file:
                collections_links_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON file: {e}")
            return
        
        for collection in collections_links_data:
            category_name = collection.get("Category_name")
            sub_category_name = collection.get("Sub_category_name")
            collection_name = collection.get("Collection_name")
            collection_link = collection.get("Collection_link")


            if category_name and collection_name and collection_link:
                collections_data = scrape_all_collection_products(page, category_name, sub_category_name, collection_name, collection_link)
                all_collections_data.extend(collections_data)


        output_file = os.path.join(output_dir, 'products-links.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_collections_data, f, ensure_ascii=False, indent=4)

        print(f"Data saved to '{output_file}'")
        browser.close()

    




class ProductScraper:
    def __init__(self):
        self.scraped_data = []
        self.scraped_links = set()
        self.output_file = open('output/products-data.json', 'a', encoding='utf-8')
        self.load_existing_data()

    def load_existing_data(self):
        """Load existing scraped data if available."""
        if os.path.exists('output/products-data.json'):
            try:
                with open('output/products-data.json', 'r', encoding='utf-8') as f:
                    self.scraped_data = json.load(f)
                    self.scraped_links = {(item['Product Link'], item["Collection"], item["Sub Category"], item['Category']) for item in self.scraped_data}
            except json.JSONDecodeError:
                print("Failed to load existing data, skipping load.")

    def load_page_with_retry(self, page, collection_link, retries=5, delay=5):
        for attempt in range(retries):
            try:
                print(f"Attempt {attempt + 1} to load the page...")
                page.goto(collection_link)
                time.sleep(10)  
                
                if "Products" in page.content():
                    print("Page loaded successfully.")
                    html_content = page.content()
                    soup = BeautifulSoup(html_content, 'lxml')
                    return soup
                else:
                    print("Necessary content not found, retrying...")
            except Exception as e:
                print(f"Error loading page: {e}, retrying...")
            time.sleep(delay)
        print("Failed to load the page after retries.")
        return False

    def scrape_product(self, page, product):
        """Scrape product details."""
        try:
            print(f"Scraping product: {product['product_link']}")
            page.goto(product['product_link'])
            time.sleep(7)

            page = self.click_show_more_if_present(page)
            

            specs_dict_details = {}
            specs_dict_dimensions = {}
            description = ""

            specs_container_dimentions = page.locator("div.specs-options-container")
            div_count = specs_container_dimentions.locator("div").count()
            for i in range(div_count):
                div = specs_container_dimentions.locator("div").nth(i)
                name_span = div.locator("span.specs-options-name")
                value_span = div.locator("span.specs-options-value")
                
                if name_span.count() > 0 and value_span.count() > 0:
                    key = name_span.text_content()
                    value = value_span.text_content()
                    specs_dict_dimensions[key.strip()] = value.strip()


            description_elements = page.locator("p", has_text="Description")
            found = False
            for i in range(description_elements.count()):
                if description_elements.nth(i).text_content() == "Description":
                    description_elements.nth(i).click()
                    page = self.click_show_more_if_present(page)
                    description = page.locator("div.description").text_content()
                    found = True
                    break


            details_elements = page.locator("p", has_text="Details")
            for i in range(details_elements.count()):
                if details_elements.nth(i).text_content() == "Details":
                    details_elements.nth(i).click()
                    page = self.click_show_more_if_present(page)
                    specs_container_details = page.locator("div.specs-options-container")
                    div_count = specs_container_details.locator("div").count()
                    for i in range(div_count):
                        div = specs_container_details.locator("div").nth(i)
                        name_span = div.locator("span.specs-options-name")
                        value_span = div.locator("span.specs-options-value")
                        
                        if name_span.count() > 0 and value_span.count() > 0:
                            key = name_span.text_content()
                            value = value_span.text_content()
                            specs_dict_details[key.strip()] = value.strip()
                    found = True
                    break


            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            product_name = soup.find("h1", class_="product-name")
            sku = soup.find('h2', class_="product-sku")

            product_images = []
            imgs = soup.find_all("img", class_="pdp-slider-img")

            if imgs:
                for img in imgs:
                        src = img.get("src")
                        if src:
                            product_images.append(src)


            product_images = list(set(product_images))
            if sku:
                new_product_data = {
                    'Category': product['category_name'],
                    "Sub Category": product["sub_ccategory_name"],
                    'Collection': product['collection_name'],
                    'Product Link': product['product_link'],
                    'Product Title': product_name.text.strip() if product_name else '',
                    'SKU': sku.text.strip().replace("SKU", "").replace(' ', "") if sku else '',
                    "Description": description,
                    'Product Details': specs_dict_details,
                    "Dimensions": specs_dict_dimensions,
                    "Product Images": product_images
                }
                
                self.scraped_data.append(new_product_data)
                with open('output/products-data.json', 'w', encoding='utf-8') as f:
                    json.dump(self.scraped_data, f, ensure_ascii=False, indent=4)
                print(f"Successfully scraped product: {product['product_link']}")

        except Exception as e:
            print(f"Error scraping {product['product_link']}: {e}")

    def click_show_more_if_present(self, page):
        if page.locator("p.show-more.mt-3").count() > 0:
            print("'Show more' button found, clicking it.")
            page.locator("p.show-more.mt-3").click()
        return page

    def scrape_products(self, products):
        """Main function to scrape all products."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            for product in products:
                product_key = (product['product_link'], product['collection_name'], product["sub_ccategory_name"], product['category_name'])
                if product_key not in self.scraped_links:
                    self.scrape_product(page, product)
            browser.close()


   
    
    
#   -----------------------------------------------------------Run------------------------------------------------------------------------

def run_spiders():

    output_dir = 'utilities'
    os.makedirs(output_dir, exist_ok=True)
    menu_scraper()
    collections_scraper()




if __name__ == "__main__":
    try:
        run_spiders()
        with open('utilities/products-links.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
        scraper = ProductScraper()
        scraper.scrape_products(products)
    except Exception as e:
        print(f"Failed to load products: {e}")