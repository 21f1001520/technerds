import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set plot style
sns.set_theme(style="whitegrid")

DATA_DIR = 'data'
OUTPUT_DIR = 'output'
APP_DATA_PATH = os.path.join(DATA_DIR, 'application_data.csv')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_data():
    print("Loading data...")
    df = pd.read_csv(APP_DATA_PATH)
    return df

def plot_target_distribution(df):
    plt.figure(figsize=(6, 4))
    sns.countplot(x='TARGET', data=df)
    plt.title('Distribution of Target Variable (0: Non-Default, 1: Default)')
    plt.savefig(os.path.join(OUTPUT_DIR, 'target_distribution.png'))
    plt.close()
    print("Saved target_distribution.png")

def plot_missing_values(df):
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    missing_percent = (missing / len(df)) * 100
    missing_percent = missing_percent.sort_values(ascending=False)
    
    plt.figure(figsize=(12, 6))
    missing_percent.head(20).plot(kind='bar')
    plt.title('Top 20 Columns with Missing Values (%)')
    plt.ylabel('Percentage Missing')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'missing_values.png'))
    plt.close()
    print("Saved missing_values.png")

def plot_numerical_distributions(df):
    cols = ['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY']
    for col in cols:
        if col in df.columns:
            plt.figure(figsize=(10, 5))
            sns.histplot(df[col].dropna(), kde=True, bins=50)
            plt.title(f'Distribution of {col}')
            plt.savefig(os.path.join(OUTPUT_DIR, f'dist_{col}.png'))
            plt.close()
            print(f"Saved dist_{col}.png")
            
            # Boxplot for outliers
            plt.figure(figsize=(10, 2))
            sns.boxplot(x=df[col].dropna())
            plt.title(f'Boxplot of {col}')
            plt.savefig(os.path.join(OUTPUT_DIR, f'boxplot_{col}.png'))
            plt.close()

def plot_categorical_analysis(df):
    cols = ['NAME_CONTRACT_TYPE', 'CODE_GENDER', 'NAME_EDUCATION_TYPE']
    for col in cols:
        if col in df.columns:
            plt.figure(figsize=(10, 5))
            sns.countplot(y=col, data=df, order=df[col].value_counts().index)
            plt.title(f'Count of {col}')
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, f'count_{col}.png'))
            plt.close()
            print(f"Saved count_{col}.png")

            # Default rate by category
            plt.figure(figsize=(10, 5))
            default_rates = df.groupby(col)['TARGET'].mean().sort_values(ascending=False)
            sns.barplot(x=default_rates.values, y=default_rates.index)
            plt.title(f'Default Rate by {col}')
            plt.xlabel('Default Rate')
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, f'default_rate_{col}.png'))
            plt.close()

def main():
    df = load_data()
    
    plot_target_distribution(df)
    plot_missing_values(df)
    plot_numerical_distributions(df)
    plot_categorical_analysis(df)
    
    print("EDA completed. Plots saved to 'output' directory.")

if __name__ == "__main__":
    main()
