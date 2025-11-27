# Project Overview

The goal of this project was to create the Responsibility100 Index - a corporate sustainability index focused on Equality, Diversity, and Inclusion (EDI) - using company-provided equality reports. These reports include 26 metrics that capture different aspects of company EDI performance.

During the project, I prepared datasets, analyzed the data, safely imputed missing values, and designed and calculated the final Responsibility100 Index.

---------------------------------------------------------------------------------------------------------------------

# Main Insights

- The provided data was from **2017**, and overall company performance was relatively low compared to today.  
  The highest score was **17/100**.
- Most companies reported only the most general metrics, such as Protected Group representation. These metrics are typically mandatory or easy to collect and tend to be shallow; they do not fully capture real equality of opportunity within companies.
- More representative metrics-such as management-level equality, pay gaps, and parental leave-had **significant missing values** across all demographic groups.
- The most severe gaps were found for the most protected groups, including LGBT+, BAME, and people with disabilities.
- Some **metrics were inherently low** even when reported - for example, maternity leave benefits averaged around two weeks among companies that provided data.
- Sustainability-related metrics, such as **year-to-year improvement**, were missing in more than half of the cases, and available data did not show clear progress.
- The **index** was designed to reward companies that report more representative and meaningful metrics, as well as those that demonstrate improvement over time.

---------------------------------------------------------------------------------------------------------------------

# Index Design

### Final Formula

***Index = 0.25 × Equality Index + 0.25 × Diversity Index + 0.25 × Inclusion Index + 0.25 × Transparency Ratio </span***


### The Main Principle
The index is based on **principle-based grouping** (Equality, Diversity, Inclusion) rather than **demographic-based grouping** (Gender, BAME, LGBT+, Disability). This approach captures what companies are actually achieving.

Despite category prefixes such as `equality_lgbt_reporting`, the meaning of each metric depends on the principle it reflects:

- Equality — fair treatment, pay, and opportunities  
  *e.g., `equality_bame_pay`*
- Diversity — representation across company levels  
  *e.g., `equality_gender_directors`*
- Inclusion — transparency, accountability, and reporting quality  
  *e.g., `equality_lgbt_reporting`*

All metrics were grouped according to these three EDI principles.

<img width="874" height="387" alt="Screenshot 2025-11-27 at 19 32 45" src="https://github.com/user-attachments/assets/1a94b1b8-23c7-4061-ac5f-36d28841aeb6" />


### Handling Missing Data

The dataset had substantial missing values. The main reasons included:
- Metrics that companies did not possess or did not track well  
- Employee reluctance to disclose personal characteristics  

These issues contradict each other and complicate data quality.

The index does not directly punish missing data, and heavily observed metrics receive greater weight. However, the **Transparency component** rewards companies that provide more complete and representative reporting.

---

 Index Calculation Steps

| Step | Description | Notes |
|------|-------------|-------|
| **1. Weighted High-Quality Metrics** | Assign higher weights to well-reported, reliable variables. | Improves robustness and reduces distortion from sparse inputs. |
| **2. Group by EDI Principles** | Organize metrics into Equality, Diversity, Inclusion. | Ensures conceptual clarity. |
| **3. Normalize Values** | Rescale variables to a common range (e.g., 0–1). | Prevents large-range variables from dominating. |
| **4. Compute Sub-Scores** | Calculate composite scores for each EDI dimension. | Enables detailed comparisons. |
| **5. Add Transparency Index** | Score based on completeness and reporting quality. | Rewards transparent companies. |
| **6. Final EDI Index** | Combine all components into a single score. | Produces a comparable measure of performance. |

---------------------------------------------------------------------------------------------------------------------

# Major Challenge: Safe Metric Imputation

The key challenge was safely imputing missing values to generate an accurate index while avoiding distortion.

#### Imputation Strategy

| % Missing | Recommended Strategy | Notes |
|----------:|----------------------|-------|
| **0–5%**  | Simple imputation | Minimal impact; mean/median/mode for numeric or categorical data |
| **5–20%** | Targeted imputation | Investigate MCAR/MAR/MNAR; regression, kNN, or MICE if correlated |
| **20–40%** | Advanced imputation | Multivariate imputation (MICE, kNN) |
| **40–60%** | Domain-specific or leave missing | Regression/time-series if possible; otherwise leave unfilled |
| **>60%** | Leave missing | Only impute when strong domain rules exist |


<img width="856" height="568" alt="image" src="https://github.com/user-attachments/assets/c2e4adc4-9869-4986-83e3-6e34700fc107" />


#### Imputation Summary Table


| Category | Program Name | Missing % | Investigation | Imputation Method | Notes | Missing % After Filling |
|---------|--------------|-----------:|---------------|-------------------|--------|--------------------------:|
| **No imputation** | equality_gender_directors (%) | 0 |  |  |  | 0 |
|  | equality_gender_appointments (%) | 0 |  |  |  |  |
|  | equality_wise (Y/N) | 0 |  |  |  | 0 |
| **Simple imputation** | equality_female_employees (%) | 1.010101 | Numerical. Fairly symmetric, Skew = -0.074, Kurtosis = -0.85. Distribution balanced with no heavy skewness or extreme outliers. | Mean |  | 0 |
|  | equality_disability_reporting (Y/N) | 3.030303 | Categorical | Mode |  |  |
|  | equality_wise_level (Level 4–0) | 3.030303 | Categorical | Mode |  | 0 |
|  | equality_lgbt_reporting (Y/N) | 3.030303 | Categorical | Mode |  | 0 |
|  | equality_bame_reporting (Y/N) | 3.030303 | Categorical | Mode |  | 0 |
|  | equality_parker (Y/N) | 3.030303 | Categorical | Mode |  | 0 |
| **Targeted imputation** | equality_female_management (%) | 8.080808 | MAR; Moderate relationship with several metrics (0.36–0.58). MICE recommended. | Bayesian | R² = 0.7595, RSE = 2.5506 | 0 |
|  | equality_gender_pay (%) | 19.191919 | MCAR. Roughly normal distribution; Skew = 0.36, Kurtosis = -0.78 | Median |  | 0 |
| **Advanced imputation** | equality_gender_pay_previous (%) | 24.242424 | MAR; Strong correlation with gender_pay (0.980) | Linear regression | R² = 0.9595, RSE = 2.5506 | 0 |
|  | equality_gender_bonus (%) | 25.252525 | MAR; Moderate relationship | MICE | R² = 0.652, MAE = 4.04 | 0 |
| **Domain-specific imputation or consider dropping** | equality_gender_pay_improvement (%) | 46.464646 | MAR; Weak correlation with one metric | Unfilled |  | 46.464646 |
|  | equality_leave_primary (W) | 49.494949 | MAR; Correlation with leave_secondary (0.45) | Linear regression | Filled only where correlated column had values | 48 |
|  | equality_leave_secondary (W) | 58.585859 | MAR; Correlation with leave_primary (0.45) | Linear regression | Filled only where correlated column had values | 48 |
| **Remain unfilled** | equality_female_graduates (%) | 69.69697 |  | Unfilled |  | 69.69697 |
|  | equality_bame_employees (%) | 79.79798 |  | Unfilled |  | 79.79798 |
|  | equality_disability_employees (%) | 88.888889 |  | Unfilled |  | 88.888889 |
|  | equality_bame_management (%) | 89.89899 |  | Unfilled |  | 89.89899 |
|  | equality_lgbt_employees (%) | 92.929293 |  | Unfilled |  | 92.929293 |
|  | equality_bame_pay (%) | 96.969697 |  | Unfilled |  | 96.969697 |
|  | equality_lgbt_management (%) | 100 |  | Unfilled |  | 100 |
|  | equality_disability_pay (%) | 100 |  | Unfilled |  | 100 |
|  | equality_disability_management (%) | 100 |  | Unfilled |  | 100 |
|  | equality_lgbt_pay (%) | 100 |  | Unfilled |  | 100 |

<img width="1188" height="790" alt="image" src="https://github.com/user-attachments/assets/52c341dd-3eb8-4513-aff6-25158d1fbc8c" />

---------------------------------------------------------------------------------------------------------------------
# Example of the final document for stakeholders

The fragment from the excel document

<img width="991" height="590" alt="Screenshot 2025-11-27 at 19 26 29" src="https://github.com/user-attachments/assets/b4bcbeca-806b-4738-b69b-a9e9b69181c2" />


# Project Structure

Project_csv/                              — Working files used during the project  
Raw_data/                                 — Original provided data  
01_Dataset_preparing_and_overview.ipynb   — Data preparation and exploration  
02_Filling_Dataset.ipynb                  — Data imputation  
03_Index_calculation.ipynb                — Index design and computation  
Final_ranking.xlsx                        — Final index results  
README.md  
random_test.py                            — Helper functions

---------------------------------------------------------------------------------------------------------------------






