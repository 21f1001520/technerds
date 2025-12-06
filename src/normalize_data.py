import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

# Configuration
INPUT_DIR = './data/processed/cleaned'
OUTPUT_DIR = './data/processed/normalized'
FILES = ['application_data.csv', 'previous_application.csv']

def normalize_data(file_name):
    print(f"Normalizing {file_name}...")
    file_path = os.path.join(INPUT_DIR, file_name)
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run cleanup script first.")
        return

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    # Select numerical columns
    # Exclude IDs, Target, and Flags
    exclude_cols = ['TARGET', 'SK_ID_CURR', 'SK_ID_PREV']
    exclude_prefixes = ('FLAG_', 'NFLAG_', 'REG_', 'LIVE_')
    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    cols_to_scale = [c for c in numeric_cols 
                     if c not in exclude_cols 
                     and not c.startswith(exclude_prefixes)]

    if not cols_to_scale:
        print("No numerical columns to scale.")
    else:
        scaler = MinMaxScaler()
        df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])
        print(f"Scaled {len(cols_to_scale)} columns.")

    # Save normalized data
    output_path = os.path.join(OUTPUT_DIR, file_name)
    df.to_csv(output_path, index=False)
    print(f"Saved normalized data to {output_path}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for file_name in FILES:
        normalize_data(file_name)
    print("Data normalization complete.")
