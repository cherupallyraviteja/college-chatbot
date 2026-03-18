import pdfplumber
import pandas as pd

pdf_path = "2025-26-B.TECH II & III ACADEMIC CALENDER.pdf"   # change to your PDF path

all_tables = []

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        tables = page.extract_tables()

        for table_index, table in enumerate(tables):
            df = pd.DataFrame(table)
            df["page_number"] = page_num
            df["table_number"] = table_index + 1
            all_tables.append(df)

print("Extracted Tables from PDF:")
# Print extracted tables
for i, df in enumerate(all_tables, start=1):
    print(f"\n--- Table {i} ---")
    print(df)
