"""
E-Commerce Web Scraper
Scrapes product information (Name, Price, Rating) from books.toscrape.com
and saves the data to a CSV file.

Author: Web Scraping Demo
Date: 2026
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
from typing import List, Dict, Optional


def fetch_page(url: str, headers: Optional[Dict[str, str]] = None) -> Optional[str]:
    """
    Fetch the HTML content of a webpage.
    
    Args:
        url: The URL to fetch
        headers: Optional HTTP headers to include in the request
    
    Returns:
        HTML content as a string, or None if the request fails
    """
    try:
        # Add user-agent to mimic a real browser
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        return response.text
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_rating(rating_class: str) -> str:
    """
    Convert rating class name to numeric rating.
    
    Args:
        rating_class: The CSS class containing the rating (e.g., 'star-rating Three')
    
    Returns:
        Numeric rating as a string (e.g., '3')
    """
    rating_map = {
        'One': '1',
        'Two': '2',
        'Three': '3',
        'Four': '4',
        'Five': '5'
    }
    
    # Extract the rating word from the class
    for word in rating_class.split():
        if word in rating_map:
            return rating_map[word]
    
    return 'N/A'


def parse_products(html_content: str) -> List[Dict[str, str]]:
    """
    Parse product information from HTML content.
    
    Args:
        html_content: HTML content as a string
    
    Returns:
        List of dictionaries containing product information
    """
    products = []
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all product containers
        product_containers = soup.find_all('article', class_='product_pod')
        
        for product in product_containers:
            try:
                # Extract product name
                name_tag = product.find('h3').find('a')
                name = name_tag.get('title', 'N/A') if name_tag else 'N/A'
                
                # Extract price
                price_tag = product.find('p', class_='price_color')
                price = price_tag.text.strip() if price_tag else 'N/A'
                
                # Extract rating
                rating_tag = product.find('p', class_='star-rating')
                if rating_tag:
                    rating_class = rating_tag.get('class', [])
                    rating = parse_rating(' '.join(rating_class))
                else:
                    rating = 'N/A'
                
                # Add product to list
                products.append({
                    'Name': name,
                    'Price': price,
                    'Rating': rating
                })
                
            except Exception as e:
                print(f"Error parsing individual product: {e}")
                continue
        
        print(f"Parsed {len(products)} products from this page")
        
    except Exception as e:
        print(f"Error parsing HTML content: {e}")
    
    return products


def scrape_multiple_pages(base_url: str, num_pages: int = 3) -> List[Dict[str, str]]:
    """
    Scrape products from multiple pages.
    
    Args:
        base_url: The base URL of the website
        num_pages: Number of pages to scrape
    
    Returns:
        List of all scraped products
    """
    all_products = []
    
    for page_num in range(1, num_pages + 1):
        # Construct URL for each page
        if page_num == 1:
            url = base_url
        else:
            url = f"{base_url.rstrip('/')}/catalogue/page-{page_num}.html"
        
        # Fetch and parse the page
        html_content = fetch_page(url)
        
        if html_content:
            products = parse_products(html_content)
            all_products.extend(products)
            
            # Be polite: add a small delay between requests
            time.sleep(1)
        else:
            print(f"Failed to fetch page {page_num}")
            break
    
    return all_products


def save_to_csv(products: List[Dict[str, str]], filename: str = 'scraped_products.csv') -> bool:
    """
    Save product data to a CSV file.
    
    Args:
        products: List of product dictionaries
        filename: Name of the CSV file to create
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if not products:
            print("No products to save!")
            return False
        
        # Define CSV headers
        headers = ['Name', 'Price', 'Rating']
        
        # Write to CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            
            # Write header row
            writer.writeheader()
            
            # Write product rows
            writer.writerows(products)
        
        print(f"\n{'='*60}")
        print(f"✓ SUCCESS: Data successfully saved to '{filename}'")
        print(f"✓ Total products scraped: {len(products)}")
        print(f"{'='*60}\n")
        
        return True
    
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False


def display_sample_products(products: List[Dict[str, str]], num_samples: int = 5):
    """
    Display a sample of scraped products.
    
    Args:
        products: List of product dictionaries
        num_samples: Number of samples to display
    """
    print("\n" + "="*60)
    print("SAMPLE OF SCRAPED PRODUCTS:")
    print("="*60)
    
    for i, product in enumerate(products[:num_samples], 1):
        print(f"\n{i}. {product['Name']}")
        print(f"   Price: {product['Price']}")
        print(f"   Rating: {product['Rating']}/5 stars")
    
    print("\n" + "="*60 + "\n")


def main():
    """
    Main function to orchestrate the web scraping process.
    """
    print("\n" + "="*60)
    print("E-COMMERCE WEB SCRAPER")
    print("="*60 + "\n")
    
    # Configuration
    BASE_URL = "https://books.toscrape.com"
    NUM_PAGES = 3  # Scrape 3 pages to get 20+ products
    OUTPUT_FILE = "scraped_products.csv"
    
    # Step 1: Scrape products from multiple pages
    print("Starting web scraping process...\n")
    products = scrape_multiple_pages(BASE_URL, NUM_PAGES)
    
    # Step 2: Check if we got enough products
    if len(products) < 20:
        print(f"\nWarning: Only scraped {len(products)} products. Attempting to scrape more pages...")
        # Try scraping more pages if needed
        additional_pages = scrape_multiple_pages(BASE_URL, 2)
        products.extend(additional_pages)
    
    # Step 3: Display sample products
    if products:
        display_sample_products(products)
    
    # Step 4: Save to CSV
    if products:
        save_to_csv(products, OUTPUT_FILE)
    else:
        print("No products were scraped. Please check the website URL and try again.")
        return
    
    # Step 5: Final summary
    print(f"Scraping complete! Check '{OUTPUT_FILE}' for all scraped data.")


if __name__ == "__main__":
    main()
