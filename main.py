import re
import requests
import pandas as pd
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

def extract_ids_from_url(url: str) -> Optional[tuple]:
    """Ekstrak shop_id dan item_id dari URL produk Shopee."""
    match = re.search(r'i\.(\d+)\.(\d+)', url)
    if match:
        return match.group(1), match.group(2)
    return None

def fetch_product_title(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Judul produk biasanya ada di tag <title> atau meta property
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text.strip()
        # Alternatif: meta property
        meta_title = soup.find('meta', property='og:title')
        if meta_title and meta_title.get('content'):
            return meta_title['content'].strip()
    except Exception as e:
        print(f"Error fetching product title: {e}")
    return "Unknown Product"

def fetch_ratings(shop_id: str, item_id: str, limit: int = 20, max_reviews: Optional[int] = None) -> List[Dict[str, Any]]:
    """Ambil semua review dari produk Shopee berdasarkan shop_id dan item_id."""
    ratings_url = (
        'https://shopee.co.id/api/v2/item/get_ratings?'
        'filter=0&flag=1&itemid={item_id}&limit={limit}&offset={offset}&shopid={shop_id}&type=0'
    )
    offset = 0
    all_ratings = []
    while True:
        url = ratings_url.format(shop_id=shop_id, item_id=item_id, limit=limit, offset=offset)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Error fetching data: {e}")
            break

        ratings = data.get('data', {}).get('ratings', [])
        if not ratings:
            break

        for rating in ratings:
            all_ratings.append({
                'username': rating.get('author_username', ''),
                'rating': rating.get('rating_star', ''),
                'comment': rating.get('comment', '')
            })
            # mencetak review yang di-scrape
            print(rating.get('author_username', ''))
            print(rating.get('rating_star', ''))
            print(rating.get('comment', ''))
            print('-' * 80)

            if max_reviews and len(all_ratings) >= max_reviews:
                return all_ratings

        if len(ratings) < limit:
            break
        offset += limit
    return all_ratings

def save_reviews(data: List[Dict[str, Any]], basename: str = 'shopee_reviews'):
    """Simpan data review ke file CSV, Excel, dan JSON."""
    df = pd.DataFrame(data)
    # menyimpan data ke file CSV
    df.to_csv(f'{basename}.csv', index=False, encoding='utf-8-sig')
    # menyimpan data ke file Excel
    df.to_excel(f'{basename}.xlsx', index=False, encoding='utf-8-sig')
    # menyimpan data ke file JSON
    df.to_json(f'{basename}.json', orient='records', force_ascii=False)

def main():
    url = 'https://shopee.co.id/Premium-Brill-Eighty-eight-Flannel-Shirt-077-i.32031549.1991571675'
    ids = extract_ids_from_url(url)
    if not ids:
        print("Gagal mengekstrak shop_id dan item_id dari URL.")
        return
    shop_id, item_id = ids
    product_title = fetch_product_title(url)
    print(f"Judul produk: {product_title}")
    reviews = fetch_ratings(shop_id, item_id)
    if reviews:
        save_reviews(reviews, basename=product_title.replace(' ', '_').replace('/', '_'))
        print(f"Berhasil menyimpan {len(reviews)} review.")
    else:
        print("Tidak ada review yang ditemukan.")

if __name__ == "__main__":
    main()