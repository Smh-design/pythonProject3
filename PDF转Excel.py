import pdfplumber
import pandas as pd

def pdf_to_excel(pdf_path, excel_path):
    # 用于存储所有页面的数据
    all_tables = []

    # 打开PDF文件
    with pdfplumber.open(pdf_path) as pdf:
        # 遍历每一页
        for page in pdf.pages:
            # 提取表格
            tables = page.extract_tables()
            for table in tables:
                all_tables.extend(table)

    # 创建DataFrame
    df = pd.DataFrame(all_tables[1:], columns=all_tables[0])

    # 保存为Excel文件
    df.to_excel(excel_path, index=False)

    print(f"PDF已成功转换为Excel并保存为 {excel_path}")

# 使用示例
pdf_path = "D:\Desktop\SU-Apr2024.pdf"
excel_path = "output_excel_file.xlsx"
pdf_to_excel(pdf_path, excel_path)