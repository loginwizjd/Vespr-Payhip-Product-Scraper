import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import os
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

def display_ascii_art():
    print(CYAN + r"""                                              
                  Vespr Payhip Scraper V1.1.0
    """ + RESET)
    print(GREEN + "Welcome to Vespr Payhip Scraper!" + RESET)
    print("Scrape Payhip product pages and export data in JSON, CSV, or Google Drive.")
    print("----------------------------------------------------------")

def validate_url(user_url):
    if user_url.startswith("https://payhip.com/") and "/collection/all" in user_url:
        return user_url
    elif user_url.startswith("https://payhip.com/"):
        corrected_url = user_url.rstrip("/") + "/collection/all"
        print(GREEN + f"✅ URL corrected to: {corrected_url}" + RESET)
        return corrected_url
    else:
        print(RED + "❌ Invalid URL. Please enter a valid Payhip URL in the format:" + RESET)
        print("   https://payhip.com/<username>/collection/all")
        return None

def get_product_description(url, retries=3):
    for attempt in range(retries):
        try:
            res = requests.get(url, headers=HEADERS)
            if res.status_code != 200:
                raise Exception(f"Status code: {res.status_code}")
            soup = BeautifulSoup(res.text, "html.parser")
            desc_el = soup.select_one("div.product-description")
            return desc_el.get_text(strip=True) if desc_el else "No description"
        except Exception as e:
            print(RED + f"Error fetching product description (Attempt {attempt + 1}/{retries}): {e}" + RESET)
            time.sleep(2)
    return "No description"

def scrape_page(url, delay):
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print(RED + f"❌ Failed to fetch page: {url}" + RESET)
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    product_cards = soup.select("div.product-card-wrapper")
    products = []
    total_products = len(product_cards)
    for index, card in enumerate(product_cards, start=1):
        try:
            title_tag = card.select_one("h3.card__heading a") or card.select_one("h4.card__heading a")
            title = title_tag.text.strip() if title_tag else "N/A"
            link = title_tag["href"] if title_tag else "#"
            if link.startswith("/"):
                link = f"https://payhip.com{link}"
            price_tag = card.select_one("span.price-item--regular")
            price = price_tag.text.strip() if price_tag else "Free"
            img_tag = card.select_one("img")
            image = img_tag["src"] if img_tag else "N/A"
            description = get_product_description(link)
            time.sleep(delay)
            products.append({
                "title": title,
                "price": price,
                "link": link,
                "image": image,
                "description": description
            })
            progress = (index / total_products) * 100
            print(GREEN + f"[{progress:.2f}%] Scraped: {title}" + RESET)
            print(f"    Description: {description[:50]}...")
            print(f"    Link: {link}")
        except Exception as e:
            print(RED + f"Error scraping product: {e}" + RESET)
            continue
    return products

def get_total_pages(base_url):
    try:
        res = requests.get(base_url, headers=HEADERS)
        if res.status_code != 200:
            print(RED + f"❌ Failed to fetch the page. Status code: {res.status_code}" + RESET)
            return 1
        soup = BeautifulSoup(res.text, "html.parser")
        pagination = soup.select_one("div.pagination-wrapper")
        if not pagination:
            print(YELLOW + "ℹ️ No pagination found. Assuming only 1 page." + RESET)
            return 1
        page_links = pagination.select("a")
        page_numbers = set()
        for link in page_links:
            href = link.get("href", "")
            if "page=" in href:
                try:
                    page_number = int(href.split("page=")[-1])
                    page_numbers.add(page_number)
                except ValueError:
                    continue
        max_page_value = max(page_numbers) if page_numbers else 0
        total_pages = (max_page_value // 16) + 1
        print(GREEN + f"✅ Total pages identified: {total_pages}" + RESET)
        return total_pages
    except Exception as e:
        print(RED + f"❌ Error determining total pages: {e}" + RESET)
        return 1

def export_to_json(products, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)
    print(GREEN + f"✅ Data exported to {filename} (JSON)" + RESET)

def export_to_csv(products, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price", "Link", "Image", "Description"])
        for product in products:
            writer.writerow([product["title"], product["price"], product["link"], product["image"], product["description"]])
    print(GREEN + f"✅ Data exported to {filename} (CSV)" + RESET)

def scrape_all():
    display_ascii_art()
    while True:
        user_url = input(CYAN + "Enter Payhip URL: " + RESET).strip()
        validated_url = validate_url(user_url)
        if validated_url:
            break
    delay = input(YELLOW + "Enter delay between requests (in seconds, default 1): " + RESET).strip()
    delay = float(delay) if delay.isdigit() else 1.0
    total_pages = get_total_pages(validated_url)
    print(f"Total pages: {total_pages}")
    products = []
    for page in range(total_pages):
        page_offset = page * 16
        current_page = f"{validated_url}?page={page_offset}" if page_offset > 0 else validated_url
        print(CYAN + f"Scraping page: {current_page}" + RESET)
        page_products = scrape_page(current_page, delay)
        products.extend(page_products)
    print(YELLOW + "Export options:" + RESET)
    print("1. Export to JSON")
    print("2. Export to CSV")
    export_choice = input(CYAN + "Choose an export option (1/2): " + RESET).strip()
    filename = input(YELLOW + "Enter filename (without extension): " + RESET).strip()
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    if export_choice == "1":
        export_to_json(products, f"{filename}.json")
    elif export_choice == "2":
        export_to_csv(products, f"{filename}.csv")
    else:
        print(RED + "❌ Invalid choice. No export performed." + RESET)
    print(GREEN + f"✅ Scraped {len(products)} products." + RESET)

if __name__ == "__main__":
    scrape_all()