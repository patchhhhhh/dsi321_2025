import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# 🔑 API Key ของ NewsAPI
API_KEY = "your_newsapi_key_here"  # ← ใส่ของคุณเองที่นี่

# 🔍 คำค้นหา
QUERIES = [
    "Life Cycle Assessment of Alternative Construction Materials",
    "Physical and Mechanical Properties of Compressed Earth Blocks",
    "The Potential of Bamboo as a Structural Construction Material",
    "Applications of Concrete Mixed with Recycled Materials",
    "Thermal Insulation from Natural Materials",
    "Developing Construction Materials from Agricultural Waste",
    "Bio-based Construction Materials",
    "The Use of 3D Printing with Alternative Construction Materials",
    "Designing Energy-Efficient Buildings with Alternative Construction Materials",
    "Standards and Regulations for Alternative Construction Materials",
    "Adoption and Acceptance of Alternative Construction Materials in Thailand",
    "The Economic Impact of Using Alternative Construction Materials on Local Communities",
    "Promoting Alternative Construction Materials for Sustainable Development",
    "Consumer Awareness and Understanding of Alternative Construction Materials",
    "Opportunities and Challenges in the Production of Alternative Construction Materials in Thailand",
    "Developing Alternative Construction Materials with Enhanced Properties",
    "Improving the Properties of Alternative Construction Materials with New Technologies",
    "Research and Development of Alternative Construction Materials from Local Resources",
    "Integrating Alternative Construction Materials into the Circular Economy Concept",
    "Building Networks and Collaboration for the Development of Alternative Construction Materials"
]

CSV_FILENAME = "construction_materials_newsapi.csv"
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"

# 📅 วันย้อนหลัง 5 ปี
five_years_ago = datetime.now() - timedelta(days=5*365)
from_date = five_years_ago.strftime('%Y-%m-%d')
to_date = datetime.now().strftime('%Y-%m-%d')

# 📂 โหลด URL ที่เคยบันทึก
def load_seen_urls():
    if os.path.exists(CSV_FILENAME):
        df = pd.read_csv(CSV_FILENAME)
        return set(df['url'].values)
    return set()

# 🔍 ดึงข่าวจาก NewsAPI
def search_news(query, page_size=100, max_pages=10):
    seen_urls = load_seen_urls()
    all_data = []

    for page in range(1, max_pages + 1):
        params = {
            "q": query,
            "from": from_date,
            "to": to_date,
            "sortBy": "relevancy",
            "language": "en",
            "apiKey": API_KEY,
            "pageSize": page_size,
            "page": page
        }

        response = requests.get(NEWSAPI_ENDPOINT, params=params)
        result = response.json()

        if result.get("status") != "ok":
            print(f"❌ Error fetching data for '{query}':", result.get("message"))
            break

        articles = result.get("articles", [])
        if not articles:
            break

        for article in articles:
            url = article["url"]
            if url in seen_urls:
                continue
            seen_urls.add(url)

            all_data.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "query": query,
                "title": article["title"],
                "url": url,
                "publishedAt": article["publishedAt"],
                "source": article["source"]["name"],
                "description": article.get("description", ""),
                "content": article.get("content", "")
            })

        print(f"✅ Fetched {len(articles)} results for '{query}' (page {page})")

    return all_data

# 💾 บันทึกข้อมูลลง CSV
def save_to_csv(data, filename=CSV_FILENAME):
    df_new = pd.DataFrame(data)

    if os.path.exists(filename):
        df_old = pd.read_csv(filename)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new

    df_all.to_csv(filename, index=False)
    print(f"💾 Saved {len(data)} rows to '{filename}'\n")

# 📥 ดึงข้อมูลจากทุก query
all_results = []
results_needed = 1000
queries_handled = 0

# คำนวณว่าเราจะต้องดึงข้อมูลจากหลายหน้าและหลายคำค้น
for query in QUERIES:
    if queries_handled >= results_needed:
        break
    data = search_news(query, page_size=100, max_pages=10)  # ใช้หน้า 10 เพื่อดึง 100 รายการต่อหน้า
    all_results.extend(data)
    queries_handled += len(data)

# 💾 บันทึก
if all_results:
    save_to_csv(all_results)
else:
    print("⚠️ No data fetched.")
