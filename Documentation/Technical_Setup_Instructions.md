
# Technical Setup Instructions

To set up and run this Data Visualization Project, follow these steps to ensure a smooth execution. This guide assumes you have Python installed on your system (version 3.8 or higher recommended) and access to a Jupyter Notebook environment.

### **1. Clone the Repository**
Clone the project repository from GitHub to your local machine:

```
git clone https://github.com/21f1001520/technerds.git
cd technerds
```

This will download the project structure, including folders like `build`, `charts`, `data`, `output`, `src`, `week_1`, `week_2`, `week_3`, and files such as `LICENSE`, `pyproject.toml`, `README.md`, and `uv.lock`.

### **2. Install Required Libraries**
Install all the necessary libraries prior to running the code. These are based on the imports used in the project. Run the following command in your terminal or command prompt:

```
pip install pandas numpy regex math pathlib seaborn matplotlib plotly scikit-learn scipy
```

The key libraries include:
- `pandas` for data manipulation
- `numpy` for numerical computations
- `re` for regular expressions (standard library)
- `math` for mathematical functions (standard library)
- `pathlib` for file path handling (standard library)
- `seaborn` and `matplotlib` for static visualizations
- `plotly.express` for interactive plots
- `sklearn.preprocessing.LabelEncoder` for encoding categorical variables
- `scipy.stats` for statistical tests
- `sklearn.model_selection.train_test_split` for splitting datasets
- `sklearn.ensemble.RandomForestClassifier` for modeling
- `sklearn.metrics.roc_auc_score` for evaluation
- `warnings` to suppress warnings (standard library)

Additionally, set visualization styles in your code if needed:
```python
import warnings
warnings.filterwarnings('ignore')
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
```

### **3. Set Up Directory Structure**
Before running the notebook, create the required data directories to store raw, processed, and final datasets. Navigate to the project root and run the following commands (or create them manually):

```
mkdir data
cd data
mkdir raw_dataset
mkdir final_dataset
mkdir processed
cd processed
mkdir Feature-Engineered
mkdir initially_cleaned_dataset
cd ../..
```

This will result in the following structure under `data/`:
- `raw_dataset/` (for original datasets like `application_data.csv`, `previous_application.csv`, `columns_description.csv`)
- `final_dataset/` (for the assembled final dataset like `final_dataset.csv`)
- `processed/` 
  - `Feature-Engineered/` (for engineered files like `application_data.csv` and `previous_application.csv`)
  - `initially_cleaned_dataset/` (for initial cleaning outputs)

Place your raw datasets (e.g., `application_data.csv`, `previous_application.csv`, `columns_description.csv`) into `data/raw_dataset/` before proceeding.

### **4. Run the Notebook Step by Step**
The main code for data exploration, cleaning, feature engineering, analysis, and visualization is in `src/code.ipynb`. To run it:

1. Launch Jupyter Notebook:
   ```
   jupyter notebook
   ```
   Or use JupyterLab:
   ```
   jupyter lab
   ```

2. Open `src/code.ipynb` in your browser.

3. Execute the cells step by step:
   - **Initial Setup Cells**: Import libraries and set configurations (e.g., warnings, visualization styles).
   - **Data Loading Cells**: Load datasets from `data/raw_dataset/` using `pandas` (e.g., `pd.read_csv('data/raw_dataset/application_data.csv')`).
   - **Data Cleaning Cells**: Handle missing values, outliers, and anomalies (e.g., capping income, fixing `DAYS_EMPLOYED`).
   - **Exploratory Data Analysis (EDA) Cells**: Generate distributions, boxplots, and insights using `seaborn`, `matplotlib`, and `plotly` (e.g., target distribution, contract type counts).
   - **Feature Engineering Cells**: Create new features like ratios (`INCOME_TO_CREDIT_RATIO`), binaries (`HAS_CHILDREN`), and aggregates; save to `data/processed/Feature-Engineered/`.
   - **Merging and Final Assembly Cells**: Merge datasets, impute remaining misses, and export to `data/final_dataset/final_dataset.csv`.
   - **Deep Analysis Cells**: Perform univariate, bivariate, multivariate analysis; correlation heatmaps; outlier detection; feature importance with RandomForestClassifier; risk scoring.
   - **Visualization Cells**: Generate plots and save them to `output/` or `charts/Analysis/` (e.g., histograms, countplots, default rate by quintiles).

   Run each cell sequentially, checking outputs for errors. The notebook assumes the directory structure is set up as described. If issues arise (e.g., file not found), verify paths and dataset placement.

After running, the processed files, final dataset, and visualizations will be generated in the respective folders. This sets the foundation for the Power BI dashboard.

# **Contact Us**
For questions, collaborations, or further details, please reach out our Team Technerds members:

* Name: Shib Kumar Saraf
* Email: 21f1001520@ds.study.iitm.ac.in

* Name: Suraaj Jain
* Email: 22f3002242@ds.study.iitm.ac.in

* Name: Supreeth Rao
* Email: 21f1002726@ds.study.iitm.ac.in

* Name: Kanishk Kumar
* Email: 22f1000386@ds.study.iitm.ac.in
