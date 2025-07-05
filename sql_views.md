
# 📊 Complete Set of 18 Insight SQL Views for Streamlit Dashboard



## 🔹 1. Tourism Trends (2019–2024)

```sql
CREATE OR REPLACE VIEW tourism_annual_summary AS
SELECT year, ROUND(SUM(total_fee_cr), 2) AS total_tourism_fee_cr
FROM tourism_fee_final GROUP BY year ORDER BY year;
```

```sql
CREATE OR REPLACE VIEW tourism_monthly_avg AS
SELECT month, ROUND(AVG(total_fee_cr), 2) AS avg_fee_cr
FROM tourism_fee_final GROUP BY month ORDER BY month;
```

```sql
CREATE OR REPLACE VIEW recovery_speed_by_year AS
SELECT year, ROUND(SUM(total_fee_cr), 2) AS total_fee_cr,
LAG(ROUND(SUM(total_fee_cr), 2)) OVER (ORDER BY year) AS prev_year_fee,
ROUND((SUM(total_fee_cr) - LAG(SUM(total_fee_cr)) OVER (ORDER BY year)) / 
NULLIF(LAG(SUM(total_fee_cr)) OVER (ORDER BY year), 0) * 100, 2) AS yoy_growth_pct
FROM tourism_fee_final GROUP BY year ORDER BY year;
```

```sql
CREATE OR REPLACE VIEW peak_tourism_months AS
SELECT month, ROUND(SUM(total_fee_cr), 2) AS total_fee_cr
FROM tourism_fee_final GROUP BY month ORDER BY total_fee_cr DESC;
```

---

## 🔹 2. Economic Impact (Forex vs Domestic Earnings)

```sql
CREATE OR REPLACE VIEW forex_earnings_summary AS
SELECT year, forex_earnings_cr FROM foreign_exchange_earnings_year_wise ORDER BY year;
```

```sql
CREATE OR REPLACE VIEW funding_vs_tourism_by_year AS
SELECT f.year, ROUND(SUM(f.fund_allocated_cr), 2) AS total_funding_cr,
ROUND(SUM(t.total_fee_cr), 2) AS total_tourism_fee_cr
FROM state_cultural_funding_clean f JOIN tourism_fee_final t ON f.year = t.year
GROUP BY f.year ORDER BY f.year;
```

---

## 🔹 3. India in Global Tourism

```sql
CREATE OR REPLACE VIEW india_vs_world_growth AS
SELECT year, world_receipts_growth_rate, india_share_growth_rate, india_rank
FROM tourism_growth_trends WHERE year >= 2014 ORDER BY year;
```

```sql
CREATE OR REPLACE VIEW india_global_share_trend AS
SELECT * FROM india_share_trend;
```

---

## 🔹 4. Government Funding Overview

```sql
CREATE OR REPLACE VIEW funding_by_state AS
SELECT state_name, SUM(fund_allocated_cr) AS total_funding_cr
FROM state_cultural_funding_clean GROUP BY state_name ORDER BY total_funding_cr DESC;
```

```sql
CREATE OR REPLACE VIEW funding_by_year AS
SELECT year, SUM(fund_allocated_cr) AS yearly_funding_cr
FROM state_cultural_funding_clean GROUP BY year ORDER BY year;
```

```sql
CREATE OR REPLACE VIEW funding_by_agency AS
SELECT agency, SUM(fund_allocated_cr) AS total_disbursed_cr
FROM state_cultural_funding_clean GROUP BY agency ORDER BY total_disbursed_cr DESC;
```

```sql
CREATE OR REPLACE VIEW top_funded_states AS
SELECT state_name, SUM(fund_allocated_cr) AS total_funding_cr
FROM state_cultural_funding_clean WHERE state_name IN (
SELECT state_name FROM dim_states WHERE state_type = 'valid')
GROUP BY state_name ORDER BY total_funding_cr DESC LIMIT 10;
```

```sql
CREATE OR REPLACE VIEW state_funding_trends AS
SELECT state_name, year, SUM(fund_allocated_cr) AS total_funding_cr
FROM state_cultural_funding_clean WHERE state_name IN (
SELECT state_name FROM top_funded_states)
GROUP BY state_name, year ORDER BY state_name, year;
```

---

## 🔹 5. Correlation & ROI Analysis

```sql
CREATE OR REPLACE VIEW funding_vs_tourism_states AS
SELECT state_name, SUM(fund_allocated_cr) AS total_funding_cr
FROM state_cultural_funding_clean WHERE state_name IN (
SELECT state_name FROM dim_states WHERE state_type = 'valid')
GROUP BY state_name ORDER BY total_funding_cr DESC;
```

```sql
-- Placeholder if tourism data by state is added
CREATE OR REPLACE VIEW low_funding_high_impact_states AS
SELECT * FROM funding_vs_tourism_states WHERE total_funding_cr < 200;
```

```sql
-- Placeholder if tourism data by state is added
CREATE OR REPLACE VIEW high_funding_low_impact_states AS
SELECT * FROM funding_vs_tourism_states WHERE total_funding_cr > 2000;
```

---

## 🔹 6. General Ranking & Outliers

```sql
CREATE OR REPLACE VIEW highest_growth_year AS
SELECT year, yoy_growth_pct FROM recovery_speed_by_year ORDER BY yoy_growth_pct DESC LIMIT 1;
```

```sql
CREATE OR REPLACE VIEW lowest_growth_year AS
SELECT year, yoy_growth_pct FROM recovery_speed_by_year ORDER BY yoy_growth_pct ASC LIMIT 1;
```


