# **Data Visualization Project - Team Technerds**


# **1. Project Overview**

This project aims to analyze and visually explore factors influencing loan repayment behavior for a finance company operating in urban regions. The goal is to help the company better identify trustworthy applicants, reduce defaults, and strengthen the credit evaluation process.

The analysis is conducted using three datasets:

* **application_data.csv** – Client-level information recorded during loan application.
* **previous_application.csv** – History of earlier applications and their approval outcomes.
* **columns_description.csv** – Metadata dictionary explaining all variables.

The final outcomes include structured EDA, feature engineering, insights, and a foundation for an interactive dashboard.

---

# **2. Data Understanding & Initial Assessment**

### **2.1 Structure of Datasets**

* **Application Data:** Contains demographic details, financial attributes, employment information, credit status, and target variable (default or not).
* **Previous Application Data:** Records of each applicant's past loans, including approval status and payment behavior.
* **Data Dictionary:** Describes each column, its meaning, and units.

### **2.2 Key Variables of Interest**

* **TARGET** (0 = Non-Default, 1 = Default)
* **DAYS_BIRTH**, **DAYS_EMPLOYED**, **AMT_INCOME_TOTAL**, **AMT_CREDIT**, **AMT_ANNUITY**, **NAME_EDUCATION_TYPE**, **NAME_INCOME_TYPE**
* **Credit history, loan purpose, repayment timelines, contract types**

### **2.3 Data Quality Checks**

Performed initial checks for:

* Missing values
* Outliers (income, credit, annuity)
* Data type mismatches
* Incorrect entries (e.g., huge negative values)
* Duplicates

---

# **3. Data Cleaning**

### **3.1 Handling Missing Values**

* Columns with more than **40% missing values** were flagged for removal.
* Columns with moderate missing values were imputed based on:

  * **Median/mean** for numerical columns.
  * **Mode** for categorical variables.
  * Domain logic where applicable (e.g., unknown address → "Not Provided").

### **3.2 Treating Infinite and Anomalous Values**

* Variables like **DAYS_EMPLOYED** contained extremely high positive values (indicative of anomalies). These were replaced after examination.
* Negative duration values (e.g., birth and employment) were converted into positive years.

---

# **4. Feature Engineering**

Feature engineering plays a central role in understanding repayment behavior.

### **4.1 Creating Derived Variables**

#### **4.1.1 Age Calculation**

```python
applications['AGE_AT_LOAN'] = -round(applications['DAYS_BIRTH'] / 365).astype(int)
```

Converted negative day counts into positive age in years.

#### **4.1.2 Employment Duration**

```python
applications['JOB_AGE_AT_LOAN'] = -round(applications['DAYS_EMPLOYED'] / 365).astype(int)
```

Identified applicants with long stable jobs vs. unstable employment.

#### **4.1.3 Registration Duration**

```python
applications['DAYS_REGISTRATION'] = -round(applications['DAYS_REGISTRATION'] / 365)
```

Helps evaluate residence stability.

### **4.2 Financial Ratios**

Derived features for risk analysis:

* **Income-to-Credit Ratio**
* **Credit-to-Annuity Ratio**
* **Payment Difficulty Score** (e.g., credit amount divided by income)

### **4.3 Categorical Grouping**

Categories merged to simplify analysis:

* Education Levels (e.g., "Basic School" combined categories)
* Occupation and Income Types

---

# **5. Exploratory Data Analysis (EDA)**

EDA was conducted to uncover loan repayment patterns.

### **5.1 Target Variable Distribution**

* Majority of applicants are **non-defaulters (TARGET = 0)**.
* A significant minority fall into **default (TARGET = 1)** category.

### **5.2 Demographic Insights**

* Younger applicants show slightly higher risk.
* Longer employment history generally correlates with lower default.

### **5.3 Financial Insights**

* High credit amounts without proportional income increase default likelihood.
* Applicants allocating a large portion of income to annuity payments show higher risk.

### **5.4 Past Loan Behavior**

Cross-check with *previous_application.csv* revealed:

* Rejected past applications → higher probability of current default.
* Previous late payments strongly signal risk.

---

# **6. Analysis Methods Used**

### **6.1 Univariate Analysis**

* Distribution plots (histograms, box plots)
* Categorical frequency charts

### **6.2 Bivariate Analysis**

* Grouped bar charts (e.g., Income Type vs TARGET)
* Scatter plots (Income vs Credit)
* Correlation matrices

### **6.3 Multivariate Analysis**

* Heatmaps for relationship visualization
* Pairwise feature interactions to detect clusters

### **6.4 Risk Segmentation**

Applicants grouped based on:

* Income bracket
* Employment stability
* Credit burden
* Previous loan outcomes

---

# **7. Key Findings**

### **7.1 High-Risk Indicators**

* Low income + high credit demand
* Short employment duration
* Past loan rejections
* Higher number of children
* Lower education level

### **7.2 Low-Risk Indicators**

* Stable job history
* High income-to-credit ratio
* Clean previous credit record
* Long residence history

### **7.3 Most Important Segments**

* **Young applicants** (early 20s–30s)
* **Applicants with inconsistent job history**
* **Applicants previously rejected for loans**

---

# **8. Visualization Outputs (Python)**

The following charts were generated:

* **Distribution of TARGET variable**
* **Age group vs default rate**
* **Income distribution by TARGET**
* **Credit amount and annuity scatter relationship**
* **Previous application status vs default**

These visual outputs form the base for the upcoming Power BI dashboard.

---

# **9. Dashboard Plan (Power BI - To Be Done)**

Planned visuals:

* Risk heatmap
* Customer segmentation matrix
* Default vs Non-Default trends
* KPI cards (Default Rate, Avg Income, Avg Loan Amount)
* Drilldowns for demographic filters

---

# **10. Conclusion**

Through data cleaning, feature engineering, and exploratory analysis, the project identifies key behavioral and financial indicators linked to loan default. These insights will guide the finance company in improving its credit evaluation model and risk screening process.

Next steps involve building an interactive Power BI dashboard and preparing a final presentation summarizing insights for stakeholders.
