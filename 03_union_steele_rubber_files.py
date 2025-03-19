import pandas as pd
import glob
import os

# Set file directory
directory = 'Steele Rubber Image URLs'

def union_csv_files(directory, output_filename="steele_rubber_auto_parts_image_urls.csv"):
    all_filenames = glob.glob(os.path.join(directory, "*.csv"))
    all_df = []
    
    for f in all_filenames:
        df = pd.read_csv(f)
        df["File"] = os.path.basename(f)
        df["Make"] = df["File"].str.replace("image_urls_", "").str.replace(".csv", "").str.replace("-", " ")
        all_df.append(df)
    
    combined_df = pd.concat(all_df, ignore_index=True)
    combined_df = combined_df.drop(columns=["File"]) 
    combined_df.to_csv(output_filename, index=False)
    print(f"Successfully combined all CSV files in '{directory}' to '{output_filename}'")

# Example usage:
directory_path = directory
union_csv_files(directory_path)

union_csv_files(directory, output_filename="steele_rubber_auto_parts_image_urls.csv")
