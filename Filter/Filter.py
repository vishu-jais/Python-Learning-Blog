# A Python program to filter data and export it to Excel

import pandas as pd

# Sample data: list of dictionaries
data = [
    {"Name": "Anu", "Age": 25, "City": "Chennai"},
    {"Name": "Riya", "Age": 30, "City": "Bangalore"},
    {"Name": "Karthik", "Age": 22, "City": "Chennai"},
    {"Name": "Sanjay", "Age": 28, "City": "Mumbai"},
]

# Convert data to DataFrame
df = pd.DataFrame(data)

# Filter data: only people from Chennai
filtered_df = df[df["City"] == "Chennai"]

# Export filtered data to Excel
filtered_df.to_excel("filtered_data.xlsx", index=False)

print("Filtered data exported to 'filtered_data.xlsx'")
