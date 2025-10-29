# ETL Script: Extract CSV → Transform → Load to SQLite

import pandas as pd
import sqlite3

# Step 1: Extract (read CSV)
csv_file = "sample_data.csv"  # Replace with your CSV file
df = pd.read_csv(csv_file)
print("Original Data:")
print(df)

# Step 2: Transform
# Example transformations:
# - Rename columns
# - Filter rows (Age > 25)
# - Create new column

df = df.rename(columns={"Name": "FullName"})
df = df[df["Age"] > 25]
df["AgeGroup"] = df["Age"].apply(lambda x: "Adult" if x >= 18 else "Young")

print("\nTransformed Data:")
print(df)

# Step 3: Load into SQLite
conn = sqlite3.connect("etl_output.db")  # SQLite database
df.to_sql("people", conn, if_exists="replace", index=False)
conn.close()

print("\nData successfully loaded into 'etl_output.db' (table: people).")
