import pandas as pd
import os
import numpy as np

# Configuration
DATA_DIR = './data/raw_dataset'
OUTPUT_DIR = './data/processed/initially_cleaned_dataset'
FILES = ['application_data.csv', 'previous_application.csv']

def clean_application_data(df):
    """
    Specific cleaning logic for application_data.csv
    """
    print("  Applying application_data specific cleaning...")
    
    # 1. Handle magic numbers in DAYS_EMPLOYED
    # 365243 days is often used as a magic number for "Not Available" or "Pensioner"
    if 'DAYS_EMPLOYED' in df.columns:
        df['DAYS_EMPLOYED'] = df['DAYS_EMPLOYED'].replace(365243, np.nan)

    # 2. Convert DAYS_ columns to absolute values
    days_cols = [col for col in df.columns if 'DAYS_' in col]
    for col in days_cols:
         df[col] = df[col].abs()
         
    # 3. Handle XNA in categorical columns
    # Example: CODE_GENDER, ORGANIZATION_TYPE might have XNA
    # Specific categorical cleanup
    if 'CODE_GENDER' in df.columns:
        df['CODE_GENDER'] = df['CODE_GENDER'].replace('XNA', np.nan)
        
    if 'NAME_FAMILY_STATUS' in df.columns:
        df['NAME_FAMILY_STATUS'] = df['NAME_FAMILY_STATUS'].replace('Unknown', np.nan)
        
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = df[col].replace('XNA', np.nan)
        
    return df

def clean_previous_application(df):
    """
    Specific cleaning logic for previous_application.csv
    """
    print("  Applying previous_application specific cleaning...")
    
    # 1. Handle magic numbers in DAYS_ columns
    # 365243 is common in previous_application too
    days_cols = [col for col in df.columns if 'DAYS_' in col]
    for col in days_cols:
        df[col] = df[col].replace(365243, np.nan)
        df[col] = df[col].abs()
        
    # 2. Handle XNA/XAP in categorical columns
    if 'NAME_PAYMENT_TYPE' in df.columns:
        df['NAME_PAYMENT_TYPE'] = df['NAME_PAYMENT_TYPE'].replace('XNA', np.nan)

    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
         df[col] = df[col].replace(['XNA', 'XAP'], np.nan)

    return df

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
    
    # 2. Specific Cleaning
    if file_name == 'application_data.csv':
        df = clean_application_data(df)
    elif file_name == 'previous_application.csv':
        df = clean_previous_application(df)

    # Save cleaned data
    output_path = os.path.join(OUTPUT_DIR, file_name)
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for file_name in FILES:
        clean_data(file_name)
    print("Data cleanup complete.")
