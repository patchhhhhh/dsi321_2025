from serpapi import GoogleSearch
import pandas as pd
from datetime import datetime, timedelta
import os

# 🔑 API Key จาก serpapi.com
API_KEY = "15179a882a5e319597d7dcb0fa7a2e61516f3cfbca11839352ad2f5545f0b5aa"  # ใส่ API Key ที่นี่

# 🔍 คำค้นหาเกี่ยวกับวัสดุก่อสร้างยั่งยืน
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

CSV_FILENAME = "construction_materials_serpapi.csv"

# 📅 กำหนดวันเริ่มต้นย้อนหลัง 5 ปี
five_years_ago = datetime.now() - timedelta(days=5*365)

# 🗂 ฟังก์ชันค้นหาผ่าน GoogleSearch
def search_google(query, num_pages=3):
    all_data = []
    seen_urls = set()  # ใช้เซ็ตเพื่อตรวจสอบ URL ที่เคยเจอ

    # โหลดข้อมูลจากไฟล์ CSV เก่า (ถ้ามี)
    if os.path.exists(CSV_FILENAME):
        df_existing = pd.read_csv(CSV_FILENAME)
        seen_urls.update(df_existing['url'].values)  # นำ URL ที่เคยเจอแล้วมาจากไฟล์ CSV

    for page in range(num_pages):
        params = {
            "q": query,
            "api_key": API_KEY,
            "num": 10,  # จำนวนผลลัพธ์ต่อหน้า
            "start": page * 10  # ข้ามหน้าไป
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic = results.get("organic_results", [])

        data = []
        for item in organic:
            url = item.get("link")
            title = item.get("title")
            snippet = item.get("snippet", "")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # ตรวจสอบว่า URL หรือ title ซ้ำ
            if url not in seen_urls and title not in seen_urls:
                seen_urls.add(url)  # เพิ่ม URL ที่เจอแล้วไปในเซ็ต

                # ตรวจสอบวันเวลาของข้อมูล ว่าตรงกับช่วง 5 ปีที่แล้วหรือไม่
                try:
                    # คุณสามารถปรับตรงนี้หาก Google Search ส่งข้อมูลวันที่มา
                    # กรองข้อมูลโดยดูจากปีที่แตกต่างจากวันที่ใน timestamp
                    # (หากไม่มีข้อมูล timestamp คุณอาจจะใช้เวลาในปัจจุบันแทน)
                    year_in_snippet = int(snippet[-4:])  # สมมุติว่า snippet มีปีอยู่ที่ท้ายสุด
                    if year_in_snippet >= five_years_ago.year:
                        data.append({
                            "timestamp": timestamp,
                            "query": query,
                            "title": title,
                            "url": url,
                            "snippet": snippet
                        })
                except Exception as e:
                    # หากไม่มีปีใน snippet ก็กำหนดให้เป็นข้อมูลที่อยู่ภายใน 5 ปี
                    data.append({
                        "timestamp": timestamp,
                        "query": query,
                        "title": title,
                        "url": url,
                        "snippet": snippet
                    })

        print(f"✅ Fetched {len(data)} results for: '{query}' (page {page + 1})")
        all_data.extend(data)

    return all_data

# 💾 ฟังก์ชันบันทึกข้อมูลลง CSV
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
for query in QUERIES:
    data = search_google(query, num_pages=5)  # กำหนดจำนวนหน้าที่ต้องการดึงข้อมูลเป็น 5 หน้า
    all_results.extend(data)

# 💾 บันทึกลง CSV
if all_results:
    save_to_csv(all_results)
else:
    print("⚠️ No data fetched.")
