import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud_from_excel(file_path, sheet_name, column_name):
    # อ่านไฟล์ CSV
    df = pd.read_csv(file_path)

    # ล้างช่องว่างหัวท้ายจากชื่อคอลัมน์
    df.columns = df.columns.str.strip()

    # แสดงชื่อคอลัมน์ทั้งหมดเพื่อช่วยตรวจสอบ
    print("Available columns:", df.columns.tolist())

    # ตรวจสอบว่าคอลัมน์ที่ระบุมีอยู่จริงหรือไม่
    if column_name not in df.columns:
        print(f"❌ ไม่พบคอลัมน์ '{column_name}' ในไฟล์")
        return

    # รวมข้อความจากคอลัมน์ที่เลือก
    text = ' '.join(df[column_name].dropna().astype(str))

    # สร้าง Word Cloud
    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color='white',
        # font_path='THSarabunNew.ttf'  # หากเป็นภาษาไทยให้ปลดคอมเมนต์และใช้ฟอนต์ไทย
    ).generate(text)

    # แสดงผล Word Cloud
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    csv_file = 'data/cleaned.csv'  # เปลี่ยน path ตามจริง
    sheet = None  # ไม่จำเป็นต้องใช้สำหรับ CSV
    column = 'cleaned_title'  # แก้ตามชื่อคอลัมน์จริง

    generate_wordcloud_from_excel(csv_file, sheet, column)

if __name__ == "__main__":
    main()
