# 🤖 AI Agent Handoff Specification

## 1. Context Metadata
* **Source Session:** Data Science, AI & Statistics Market Research
* **Target Role:** Downstream AI Analytics / ETL Agent
* **Handoff Version:** 1.0.0
* **Status:** Ready for Processing
* **Domain Scope:** AI, Data Science, and Statistics (Graduates, Employment, Salaries, Skills, Career Levels)

---

## 2. Summary of Ingested Context

The upstream process gathered and categorized Open Data resources regarding the global landscape of AI, Data Science, and Statistics:

1. **Academic Output:** Graduate statistics across degree levels (Bachelor's, Master's, Ph.D.) sourced from national education registries and open surveys.
2. **Employment & Compensation:** Job market volume, international salary distributions, and country-level breakdowns segmented by experience.
3. **Market Demand & Skills:** Skill profiles extracted from public job postings across major platforms.
4. **Career Progression Standards:** Classification into Entry-level (`EN`), Mid-level (`MI`), and Senior/Executive (`SE`/`EX`).

---

## 3. Data Schema & Source Mapping

### A. Dataset 1: Higher Education Graduates
* **Primary Sources:** NCES IPEDS (US Govt Open Data), Kaggle ML & DS Survey
* **Target Schema:**
  ```json
  {
    "year": "integer",
    "country": "string",
    "degree_level": "enum [Bachelor, Master, PhD]",
    "field_code": "string (CIP Code e.g. 30.7001)",
    "field_name": "enum [Artificial Intelligence, Data Science, Statistics, Computer Science]",
    "graduate_count": "integer"
  }
  ```

### B. Dataset 2: Employment & Salary Distribution
* **Primary Sources:** U.S. Bureau of Labor Statistics (BLS OEWS), Kaggle DS Salaries Dataset
* **Target Schema:**
  ```json
  {
    "work_year": "integer",
    "job_title": "string",
    "experience_level": "enum [EN, MI, SE, EX]",
    "employment_type": "enum [FT, PT, CT, FL]",
    "salary_in_usd": "float",
    "employee_residence": "string (ISO 2-letter code)",
    "company_location": "string (ISO 2-letter code)",
    "company_size": "enum [S, M, L]"
  }
  ```

### C. Dataset 3: Job Listings & Skill Extraction
* **Primary Sources:** Data Science Job Postings with Salaries & Skills (Scraped Open Datasets)
* **Target Schema:**
  ```json
  {
    "posting_id": "string",
    "company_name": "string",
    "job_title": "string",
    "country": "string",
    "minimum_degree": "enum [None, Bachelor, Master, PhD]",
    "required_skills": "array of strings",
    "experience_years_required": "float"
  }
  ```

---

## 4. Standardized Categorization Framework

### Career Levels Taxonomy
| Level Code | Level Name | YOE Range | Key Core Competencies |
| :--- | :--- | :--- | :--- |
| `EN` | Entry-level / Junior | 0 - 2 yrs | Basic Python/R, SQL, Data Wrangling, Basic Statistics, EDA, Dashboarding |
| `MI` | Mid-level / Intermediate | 2 - 5 yrs | Advanced Modeling, ML Pipelines, Deep Learning, Feature Engineering, Cloud (AWS/GCP/Azure) |
| `SE` | Senior / Specialist | 5 - 8 yrs | System Architecture, MLOps, Business Strategy Alignment, Distributed Computing |
| `EX` | Executive / Director | 8+ yrs | Organization AI Strategy, Budgeting, Cross-functional Leadership, AI Governance |

### Skill Taxonomy Checklist
* **Languages:** `Python`, `R`, `SQL`, `C++`, `Julia`
* **Frameworks & Libs:** `PyTorch`, `TensorFlow`, `Scikit-Learn`, `Pandas`, `NumPy`
* **Statistics & Math:** `Hypothesis Testing`, `Regression Analysis`, `A/B Testing`, `Bayesian Inference`
* **Infrastructure & MLOps:** `Docker`, `Kubernetes`, `Spark`, `Airflow`, `AWS`, `GCP`, `Azure`
* **Visualization:** `Tableau`, `Power BI`, `Matplotlib`, `Seaborn`

---

## 5. Execution Instructions for Next AI Agent

Please execute the following tasks using the schemas and context provided above:

1. **Data Normalization & Fusion:**
   * Merge the target schema outputs into a consolidated data model.
   * Standardize country codes using ISO-3166-1 alpha-2.
   * Convert all salary entries to USD equivalents where applicable.

2. **Analytical Objectives:**
   * **Supply vs. Demand Analysis:** Compare the annual output of graduates against the estimated job openings for `EN` positions.
   * **Salary Benchmarking:** Calculate median salary and interquartile range (IQR) grouped by `experience_level` and `company_location`.
   * **Skill Co-occurrence Matrix:** Compute the top 10 skill co-occurrence pairs in modern AI/DS job postings.

3. **Output Formatting:**
   * Return results in clean, structured JSON or Markdown summary tables.
   * Highlight any gaps or missing values detected during data cleaning.