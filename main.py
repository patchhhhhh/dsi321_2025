from serpapi import DuckDuckGoSearch
import pandas as pd
import time
from datetime import datetime
import os

# 🔑 ใส่ API Key ที่ได้จาก serpapi.com
API_KEY = "15179a882a5e319597d7dcb0fa7a2e61516f3cfbca11839352ad2f5545f0b5aa"  # <== เปลี่ยนตรงนี้

# 🔍 คำค้นหาเกี่ยวกับวัสดุก่อสร้างยั่งยืน
QUERIES = [
    "sustainable construction materials",
    "eco friendly building materials",
    "construction materials Thailand",
    "green construction trends"
]

# 🕒 ตั้งเวลาคั่นระหว่างการดึงข้อมูล (หน่วย: นาที)
INTERVAL_MINUTES = 30
CSV_FILENAME = "construction_materials_serpapi.csv"

def search_duckduckgo(query):
    params = {
        "q": query,
        "api_key": API_KEY
    }

    search = DuckDuckGoSearch(params)
    results = search.get_dict()
    organic = results.get("organic_results", [])

    data = []
    for item in organic:
        data.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "query": query,
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet", "")
        })

    print(f"✅ Fetched {len(data)} results for: '{query}'")
    return data

def save_to_csv(data, filename=CSV_FILENAME):
    df_new = pd.DataFrame(data)

    if os.path.exists(filename):
        df_old = pd.read_csv(filename)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(filename, index=False)
    print(f"💾 Saved {len(data)} rows to '{filename}'\n")

# 🔁 วนลูปทุก INTERVAL_MINUTES นาที
print("🔄 Start DuckDuckGo (via SerpAPI) scraping loop. Press Ctrl+C to stop.")
try:
    while True:
        all_results = []

        for query in QUERIES:
            data = search_duckduckgo(query)
            all_results.extend(data)
            time.sleep(5)  # พักระหว่างคำค้น

        if all_results:
            save_to_csv(all_results)

        print(f"⏳ Waiting {INTERVAL_MINUTES} minutes...\n")
        time.sleep(INTERVAL_MINUTES * 60)

except KeyboardInterrupt:
    print("🛑 Stopped by user.")
