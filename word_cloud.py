import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud_from_excel(file_path, sheet_name, column_name):
    # อ่านข้อมูลจากไฟล์ Excel
    df = pd.read_excel("C:\\Users\\DSICISTU\\Downloads\\scrap.xlsx", sheet_name=sheet_name)

    # รวมข้อความจากคอลัมน์ที่เลือก
    text = ' '.join(df[column_name].dropna().astype(str))

    # สร้าง Word Cloud
    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color='white',
        # ถ้ามีข้อความภาษาไทยให้ใส่ font_path แบบนี้:
        # font_path='THSarabunNew.ttf'
    ).generate(text)

    # แสดงผล Word Cloud
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    # ปรับชื่อไฟล์และคอลัมน์ตามของคุณ
    excel_file = 'scrap.xlsx'
    sheet = 'scrap'
    column = 'title'

    generate_wordcloud_from_excel(excel_file, sheet, column)

if __name__ == "__main__":
    main()
