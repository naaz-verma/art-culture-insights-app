
# 📊 Snowflake Data Cleaning & Normalization

This section documents the SQL transformations used to clean, normalize, and prepare datasets in Snowflake for the **Art, Culture, and Tourism Dashboard**.

---

## 🔹 Dataset 1: `tourism_fee` (Monthly Tourism Earnings)

**Problem:**  
- Raw table had one column per year (wide format)  
- 2021 values were in **Lakhs**, rest in **Cr**

**Steps Taken:**

```sql
-- 1. Normalize wide format to long format
CREATE OR REPLACE TABLE tourism_fee_clean (
    month STRING,
    year INT,
    total_fee_cr DECIMAL(12,2)
);

INSERT INTO tourism_fee_clean (month, year, total_fee_cr)
SELECT MONTH, 2019, YEAR19 FROM tourism_fee WHERE YEAR19 IS NOT NULL
UNION ALL
SELECT MONTH, 2020, YEAR20 FROM tourism_fee WHERE YEAR20 IS NOT NULL
UNION ALL
SELECT MONTH, 2021, YEAR21 FROM tourism_fee WHERE YEAR21 IS NOT NULL
UNION ALL
SELECT MONTH, 2023, YEAR23 FROM tourism_fee WHERE YEAR23 IS NOT NULL
UNION ALL
SELECT MONTH, 2024, YEAR24 FROM tourism_fee WHERE YEAR24 IS NOT NULL;

-- 2. Create a month dimension table for sorting
CREATE OR REPLACE TABLE dim_months AS
SELECT * FROM VALUES
('January', 1), ('February', 2), ('March', 3), ('April', 4), ('May', 5),
('June', 6), ('July', 7), ('August', 8), ('September', 9), ('October', 10),
('November', 11), ('December', 12)
AS dim_month(month_name, month_number);

-- 3. Convert 2021 values from Lakhs → Cr
CREATE TABLE tourism_fee_final AS
SELECT
    month,
    year,
    CASE
        WHEN year = 2021 THEN total_fee_cr / 100
        ELSE total_fee_cr
    END AS total_fee_cr
FROM tourism_fee_clean;
```

✅ **Final usable table**: `tourism_fee_final`

---

## 🔹 Dataset 2: `foreign_exchange_earnings_year_wise` (Annual Forex Earnings)

**Status**: Already normalized. No changes required.  
Contains India's tourism-related forex earnings from 2014 to 2020 in ₹ Cr.

✅ **Final usable table**: `foreign_exchange_earnings_year_wise`

---

## 🔹 Dataset 3: `international_tourism_stats` (Global Context)

**Steps Taken:**

```sql
-- 1. Clean raw data
CREATE OR REPLACE TABLE international_tourism_stats_clean AS
SELECT
    year,
    world_receipts_usd_million,
    world_receipts_growth_rate,
    india_share_usd_million,
    india_share_growth_rate,
    india_share_pct,
    india_rank
FROM international_tourism_stats;

-- 2. Optional: convert to Billion USD for presentation
SELECT
    year,
    ROUND(world_receipts_usd_million / 1000, 2) AS world_receipts_billion,
    ROUND(india_share_usd_million / 1000, 2) AS india_receipts_billion
FROM international_tourism_stats_clean;

-- 3. Create reusable views
CREATE OR REPLACE VIEW tourism_growth_trends AS
SELECT
    year,
    world_receipts_growth_rate,
    india_share_growth_rate,
    india_rank
FROM international_tourism_stats_clean;

CREATE OR REPLACE VIEW india_share_trend AS
SELECT
    year,
    india_share_pct,
    india_share_usd_million,
    india_rank
FROM international_tourism_stats_clean
ORDER BY year;
```

✅ **Final table**: `international_tourism_stats_clean`  
✅ **Final views**: `tourism_growth_trends`, `india_share_trend`

---

## 🔹 Dataset 4: `state_cultural_funding` (Project-Wise Govt. Funding)

**Issues**:  
- Inconsistent `state_name` values (e.g., NER, Sikkim/West Bengal)  
- Fund in Lakhs → converted to Cr  
- Needed classification for clean dashboards

**Steps Taken:**

```sql
-- 1. Clean and normalize funding data
CREATE OR REPLACE TABLE state_cultural_funding_clean AS
SELECT
    year,
    sanction_date,
    TRIM(state_name) AS state_name,
    TRIM(project_name) AS project_name,
    TRIM(agency) AS agency,
    fund_allocated_lakh,
    ROUND(fund_allocated_lakh / 100, 2) AS fund_allocated_cr
FROM state_cultural_funding
WHERE fund_allocated_lakh IS NOT NULL;

-- 2. Create state dimension table
CREATE OR REPLACE TABLE dim_states AS
SELECT DISTINCT
    TRIM(state_name) AS state_name
FROM state_cultural_funding
ORDER BY state_name;

ALTER TABLE dim_states ADD COLUMN state_type STRING;

-- 3. Manually tag state names
-- Mark valid states
UPDATE dim_states SET state_type = 'valid'
WHERE state_name IN (
  'Delhi', 'Kerala', 'Goa', 'Maharashtra', 'Rajasthan',
  'Telangana', 'Bihar', 'Punjab (GFR)', 'Assam', 'Mizoram',
  'Madhya Pradesh'
);

-- Mark grouped/combined states
UPDATE dim_states SET state_type = 'grouped'
WHERE state_name IN (
  'NER', 'Leh & Ladakh', 'Sikkim/West Bengal'
);

-- Tag the rest as unknown
UPDATE dim_states SET state_type = 'unknown'
WHERE state_type IS NULL;

-- 4. Create views for analysis
CREATE OR REPLACE VIEW funding_by_state AS
SELECT
    state_name,
    SUM(fund_allocated_cr) AS total_funding_cr
FROM state_cultural_funding_clean
GROUP BY state_name
ORDER BY total_funding_cr DESC;

CREATE OR REPLACE VIEW funding_by_year AS
SELECT
    year,
    SUM(fund_allocated_cr) AS yearly_funding_cr
FROM state_cultural_funding_clean
GROUP BY year
ORDER BY year;

CREATE OR REPLACE VIEW funding_by_agency AS
SELECT
    agency,
    SUM(fund_allocated_cr) AS total_disbursed_cr
FROM state_cultural_funding_clean
GROUP BY agency
ORDER BY total_disbursed_cr DESC;
```

✅ **Final table**: `state_cultural_funding_clean`  
✅ **Dimension**: `dim_states` (with `state_type`)  
✅ **Views**: `funding_by_state`, `funding_by_year`, `funding_by_agency`

---

## ✅ Final Snowflake Tables & Views Summary

| Name                             | Type     | Description                                 |
|----------------------------------|----------|---------------------------------------------|
| `tourism_fee_final`              | Table    | Cleaned monthly tourism earnings (Cr)       |
| `foreign_exchange_earnings_year_wise` | Table    | Annual forex earnings from tourism          |
| `international_tourism_stats_clean`   | Table    | India + global tourism stats                |
| `state_cultural_funding_clean`        | Table    | Cleaned project-wise cultural funding       |
| `dim_states`, `dim_months`       | Table    | Support tables for filtering/sorting        |
| `tourism_growth_trends`          | View     | YoY % growth for India vs world             |
| `india_share_trend`              | View     | India's % share + rank in world tourism     |
| `funding_by_state`               | View     | Total cultural funding by state             |
| `funding_by_year`                | View     | Yearly cultural funding                     |
| `funding_by_agency`             | View     | Top agencies disbursing cultural funds      |
