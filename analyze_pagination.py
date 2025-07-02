import requests
from bs4 import BeautifulSoup
import time

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

url = "https://reviews.femaledaily.com/products/moisturizer/gel/skintific/5x-ceramide-barrier-repair-moisture-gel-moisturizer"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

print("=== Looking for pagination elements ===")
# Look for common pagination classes/elements
pagination_elements = [
    'pagination', 'pager', 'page-nav', 'next', 'prev', 'page-number',
    'page-link', 'page-item', 'load-more', 'show-more'
]

for element_class in pagination_elements:
    found = soup.find_all(class_=lambda x: x and element_class in x.lower())
    if found:
        print(f"\nFound elements with '{element_class}' in class:")
        for elem in found[:3]:  # Show first 3 matches
            print(f"  Tag: {elem.name}, Class: {elem.get('class')}, Text: {elem.get_text(strip=True)[:100]}")

# Look for buttons or links that might be pagination
print("\n=== Looking for potential pagination buttons/links ===")
buttons = soup.find_all(['button', 'a'], string=lambda text: text and any(word in text.lower() for word in ['next', 'more', 'load', 'page', 'selanjutnya', 'lainnya']))
for button in buttons[:5]:
    print(f"Tag: {button.name}, Text: '{button.get_text(strip=True)}', href/onclick: {button.get('href') or button.get('onclick')}")

# Check if there are any AJAX endpoints or data attributes
print("\n=== Looking for data attributes that might indicate AJAX loading ===")
ajax_elements = soup.find_all(attrs={'data-url': True})
for elem in ajax_elements[:3]:
    print(f"Tag: {elem.name}, data-url: {elem.get('data-url')}")

# Look for script tags that might contain pagination logic
print("\n=== Looking for relevant script content ===")
scripts = soup.find_all('script')
for script in scripts:
    if script.string and any(word in script.string.lower() for word in ['page', 'pagination', 'load', 'more', 'next']):
        print(f"Found relevant script content (first 200 chars): {script.string[:200]}")
        break
