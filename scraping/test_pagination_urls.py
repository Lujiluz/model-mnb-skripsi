import requests
from bs4 import BeautifulSoup
import time

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

base_url = "https://reviews.femaledaily.com/products/moisturizer/gel/skintific/5x-ceramide-barrier-repair-moisture-gel-moisturizer"

# Test different URL patterns that might work for pagination
test_urls = [
    f"{base_url}?page=2",
    f"{base_url}/page/2",
    f"{base_url}?p=2", 
    f"{base_url}#page=2"
]

print("=== Testing different pagination URL patterns ===")
for test_url in test_urls:
    try:
        response = requests.get(test_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            reviews = soup.find_all('div', class_='list-reviews')
            if reviews:
                comment_content = reviews[0].find_all('p', class_='text-content')
                print(f"\nURL: {test_url}")
                print(f"Status: {response.status_code}")
                print(f"Found {len(comment_content)} comments")
                if len(comment_content) > 0:
                    first_comment = comment_content[0].find('span')
                    if first_comment:
                        print(f"First comment preview: {first_comment.get_text(strip=True)[:100]}...")
            else:
                print(f"\nURL: {test_url} - No reviews found")
        else:
            print(f"\nURL: {test_url} - Status: {response.status_code}")
    except Exception as e:
        print(f"\nURL: {test_url} - Error: {e}")
    
    time.sleep(1)  # Be respectful to the server
