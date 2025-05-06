import feedparser
import csv
from datetime import datetime
import os

# คำค้นหาหลายคำที่เกี่ยวกับ alternative construction materials
search_keywords = [
    "Life Cycle Assessment of Alternative Construction Materials",
    "Physical and Mechanical Properties of Compressed Earth Blocks",
    "The Potential of Bamboo as a Structural Construction Material",
    "Applications of Concrete Mixed with Recycled Materials",
    "Thermal Insulation from Natural Materials"
]

# สร้างโฟลเดอร์ 'data' ถ้ายังไม่มี
os.makedirs("data", exist_ok=True)
# ชื่อไฟล์ CSV ที่จะบันทึก
csv_path = os.path.join("data", "scrap.csv")
file_exists = os.path.isfile(csv_path)

# โหลดลิงก์ที่เคยบันทึกไว้
existing_links = set()
if file_exists:
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames and "link" in reader.fieldnames:
            for row in reader:
                existing_links.add(row["link"])
        else:
            print("❌ ไม่พบหรือไม่มี field 'link' ในไฟล์ CSV")

# เตรียมเขียน CSV
new_entries = 0
with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # เขียน header ถ้ายังไม่มีไฟล์
    if not file_exists:
        writer.writerow(["title", "link", "published", "fetched_at", "keyword"])

    for keyword in search_keywords:
        rss_url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}"
        feed = feedparser.parse(rss_url)

        for entry in feed.entries:
            if entry.link not in existing_links:
                writer.writerow([
                    entry.title,
                    entry.link,
                    entry.published,
                    datetime.now().isoformat(),
                    keyword
                ])
                existing_links.add(entry.link)
                new_entries += 1

print(f"✅ ดึงข่าวใหม่ {new_entries} รายการจาก {len(search_keywords)} คำค้นและบันทึกลง scrap.csv แล้ว")