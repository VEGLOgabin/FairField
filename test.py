
# from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright
# import time

# def load_page_with_retry(page, url, retries=5, delay=5):
#     for attempt in range(retries):
#         try:
#             print(f"Attempt {attempt + 1} to load the page...")
#             page.goto(url)
#             time.sleep(20)  # Adjust the wait time for content to load
#             # Check if the page has loaded necessary content
#             if "Products" in page.content():  # Example check
#                 print("Page loaded successfully.")
#                 html_content = page.content()
#                 soup = BeautifulSoup(html_content, 'lxml')
  
#                 return [True, soup, page]
#             else:
#                 print("Necessary content not found, retrying...")
#         except Exception as e:
#             print(f"Error loading page: {e}, retrying...")
#         time.sleep(delay)  # Wait before retrying
#     print("Failed to load the page after retries.")
#     return False


# def click_show_more_if_present(page):
#     # Check if the "show more" button is present
#     if page.locator("p.show-more.mt-3").count() > 0:
#         print("'Show more' button found, clicking it.")
#         page.locator("p.show-more.mt-3").click()
#         # time.sleep(3)  # Wait for the action to complete
#         return page
#     else:
#         print("'Show more' button not found, continuing execution.")
#         return page

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()
#     url = "https://www.fairfieldchair.com/products/commercial/casegoods/pull-up-drink-tables/veneto-drink-table-8195-88?upholstery_options=19602734&search=true"

#     result = load_page_with_retry(page, url)
#     if result:
#         print("Page is ready for scraping.")
#         soup = result[1]

#         page = result[-1]

#         page = click_show_more_if_present(page)

#         specs_container_dimentions = page.locator("div.specs-options-container")
    
#         specs_dict_dimensions = {}
        
#         div_count = specs_container_dimentions.locator("div").count()
#         for i in range(div_count):
#             div = specs_container_dimentions.locator("div").nth(i)
#             name_span = div.locator("span.specs-options-name")
#             value_span = div.locator("span.specs-options-value")
            
#             if name_span.count() > 0 and value_span.count() > 0:
#                 key = name_span.text_content().strip().replace(":", "")
#                 value = value_span.text_content().strip()
#                 specs_dict_dimensions[key] = value
        
#         print(specs_dict_dimensions)

#         if page.locator("p", has_text="Description").count()>0:

#             description_elements = page.locator("p", has_text="Description")
#             found = False
#             for i in range(description_elements.count()):
#                 if description_elements.nth(i).text_content().strip() == "Description":
#                     print("Exact element found!")
#                     description_elements.nth(i).click() 

#                     page = click_show_more_if_present(page)
#                     if page.locator("div.description").count()>0:

#                         description = page.locator("div.description")
#                         description = description.text_content().strip()
#                         print(description)
#                     time.sleep(6)
#                     found = True
#                     break

#             if not found:
#                 print("No element with exact text 'Description' found.")

#         if page.locator("p", has_text="Details").count()>0:

#             details_elements = page.locator("p", has_text="Details")
#             found = False
#             for i in range(details_elements.count()):
#                 if details_elements.nth(i).text_content().strip() == "Details":
#                     print("Exact element found!")
#                     details_elements.nth(i).click()  

#                     page  = click_show_more_if_present(page)
#                     specs_container_details = page.locator("div.specs-options-container")
#                     specs_dict_details = {}
#                     div_count = specs_container_details.locator("div").count()
#                     for i in range(div_count):
#                         div = specs_container_details.locator("div").nth(i)
#                         name_span = div.locator("span.specs-options-name")
#                         value_span = div.locator("span.specs-options-value")
                        
#                         if name_span.count() > 0 and value_span.count() > 0:
#                             key = name_span.text_content().strip().replace(":", "")
#                             value = value_span.text_content().strip()
#                             specs_dict_details[key] = value
                    
#                     print(specs_dict_details)
                    
#                     time.sleep(15)
#                     found = True
#                     break

#             if not found:
#                 print("No element with exact text 'Description' found.")

#         with open("output1.html", "w", encoding="utf-8") as file:
#             file.write(soup.prettify())
#         # products = soup.find_all("div", class_ = "col-6 col-md-3 col-lg-3 product-widget px-5 py-3 mb-4")
#         # products = soup.find_all("a", attrs={"target": "_self"})

#         # products_links = [
#         #     'https://www.fairfieldchair.com' + item.get('href') 
#         #     for item in products 
#         #     if item.get('href', '').startswith('/products/')
#         #     ] 
#         # print(len(products_links))
#         # for item in products_links:
#         #     print(item)

#         # pages = soup.find("ul", class_ = "pagination")
#         # if pages:
#         #     li = pages.find_all("a", class_ = "page-link")
#         #     last_data = li[-2].text.strip()
#         #     total_pages = int(last_data)
#         #     print(total_pages)
#     else:
#         print("Exiting due to loading failure.")
#     browser.close()























import json
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

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

if __name__ == "__main__":
    try:
        with open('utilities/products-links.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
        scraper = ProductScraper()
        scraper.scrape_products(products)
    except Exception as e:
        print(f"Failed to load products: {e}")


