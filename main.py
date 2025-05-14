from prefect import flow, task
import feedparser
import csv
from datetime import datetime
import os

search_keywords = [
    "Research and Development of Alternative Construction Materials from Local Resources",
    "Integrating Alternative Construction Materials into the Circular Economy Concept",
    "Building Networks and Collaboration for the Development of Alternative Construction Materials"
]

@task
def create_csv_if_not_exists(csv_path: str):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    if not os.path.isfile(csv_path):
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["title", "link", "published", "fetched_at", "keyword"])
        return set()
    else:
        existing_links = set()
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames and "link" in reader.fieldnames:
                for row in reader:
                    existing_links.add(row["link"])
            else:
                print("❌ ไม่พบหรือไม่มี field 'link' ในไฟล์ CSV")
        return existing_links

@task
def fetch_news(keyword: str):
    rss_url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}"
    feed = feedparser.parse(rss_url)
    return feed.entries

@task
def write_new_entries(csv_path: str, entries, existing_links: set, keyword: str):
    new_count = 0
    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for entry in entries:
            if entry.link not in existing_links:
                writer.writerow([
                    entry.title,
                    entry.link,
                    entry.published,
                    datetime.now().isoformat(),
                    keyword
                ])
                existing_links.add(entry.link)
                new_count += 1
    return new_count

@flow
def scrape_google_news():
    csv_path = "data/scrap.csv"
    total_new_entries = 0
    existing_links = create_csv_if_not_exists(csv_path)

    for keyword in search_keywords:
        entries = fetch_news(keyword)
        new_count = write_new_entries(csv_path, entries, existing_links, keyword)
        total_new_entries += new_count

    print(f"✅ ดึงข่าวใหม่ {total_new_entries} รายการจาก {len(search_keywords)} คำค้นและบันทึกลง {csv_path} แล้ว")

if __name__ == "__main__":
    scrape_google_news()
