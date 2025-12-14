# **Data Visualization Project - Team Technerds**

# **1. Project Overview**
This project aims to analyze and visually explore factors influencing loan repayment behavior for a finance company operating in urban regions. The goal is to help the company better identify trustworthy applicants, reduce defaults, and strengthen the credit evaluation process.

The analysis is conducted using three datasets:
* **application_data.csv** – Client-level information recorded during loan application.
* **previous_application.csv** – History of earlier applications and their approval outcomes.
* **columns_description.csv** – Metadata dictionary explaining all variables.

The final outcomes include structured EDA, feature engineering, insights, and a foundation for an interactive dashboard.

---

# **Data Exploration, Cleaning & Initial Insights**

## **1. Business Understanding**
### **Business Goal**
The primary objective is to minimize financial losses from loan defaults while maximizing the approval of creditworthy applicants. By analyzing historical loan application data, we aim to identify key indicators of default risk. This will enable the credit team to refine their approval criteria, implement risk-based pricing, or flag high-risk applications for manual review.

### **Key Analysis Questions**
1. **What are the defining characteristics of applicants who default versus those who repay?** (Demographics, Income, Employment)
2. **How does financial stability (Income, Credit Amount, Annuity) correlate with default risk?**
3. **Are there specific loan types or contract terms associated with higher default rates?**
4. **How does previous loan history influence current application performance?**
5. **What data quality issues (missing values, outliers) need to be addressed before modeling?**

## **2. Data Structure & Quality Assessment**
### **Dataset Overview**
- **Application Data**: Contains client-level information for current loan applications.
    - *Shape*: (307,511 rows, 122 columns)
    - *Target Variable*: `TARGET` (1 = Default, 0 = Repaid)
   
    ![Target Distribution](./output/target_distribution.png)
- **Previous Application Data**: History of previous loans for the same clients.
    - *Shape*: (1,670,214 rows, 37 columns)
- **Column Descriptions**: Metadata explaining the features.

### **Data Quality Issues**
- **Missing Values**:
    - Significant missing data in several columns. Top missing columns include housing-related information (e.g., `COMMONAREA_AVG`, `NONLIVINGAPARTMENTS_AVG`) and external source scores.
    - *Action*: We will need to decide on imputation strategies (median, mode, or creating a "missing" category) or drop columns with excessive missingness (>50%) if they lack predictive power.
   
    ![Missing Values](./output/missing_values.png)
- **Outliers**:
    - **Income**: `AMT_INCOME_TOTAL` shows extreme outliers (e.g., max value is likely an error or a very high-net-worth individual). These will need capping or log-transformation.
   
    ![Income Distribution](./output/dist_AMT_INCOME_TOTAL.png)
    ![Income Boxplot](./output/boxplot_AMT_INCOME_TOTAL.png)
    - **Days Employed**: There are anomalous values (e.g., 365243) which likely represent a placeholder for "unemployed" or "pensioner". This needs to be cleaned.

## **3. Initial Exploratory Insights**
### **Borrower Profiles & Default Proportions**
- **Target Distribution**: The vast majority of loans are repaid. The 8% default rate is the critical minority we need to characterize.
- **Contract Type**:
    - *Cash Loans*: Make up the majority of applications.
    - *Revolving Loans*: Have a lower volume but potentially different risk profile.
   
    ![Contract Type Count](./output/count_NAME_CONTRACT_TYPE.png)
    ![Contract Type Default Rate](./output/default_rate_NAME_CONTRACT_TYPE.png)
- **Gender**:
    - Females tend to apply more frequently than males.
    - *Insight*: Initial checks suggest males might have a slightly higher default rate (to be confirmed with statistical tests).
   
    ![Gender Count](./output/count_CODE_GENDER.png)
    ![Gender Default Rate](./output/default_rate_CODE_GENDER.png)
- **Education**:
    - Applicants with "Secondary / secondary special" education are the most common.
    - *Insight*: Higher education levels generally correlate with lower default rates.
   
    ![Education Count](./output/count_NAME_EDUCATION_TYPE.png)
    ![Education Default Rate](./output/default_rate_NAME_EDUCATION_TYPE.png)
- **Financials**:
    - **Credit Amount**: Distribution is right-skewed. Most loans are for smaller amounts, but there is a long tail of high-value loans.
    - **Income**: Highly skewed. Most applicants have low to medium income.
   
    ![Credit Distribution](./output/dist_AMT_CREDIT.png)
    ![Annuity Distribution](./output/dist_AMT_ANNUITY.png)


### **Initial Observations Summary**
The data holds strong potential for predictive modeling but requires significant cleaning. The class imbalance is a major factor to consider. Key risk drivers appear to be education level, gender, and potentially the type of loan contract. The `EXT_SOURCE` variables (external credit scores) are likely to be strong predictors and should be prioritized despite missing values.

---

# **Feature Engineering**

## **Overview**
This feature engineering process was applied to the `application_data.csv` and `previous_application.csv` datasets. The objective was to transform initially cleaned data into a concise, interpretable set of features that effectively capture borrower profiles, loan characteristics, and historical repayment behavior.

The process included domain-driven transformations, ratio calculations, time conversions, and careful aggregation of historical records. The resulting final dataset contains 307,511 observations and 68 columns, with no missing values and a preserved default rate of 8.073%. This engineered dataset is optimized for exploratory analysis, risk segmentation, and interactive visualization in Power BI.

## **1. Feature Engineering on Application Data**
The engineered `application_data` dataset was reduced from 122 to approximately 52 columns through targeted transformations and selections. Key engineered features include:
- **AGE_AT_LOAN**: Age of the applicant in years at the time of loan application (derived from |DAYS_BIRTH| / 365.25). Provides an intuitive demographic variable for segmentation and correlation analysis with repayment behaviour.
- **JOB_AGE_AT_LOAN**: Years employed at the current job (derived from |DAYS_EMPLOYED| / 365.25, with anomalies flagged). Captures employment stability, a strong indicator of repayment capacity.
- **REG_AGE_AT_LOAN**, **ID_PUBLISH_AGE_AT_LOAN**, **PHONE_AGE_AT_LOAN**: Years since registration, ID update, and phone change, respectively. Reflect potential life changes or data freshness relevant to risk assessment.
- **INCOME_TO_CREDIT_RATIO**: Total income divided by loan credit amount. Measures the applicant's ability to service the requested credit.
- **ANNUITY_TO_INCOME_RATIO**: Monthly annuity divided by total income. Indicates monthly repayment burden relative to income.
- **CREDIT_TERM_MONTHS**: Estimated loan term in months (AMT_CREDIT / AMT_ANNUITY). Summarises loan duration for comparative analysis.
- **INCOME_PER_FAMILY_MEMBER**: Income divided by family size (including applicant). Adjusts income for household dependencies.
- **HAS_CHILDREN**: Binary indicator of presence of children. Enables direct segmentation by family structure.
- **HAS_CAR_AND_REALTY**: Binary indicator of owning both a car and real estate. Serves as a proxy for overall asset ownership and financial stability.
- **AVG_APARTMENTS_BUILDING**: Mean of normalised building information features (e.g., apartment size, basement area). Consolidates multiple related housing metrics into a single interpretable score.
- **EXT_SCORES_AVG**: Average of the three external data source scores (EXT_SOURCE_1, 2, 3). Provides a robust composite external risk signal.
- **TOTAL_DOCS_SUBMITTED**: Sum of document submission flags (FLAG_DOCUMENT_3 to 21). Quantifies completeness of application documentation.

Irrelevant or redundant columns (e.g., individual contact flags) were removed to reduce dimensionality while retaining predictive and explanatory power.

The processed file was saved as `application_data.csv` in `data/processed/Feature-Engineered/`.

## **2. Feature Engineering on Previous Application Data**
Historical records from `previous_application.csv` (originally >1.6 million rows) were aggregated to the customer level (SK_ID_CURR), resulting in 16 derived features per applicant. Only columns with strong behavioural signals were retained prior to aggregation.

Key engineered features include:
- **PREV_TOTAL_APPS**: Total number of previous applications. Indicates application frequency and potential credit-seeking behaviour.
- **PREV_APPROVED_COUNT** and **PREV_APPROVAL_RATE**: Count and proportion of previously approved applications. Higher approval rates suggest consistent creditworthiness.
- **PREV_REFUSED_COUNT** and **PREV_REFUSAL_RATE**: Count and proportion of previously refused applications. Elevated refusal rates signal elevated historical risk.
- **PREV_AVG_LOAN_AMT**, **PREV_TOTAL_LOAN_AMT**, **PREV_MAX_LOAN_AMT**: Average, cumulative, and maximum credit amounts from past approved loans. Reflect historical borrowing scale and exposure.
- **PREV_AVG_OVERASK**: Average difference between requested and granted amounts (AMT_APPLICATION – AMT_CREDIT). Positive values indicate tendency to over-request, potentially reflecting optimism or financial strain.
- **PREV_AVG_DOWNPAYMENT_PCT**: Average down payment as a percentage of granted credit. Higher values demonstrate greater upfront commitment and financial capacity.
- **PREV_MOST_RECENT_APP_YEARS** and **PREV_AVG_YEARS_AGO**: Years since the most recent and average previous application (derived from |DAYS_DECISION| / 365.25). Capture recency and overall activity timeline.
- **PREV_AVG_LOAN_TERM_MONTHS**: Average contractual loan term in months. Indicates preference for short- or long-term financing.
- **PREV_PCT_CONSUMER_LOANS**: Proportion of past loans classified as consumer loans. Distinguishes consumption-driven borrowing patterns.
- **PREV_PCT_WITH_INSURANCE**: Proportion of past loans with optional insurance taken. May reflect risk awareness or financial prudence.

Applicants with no previous applications received zero values across all features, preserving the full cohort size.

The processed file was saved as `previous_application.csv` in `data/processed/Feature-Engineered/`.

## **3. Final Dataset Assembly**
The engineered application and previous-application datasets were merged on `SK_ID_CURR` using a left join. Remaining missing values in previous-application features were imputed with zeros (no history) and, where necessary, medians for numerical columns and modes for categorical columns.

The final dataset comprises 307,511 rows and 68 columns, maintaining the original target distribution (default rate 8.073%) and containing no missing values.

The dataset was exported as `final_dataset.csv` in `data/final_dataset/` for direct use in Power BI dashboard development and presentation materials.

This engineered dataset provides a clean, compact, and domain-aligned foundation for identifying risk patterns, segmenting borrower profiles, and constructing the required interactive risk dashboard.

---

# **Deep Analysis, Feature Validation & Risk Attribution**
This document presents a **highly detailed, deep exploratory and validation analysis** performed on the finalized dataset. The purpose is intentionally not model optimization, but **deep explainability and risk understanding** — clearly articulating *why* applicants default, *which financial, behavioral, and demographic signals matter most*, *how these signals interact*, and *how each analytical finding directly translates into actionable credit policy and business decisions*.

---

## **1. Final Dataset Overview**
**Dataset Location**
```text
data/final_dataset/final_dataset.csv
```

**Granularity**
* One row represents one loan application
* One-to-one mapping with unique applicant ID (`SK_ID_CURR`)

**Target Variable**
* `TARGET = 1` → Client defaulted
* `TARGET = 0` → Client fully repaid or Not defaulted

**Why this matters**
All downstream analysis, modeling, and dashboards rely on this dataset as the *single source of truth*. Ensuring clarity at this stage prevents data leakage and misinterpretation later.

---

## **2. Feature Landscape & Grouping**
To improve interpretability and avoid analytical bias, features are logically grouped before analysis.

### **2.1 Numerical Features**
Numerical features represent **continuous risk signals** related to affordability, stability, and credit behavior.
Examples include:
* `AGE_AT_LOAN` – borrower maturity and life-stage stability
* `CREDIT_INCOME_RATIO` – repayment burden relative to income
* `ANNUITY_INCOME_RATIO` – monthly cash-flow stress
* `EXT_SOURCE_MEAN` – external credit bureau assessment
* `PREV_REFUSAL_RATE` – historical rejection behavior

**Analytical Focus**:
* Distribution shape (skewness, concentration)
* Outlier behavior
* Relationship with default probability

---

### **2.2 Categorical Features**
Categorical features capture **structural and demographic context**.
Examples include:
* `CODE_GENDER`
* `NAME_CONTRACT_TYPE`
* `EDU_SIMPLIFIED`
* `ORGANIZATION_TYPE`

**Analytical Focus**:
* Frequency imbalance
* Category-level default concentration
* Statistical dependency with TARGET

---

## **3. Data Quality & Target Structure**
### **3.1 Target Distribution**
![Target Distribution](./output/target_distribution.png)

**What this plot shows**:
* A strong class imbalance with defaults forming a small minority

**Why this matters**:
* Accuracy alone is misleading
* Requires stratified sampling, ROC-AUC, and class weighting
* Reflects real-world credit portfolios

---

## **4. Univariate Analysis: Understanding Individual Signals**
Univariate analysis focuses on **isolating each feature independently** to understand its natural distribution, stability, and inherent risk signal *before* considering interactions. This step is critical in credit risk because misleading distributions or extreme skewness can silently distort downstream models if not properly understood.

Univariate analysis helps answer: *What does a typical applicant look like?*

---

### **4.1 Numerical Feature Distributions**
Each numerical feature is analyzed using **two complementary visualizations** to capture both central tendency and extreme behavior:
For each numerical feature:
* **Histogram + KDE** → overall distribution and skewness
* **Boxplot** → outliers and variability

**Typical Observations**:
* Income and loan amounts are heavily right-skewed
* Ratio features show tighter, more informative distributions
* Extreme values exist but are economically plausible

**Why this matters**:
* Guides transformations (log, capping)
* Prevents models from overfitting noise

Plots saved as:
```text
{feature}_histogram.png
{feature}_boxplot.png
```

---

### **4.2 Categorical Feature Distributions**
![Categorical Distribution Example](./charts/Analysis/CODE_GENDER_Countplot.png)

**What this plot shows**:
* Relative frequency of each category

**Key Insight**:
* Some categories dominate volume but not necessarily risk
* Rare categories can carry disproportionate default rates

**Business Relevance**:
Volume ≠ Risk. Credit decisions must consider both.

---

## **5. Bivariate Analysis: Features vs Default**
This section explains *how each feature behaves differently for defaulters vs non-defaulters*.

---

### **5.1 Numerical Features vs TARGET**
This analysis compares how numerical feature values differ **between defaulters and non-defaulters**, helping determine whether a variable merely describes customers or truly differentiates risk outcomes.

![Age vs Target](./charts/Analysis/countplot_AGE_AT_LOAN_vs_target.png)

**What this plot shows**:
* Distribution of borrower age across default outcomes

**Insight**:
* Younger applicants show higher default concentration
* Risk decreases with age up to a stability plateau

**Business Interpretation**:
Age acts as a proxy for income stability and credit maturity.

---

### **5.2 Categorical Features vs TARGET**
![Education vs Target](./charts/Analysis/countplot_EDU_SIMPLIFIED_vs_target.png)

**What this plot shows**:
* Default proportion within each education category

**Statistical Validation**:
* Chi-square tests confirm dependency
* Observed differences are statistically meaningful

**Business Interpretation**:
Education level indirectly reflects earning stability and employment quality.

---

## **6. Correlation Analysis**
### **6.1 Full Correlation Heatmap**
Correlation analysis is used here **strictly as a diagnostic tool**, not as a feature selection mechanism. In credit risk, strong linear correlations are rare; therefore, weak correlations do not imply irrelevance.

![Correlation Heatmap](./charts/Analysis/Correlation%20Heatmap.png)

**What this shows**:
* Linear relationships between all numerical variables

**Key Observation**:
* Weak linear correlations are expected in credit risk
* Risk is driven by **non-linear interactions**

---

### **6.2 Correlation with TARGET**
**Risk-Increasing Signals**:
* `PREV_REFUSAL_RATE`
* `CREDIT_GOODS_RATIO`
* `AGE_AT_LOAN`

**Protective Signals**:
* External credit scores
* Income-normalized ratios

---

### **6.3 Focused Correlation Heatmap**
![Focused Correlation Heatmap](./charts/Analysis/Correlation%20Heatmap\(Heatmap%20of%20features%20strongly%20related%20to%20TARGET\).png)

**Insight**:
Only a limited subset shows linear signal — engineered features matter most.

---

## **7. Multivariate Analysis**
### **7.1 Average Default Rate by Category**
![Default Rate by Education](./charts/Analysis/Average_Default_Rate_by_EDU_SIMPLIFIED.png)

**What this shows**:
* Risk varies significantly within categories

**Why it matters**:
* Supports segmentation-based policy rules

---

### **7.2 Numerical Binning & Risk Trend**
![Default_Rate_by_Quintile_of_AGE_AT_LOAN](./charts/Analysis/Default_Rate_by_Quintile_of_AGE_AT_LOAN.png)
![Default_Rate_by_Quintile_of_AMT_ANNUITY](./charts/Analysis/Default_Rate_by_Quintile_of_AMT_ANNUITY.png)

**Insight**:
* Clear monotonic increase in default
* Validates ratio-based feature engineering

---

### **7.3 Interaction Analysis**
![Age Distribution by Gender and TARGET](./charts/Analysis/Age_Distribution_by_Gender_and_TARGET.png)

**What this reveals**:
* Gender alone is weak
* Gender *within age bands* modifies risk

**Modeling Implication**:
Supports interaction-aware models.

---

## **8. Outlier Analysis (IQR Method)**
**Approach**:
* Applied IQR on numerical variables only
* IDs and target excluded

**Findings**:
* Outliers concentrated in income and loan size
* Represent real but high-risk applicants

**Action**:
Outliers retained but handled via robust modeling.

---

## **9. Feature Importance Validation (Random Forest)**
This section validates all exploratory findings using a **tree-based, non-linear ensemble model**, ensuring that insights derived from EDA are not purely visual but hold predictive value in a supervised learning context.

![Top 20 Feature Importances](./charts/Analysis/Top%2020%20Most%20Important%20Features.png)

**Purpose**:
* Validate EDA insights using a non-linear model

**Top Drivers Identified**:
* `EXT_SOURCE_MEAN`
* `CREDIT_GOODS_RATIO`
* `AGE_AT_LOAN`
* `PREV_REFUSAL_RATE`
* `ANNUITY_INCOME_RATIO`

**Model Performance**:
* ROC-AUC: **0.7549**

**Interpretation**:
Strong discrimination for baseline risk validation.

---

## **10. Risk Scoring & BI Readiness**
Each application enriched with:
* `RISK_PROBA` – predicted default probability
* `RISK_SCORE` – scaled 0–1000 risk score

**Output File**
```text 
data/final_dataset/FINAL_DATASET_FOR_WITH_RISK_SCORE.csv
```

**Business Value**:
* Plug-and-play Power BI integration
* Enables thresholding, segmentation, and monitoring
---

## **Power BI Dashboard**

### **1. Overview Page**
The **Overview Page** serves as the executive summary for the credit risk analysis, providing a high-level snapshot of the loan portfolio's health, applicant demographics, and key risk indicators. It is designed to allow stakeholders to quickly gauge the magnitude of applications, identify the volume of "at-risk" loans, and filter data by key demographics.

Overview Dashboard ![Overview Dashboard](./PowerBi_dashboard/overview.jpg)
#### **Key Performance Indicators (KPIs)**
The top section highlights critical aggregate metrics:
* **Total Applications:** **307.51K** total loan requests processed.
* **Risk Associated Applications:** **25K** applications flagged as defaults (approx. 8% of total).
* **Previously Approved Customers:** **290.07K** applicants with a history of prior approvals.
* **Financial Scope:** A total annuity exposure of **8.34bn**, with an average per-capita family income of **93.11K**.

#### **Financial & Risk Ratios (Gauge Indicators)**
The second row visualizes critical financial health ratios that determine affordability and risk:
* **Average Annuity to Income Ratio (0.18):** On average, applicants spend 18% of their income on loan repayment, indicating a generally healthy affordability level.
* **Credit to Income Ratio (3.96):** The average loan size is nearly 4x the applicant's income.
* **Risk Percentage (0.08):** Confirms the overall portfolio default rate is steady at 8%.

#### **Interactive Filters**
The dashboard empowers users to slice the data dynamically using:
* **Age Slider:** Filters data for applicants aged **20 to 69**.
* **Loan Type:** Toggles between **Cash Loans** and **Revolving Loans**.
* **Demographic Dropdowns:** Allows filtering by **Application Type** and **Income Type**.

#### **Visual Insights & Breakdowns**
1.  **Default Trend by Age (Line Chart):**
    * *Chart:* "Defaulted Application according to age of applicant"
    * *Insight:* There is a distinct spike in defaults among younger applicants (peaking around late 20s to early 30s). As applicants age beyond 40, the number of defaults steadily declines, corroborating the EDA finding that older applicants generally display higher credit stability.

2.  **Defaults by Family Status (Bar Chart):**
    * *Chart:* "No. of Default Applications from different Family type"
    * *Insight:* **Married** applicants comprise the largest volume of defaults (**14.9K**), followed by **Single** (**4.5K**). *Note: While the volume is high for married individuals, this is likely driven by the fact that they make up the majority of the applicant pool.*

3.  **Annuity Distribution by Gender (Pie Chart):**
    * *Chart:* "Total Annuity Amount from different Genders"
    * *Insight:* **Females** account for the majority of the total annuity amount (**59.53%** or 4.96bn), compared to **Males** (**32.58%** or 2.72bn). This aligns with the observation that females apply for loans more frequently than males.

---
### **2. Previous Applications Distribution Dashboard**
This dashboard page shifts focus from the current applicant profile to their **historical banking behavior**. By analyzing the 1.4 million previous application records, this view helps the credit team understand the relationship between a customer's past loyalty (frequency of borrowing) and their current risk profile.

![Previous Applications Distribution Dashboard](./PowerBi_dashboard/previous_applciations_overview.jpg)

#### **Historical Volume & Operational Metrics (KPIs)**
The top header provides a summary of the operational scale and historical credit funnel:
* **Processing Volume:** **1.414M** previous applications have been processed in total.
* **Approval Volume:** **886K** of these applications were approved, indicating a historically active lending environment.
* **Customer Base:** These applications map back to **307.51K** unique customers.
* **Financial Average:** The average total loan amount per person historically stands at **902.69K**, with an average downpayment ratio of **0.09** (9%).

#### **Behavioral Ratios (Gauge Indicators)**
The second row visualizes the efficiency and nature of past lending:
* **Average Approval Rate (0.71):** Approximately 71% of past applications were approved, suggesting a moderately lenient historical approval policy.
* **Average Risk Ratio (0.08):** Consistent with the main overview, the historical risk ratio hovers at 8%.
* **Average Loan Duration (13.73 months):** Most historical loans were short-term, averaging just over 1 year.
* **Consumer Loans Ratio (0.55):** Over half (55%) of past lending activity was driven by consumer loans rather than cash loans.

#### **Key Visual Insight: The "Loyalty vs. Risk" Curve**
**Chart: Risk Ratio with Previous Applications Approved**
This combination chart is the centerpiece of the historical analysis, plotting **"Applications Approved"** (X-axis) against **"Total Loan Amount"** (Bars) and **"Risk Ratio"** (Line).

* **Loan Amount Trend (Bars):** There is a clear positive correlation between approval frequency and loan size. Customers with more approved applications (moving right on the X-axis) consistently secure higher total loan amounts, peaking near the 20-approval mark.
* **Risk Trend (Line):** The risk ratio (dark blue line) remains relatively stable between **6% and 8%** for customers with 1–15 past approvals. However, it shows volatility and a sharp decline for "super-borrowers" (20+ approvals), potentially indicating that highly frequent borrowers are either very safe or represent a distinct outlier segment.

#### **Interactive Filters**
This page allows for deep-diving into specific risk cohorts using:
* **Current Application Category:** Toggle between **Defaulted** and **Not Defaulted** to see if past history differs for current defaulters.
* **Approval Frequency Slider:** Filter for customers with a specific range of past approvals (e.g., 0 to 27).
* **Demographics:** Filters for **Gender** and **Age** allow for segmentation of historical trends.

---
### **3. Current Applications Distribution Dashboard**
This dashboard page focuses on the **sociodemographic profile** of the current applicant pool. Unlike the risk-centric views, this page is descriptive, helping the business understand *who* is applying for loans. It analyzes the distribution of applicants across gender, family status, asset ownership, and employment sectors.

![ Current Applications Distribution Dashboard](./PowerBi_dashboard/curr_application_distribution.jpg)

#### **Key Portfolio Volume**
* **Total Applications:** **307.51K** unique applications are profiled here.
* **Risk Context:** Of these, **25K** are flagged as risk-associated, keeping the consistent 8% baseline visible for reference.

#### **1. Gender & Asset Ownership**
These visualizations highlight the gender imbalance and asset liquidity of the portfolio:
* **Gender Split:** The portfolio is predominantly female. **Female applicants** account for **65.84%** (202.45K) of the volume, while males account for **34.16%** (105.06K).
* **Real Estate:** A significant majority, **69.37%** (213.31K), own their own home or realty, suggesting a base level of asset stability for most applicants.
* **Vehicle Ownership:** In contrast to housing, car ownership is lower. **65.99%** of applicants do *not* own a car, which may correlate with the high volume of applications from lower-to-middle income segments.

#### **2. Family & Social Structure**
* **Family Status:** **Married** individuals form the overwhelming majority of applicants, representing **63.81%** of the total. Single applicants follow at **14.82%**, with Civil Marriage (9.69%), Separated, and Widows making up the remainder.
* **Income Source:** The "Working" class (blue collar/general workforce) submits the highest volume of applications (~0.16M), followed by "Commercial" associates (~0.07M) and Pensioners (~0.06M).

#### **3. Economic & Geographic Distribution**
* **City Population Density:** The application volume is remarkably balanced across different living environments. High, Medium, Low, and Very Low population density regions each contribute roughly **25%** of the total volume, indicating the lender has a consistent market penetration across both urban and rural settings.
* **Annuity by Occupation:** This bar chart reveals financial capacity by job type. **Managers** and **Accountants** carry the highest average annuity amounts (indicating larger loans and higher repayment capacity), while **Low-skill Laborers** and **Cleaning Staff** have the lowest average annuities.


---
### **4. Risk Drivers & Sensitivity Analysis Dashboard**
This dashboard page offers a granular "deep dive" into the current loan application pool. Unlike the high-level Overview, this view is designed for **sensitivity analysis**, allowing analysts to adjust specific financial levers (like annuity values or job tenure) to see how they impact risk profiles.

![Risk Drivers & Sensitivity Analysis Dashboard](./PowerBi_dashboard/RisK_Drivers_Sensitivity_Analysis_Dashboard.jpg)

#### **Key Financial Ratios & KPIs**
The top section reiterates core portfolio metrics with a specific focus on collateral and affordability ratios:
* **Total Applications:** **307.51K** active files under review.
* **Credit to Goods Ratio (1.12):** This gauge is unique to this page. A ratio greater than 1.0 suggests that, on average, applicants are borrowing slightly more than the value of the goods they are purchasing (potentially for insurance or fees), which can be a risk signal.
* **Affordability Metrics:** The **Annuity to Income Ratio (0.18)** and **Credit to Income Ratio (3.96)** remain visible to monitor baseline affordability.

#### **Advanced Filtering & Sensitivity Controls**
This page features the most extensive set of filters, enabling "What-If" analysis:
* **Demographic Segmentation:** Checkboxes for **Gender** (M/F) and **Education Level** (Higher, Low, Secondary).
* **Risk Sliders:** Users can filter the entire dashboard by specific continuous ranges, such as:
    * **Job Age at Loan:** To isolate new employees vs. stable veterans.
    * **Loan Completion Rate:** To filter based on historical repayment progress.
    * **No. of Contacts:** To analyze if applicants providing more contact methods are more reliable.

#### **Visual Insights: Risk Drivers**
1.  **Distribution of Applicant Category (Defaulter vs. Non-Defaulter)**
    * *Chart:* Grouped bar chart comparing key averages for `Defaulted` vs `Not Defaulted` applicants.
    * *Insight:*
        * **Region Rating (Orange Bar):** Defaulters have a noticeably higher average Region Rating (**2.13**) compared to non-defaulters (**2.02**), suggesting that location/regional economic health is a predictive factor.
        * **Credit-to-Goods (Dark Blue Bar):** Defaulters also show a slightly higher gap between credit received and goods value (**1.15** vs **1.12**), indicating they may be financing more "extras" or have less downpayment coverage.

2.  **Income vs. Risk Ratio**
    * *Chart:* Line chart plotting **Risk Ratio** against **Income Per Person**.
    * *Insight:* There is a visible **inverse relationship** between income and risk.
        * **Highest Risk:** The risk peaks at **10.4%** for the lowest income bracket (near 0–20K).
        * **Lowest Risk:** As income rises to 200K, the risk drops significantly to **6.8%**.
        * **Volatility:** The curve is not perfectly smooth; there is a notable "bump" in risk around the **150K** income mark (**8.2%**), suggesting that higher income does not always guarantee lower risk—perhaps due to higher leverage in that segment.
---

# **Conclusion**

This data visualization project has successfully transformed complex loan application datasets into clear, actionable insights through systematic data cleaning, feature engineering, and in-depth exploratory analysis. The project identifies key behavioral and financial indicators linked to loan default—such as external credit scores, repayment burden ratios, age-related stability, previous refusal rates, and historical application patterns. These insights will guide the finance company in improving its credit evaluation model and risk screening process.

The final engineered and risk-enriched dataset provides a robust, clean foundation for the upcoming interactive Power BI dashboard. This dashboard will enable stakeholders to dynamically explore borrower profiles, segment risk across demographic and financial dimensions, monitor default patterns, and simulate the impact of policy changes in real time. By emphasizing visual storytelling and interpretability, the project bridges raw data with practical business decision-making, supporting faster and more informed credit assessments while reducing potential default losses.

Next steps involve building the interactive Power BI dashboard and preparing a final presentation summarizing key insights for stakeholders.

For a detailed view of the code, notebooks, processed datasets, and visualization outputs, the complete project repository is available on GitHub:  
https://github.com/21f1001520/technerds.git

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
