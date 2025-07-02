import requests
from bs4 import BeautifulSoup
import time


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
                    page_reviews.append(review_text)
        
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


def scrape_all_reviews(base_url, headers, max_pages=None, delay=1):
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


# Configuration
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = "https://reviews.femaledaily.com/products/moisturizer/gel/skintific/5x-ceramide-barrier-repair-moisture-gel-moisturizer"

# Scrape all reviews with pagination
# Set max_pages=None for all pages, or a number to limit pages
all_reviews = scrape_all_reviews(url, headers, max_pages=3, delay=1)

print(f"\n=== SCRAPING SUMMARY ===")
print(f"Total reviews collected: {len(all_reviews)}")
print(f"\n=== ALL REVIEWS ===")
for i, review in enumerate(all_reviews, 1):
    print(f"{i}. {review}")
    print("-" * 80)
