

import pandas as pd
import glob

def merge_csv_by_key(folder_path, key_column, output_file):
    
    csv_files = glob.glob(folder_path + "/*.csv")
    
    
    merged_df = pd.read_csv(csv_files[0])
    
    
    for file in csv_files[1:]:
        df = pd.read_csv(file)
        merged_df = pd.merge(merged_df, df, on=key_column, how='outer')
    
    
    merged_df.to_csv(output_file, index=False)
    print(f"✅ Merged CSV saved successfully as: {output_file}")


if __name__ == "__main__":
    folder = "csv_files"       # Folder containing CSVs
    key = "id"                 # Common column to merge on
    output = "merged_output.csv"
    
    merge_csv_by_key(folder, key, output)
