import pandas as pd

data = [
    {"Name": "Anu", "Age": 25, "City": "Chennai"},
    {"Name": "Riya", "Age": 30, "City": "Bangalore"},
    {"Name": "Karthik", "Age": 22, "City": "Chennai"},
    {"Name": "Sanjay", "Age": 28, "City": "Mumbai"},
]

df = pd.DataFrame(data)
filtered_df = df[df["City"] == "Chennai"]
filtered_df.to_excel("filtered_data.xlsx", index=False)

print("Filtered data exported to 'filtered_data.xlsx'")
