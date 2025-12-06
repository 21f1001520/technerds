import pandas as pd
import os
import numpy as np

# Configuration
DATA_DIR = './data'
OUTPUT_DIR = './data/processed/cleaned'
FILES = ['application_data.csv', 'previous_application.csv']

def clean_data(file_name):
    print(f"Processing {file_name}...")
    file_path = os.path.join(DATA_DIR, file_name)
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    initial_shape = df.shape
    print(f"Initial shape: {initial_shape}")

    # 1. Deduplication
    df.drop_duplicates(inplace=True)
    dedup_shape = df.shape
    if initial_shape != dedup_shape:
        print(f"Dropped {initial_shape[0] - dedup_shape[0]} duplicate rows.")

    # 2. Handling Missing Values
    # Separate numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns

    # Impute numeric with median
    for col in numeric_cols:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
    
    # Impute categorical with mode
    for col in categorical_cols:
        if df[col].isnull().any():
            if not df[col].mode().empty:
                mode_val = df[col].mode()[0]
                df[col] = df[col].fillna(mode_val)
            else:
                df[col] = df[col].fillna("Unknown")

    print(f"Missing values handled.")

    # Save cleaned data
    output_path = os.path.join(OUTPUT_DIR, file_name)
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for file_name in FILES:
        clean_data(file_name)
    print("Data cleanup complete.")
