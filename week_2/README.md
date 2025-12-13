# Feature Engineering 

##  Overview
This Feature engineering process applied to the `application_data.csv` and `previous_application.csv` datasets. The objective was to transform initially cleaned data into a concise, interpretable set of features that effectively capture borrower profiles, loan characteristics, and historical repayment behavior.

The process included domain-driven transformations, ratio calculations, time conversions, and careful aggregation of historical records. The resulting final dataset contains 307,511 observations and 68 columns, with no missing values and a preserved default rate of 8.073%. This engineered dataset is optimised for exploratory analysis, risk segmentation, and interactive visualisation in Power BI.

## 1. Feature Engineering on Application Data
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

## 2. Feature Engineering on Previous Application Data
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

## 3. Final Dataset Assembly
The engineered application and previous-application datasets were merged on `SK_ID_CURR` using a left join. Remaining missing values in previous-application features were imputed with zeros (no history) and, where necessary, medians for numerical columns and modes for categorical columns.

The final dataset comprises 307,511 rows and 68 columns, maintaining the original target distribution (default rate 8.073%) and containing no missing values.

The dataset was exported as `final_dataset.csv` in `data/final_dataset/` for direct use in Power BI dashboard development and presentation materials.

This engineered dataset provides a clean, compact, and domain-aligned foundation for identifying risk patterns, segmenting borrower profiles, and constructing the required interactive risk dashboard.