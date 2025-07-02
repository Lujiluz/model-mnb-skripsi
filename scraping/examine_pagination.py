import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

url = "https://reviews.femaledaily.com/products/moisturizer/gel/skintific/5x-ceramide-barrier-repair-moisture-gel-moisturizer"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Examine pagination structure in detail
pagination_container = soup.find('div', class_='pagination-contain')
if pagination_container:
    print("=== Pagination Container Structure ===")
    print(pagination_container.prettify())
    
    # Look for page links
    page_links = pagination_container.find_all('a')
    print(f"\n=== Found {len(page_links)} pagination links ===")
    for i, link in enumerate(page_links):
        href = link.get('href')
        text = link.get_text(strip=True)
        classes = link.get('class', [])
        print(f"Link {i+1}: Text='{text}', href='{href}', classes={classes}")

# Also check the URL structure to understand how pages are numbered
print(f"\n=== Current URL ===")
print(url)

# Try to find if there are page parameters in the current URL or if it's in the pagination links
print("\n=== Checking for page parameters ===")
if '?' in url:
    print("URL contains query parameters")
else:
    print("URL does not contain query parameters - pagination might use URL paths or AJAX")
