import pandas as pd
import os

DATA_DIR = 'data/raw_dataset'
APP_DATA_PATH = os.path.join(DATA_DIR, 'application_data.csv')
PREV_APP_PATH = os.path.join(DATA_DIR, 'previous_application.csv')
COL_DESC_PATH = os.path.join(DATA_DIR, 'columns_description.xlsx')

def inspect_file(filepath, description):
    print(f"--- Inspecting {description} ---")
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None
    
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        print(f"Unsupported file format: {filepath}")
        return None

    print(f"Shape: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nInfo:")
    print(df.info())
    print("\nMissing Values (Top 10):")
    print(df.isnull().sum().sort_values(ascending=False).head(10))
    print("\nDuplicates:", df.duplicated().sum())
    return df

def main():
    print("Starting Data Inspection...")
    
    # Inspect Application Data
    app_df = inspect_file(APP_DATA_PATH, "Application Data")
    
    # Inspect Previous Application Data
    prev_app_df = inspect_file(PREV_APP_PATH, "Previous Application Data")
    
    # Inspect Column Descriptions
    col_desc_df = inspect_file(COL_DESC_PATH, "Column Descriptions")

    if app_df is not None:
        print("\n--- Target Variable Distribution (Application Data) ---")
        if 'TARGET' in app_df.columns:
            print(app_df['TARGET'].value_counts(normalize=True))
        else:
            print("TARGET column not found in Application Data")
    
    if prev_app_df is not None:
        print("\n--- Target Variable Distribution (Previous Application Data) ---")
        if 'TARGET' in prev_app_df.columns:
            print(prev_app_df['TARGET'].value_counts(normalize=True))
        else:
            print("TARGET column not found in Previous Application Data")
    
    if col_desc_df is not None:
        print("\n--- Column Descriptions ---")
        print(col_desc_df)

if __name__ == "__main__":
    main()
