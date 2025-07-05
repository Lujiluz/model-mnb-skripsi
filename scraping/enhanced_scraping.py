import requests
from bs4 import BeautifulSoup
import time
import json
import csv
from datetime import datetime


def scrape_reviews_from_page(url, headers, page_num=1):
    """Scrape reviews from a specific page"""
    if page_num > 1:
        page_url = f"{url}?page={page_num}"
    else:
        page_url = url
    
    try:
        response = requests.get(page_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('div', class_='list-reviews')
        
        if not reviews:
            return [], False
        
        comment_content = reviews[0].find_all('p', class_='text-content')
        
        page_reviews = []
        for comment in comment_content:
            clear_content = comment.find_all('span')
            for span in clear_content:
                review_text = span.get_text(strip=True)
                if review_text:  # Only add non-empty reviews
                    page_reviews.append({
                        'review': review_text,
                        'page': page_num,
                        'scraped_at': datetime.now().isoformat()
                    })
        
        # Check if there are more pages by looking for "Next" button
        pagination_container = soup.find('div', class_='pagination-contain')
        has_next = False
        if pagination_container:
            next_button = pagination_container.find('a', class_='paging-prev-text-active', string='Next')
            has_next = next_button is not None
        
        return page_reviews, has_next
        
    except requests.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        return [], False


def scrape_all_reviews(base_url, headers, max_pages=None, delay=2):
    """Scrape reviews from all pages"""
    all_reviews = []
    current_page = 1
    
    print(f"Starting to scrape reviews from: {base_url}")
    
    while True:
        print(f"Scraping page {current_page}...")
        
        page_reviews, has_next = scrape_reviews_from_page(base_url, headers, current_page)
        
        if not page_reviews:
            print(f"No reviews found on page {current_page}. Stopping.")
            break
        
        all_reviews.extend(page_reviews)
        print(f"Found {len(page_reviews)} reviews on page {current_page}")
        print(f"Total reviews collected so far: {len(all_reviews)}")
        
        # Check if we should continue
        if not has_next:
            print("No more pages available. Scraping complete.")
            break
            
        if max_pages and current_page >= max_pages:
            print(f"Reached maximum pages limit ({max_pages}). Stopping.")
            break
        
        current_page += 1
        
        # Be respectful to the server
        if delay > 0:
            time.sleep(delay)
    
    return all_reviews


def save_reviews_to_json(reviews, filename):
    """Save reviews to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)
        print(f"Reviews saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")


def save_reviews_to_csv(reviews, filename):
    """Save reviews to CSV file"""
    try:
        if not reviews:
            print("No data to save to CSV")
            return
            
        # Get fieldnames from the first review
        fieldnames = list(reviews[0].keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reviews)
        print(f"Reviews saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def save_reviews_to_txt(reviews, filename):
    """Save reviews to simple text file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for i, review in enumerate(reviews, 1):
                # Handle different data structures
                if 'nama_bank' in review and 'kode_bank' in review:
                    # Bank data structure
                    f.write(f"{i}. {review['nama_bank']} - Kode: {review['kode_bank']}\n")
                    f.write(f"   (No: {review.get('no', 'N/A')}, Page: {review.get('page', 'N/A')}, Scraped: {review['scraped_at']})\n")
                elif 'review' in review:
                    # Review data structure
                    f.write(f"{i}. {review['review']}\n")
                    f.write(f"   (Page: {review['page']}, Scraped: {review['scraped_at']})\n")
                else:
                    # Generic structure
                    f.write(f"{i}. {review}\n")
                f.write("-" * 80 + "\n")
        print(f"Reviews saved to {filename}")
    except Exception as e:
        print(f"Error saving to TXT: {e}")


# Configuration
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
product_urls = [
    {
        "product_name": "Skintific 5X Ceramide Barrier Repair Moisture Gel Moisturizer",
        "url": "https://reviews.femaledaily.com/products/moisturizer/gel/skintific/5x-ceramide-barrier-repair-moisture-gel-moisturizer"    
    },
    {
        "product_name": "MSH Niacinamide Brightening Moisture Gel",
        "url": "https://reviews.femaledaily.com/products/moisturizer/gel/skintific/msh-niacinamide-brightening-moisture-gel?cat=&cat_id=0&age_range=&skin_type=&skin_tone=&skin_undertone=&hair_texture=&hair_type=&order=newest&page=1"
    },
    {
        "product_name": "Truffle Biome Cream Gel Moisturizer - hydrating the skin",
        "url": "https://reviews.femaledaily.com/products/moisturizer/gel/skintific/truffle-biome-skin-reborn-cream-gel-moisturizer"
    },
    {
        "product_name": "Panthenol Acne Calming Water Gel - treating acne-prone skin",
        "url": "https://reviews.femaledaily.com/products/moisturizer/gel/skintific/5-panthenol-acne-calming-water-gel"
    },
    {
        "product_name": "SymWhite 377 Moisture Gel - fading dark spots",
        "url": "https://reviews.femaledaily.com/products/moisturizer/gel/skintific/symwhite-377-dark-spot-moisture-gel"
    }
]


# Scrape all reviews with pagination
# Set max_pages=None for all pages, or a number to limit pages
max_pages = 50  # Limit to first 50 pages for this example"
all_reviews = scrape_all_reviews(product_urls[4]["url"], headers, max_pages=None, delay=1)

# Generate timestamp for filenames
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

print(f"\n=== SCRAPING SUMMARY ===")
print(f"Total reviews collected: {len(all_reviews)}")

if all_reviews:
    # Save in multiple formats
    save_reviews_to_csv(all_reviews, f"reviews_{product_urls[4]["product_name"]}_{timestamp}.csv")

    print(f"\n=== SAMPLE REVIEWS ===")
    for i, review in enumerate(all_reviews[:5], 1):  # Show first 5 reviews
        if 'nama_bank' in review and 'kode_bank' in review:
            # Bank data structure
            print(f"{i}. {review['nama_bank']} - Kode: {review['kode_bank']}")
            print(f"   (No: {review.get('no', 'N/A')}, From page {review.get('page', 'N/A')})")
        elif 'review' in review:
            # Review data structure
            print(f"{i}. {review['review']}")
            print(f"   (From page {review['page']})")
        else:
            # Generic structure
            print(f"{i}. {review}")
        print("-" * 80)
    
    print(f"\nFiles saved with timestamp: {timestamp}")
else:
    print("No reviews were collected.")
