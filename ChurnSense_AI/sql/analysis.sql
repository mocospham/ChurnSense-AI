/* ChurnSense - Microsoft SQL Server / T-SQL
   Data source: data/customers_scored.csv (SIMULATED RECORDS ONLY).
   Import using SSMS -> Database -> Tasks -> Import Flat File,
   choose customers_scored.csv, set table to dbo.SyntheticChurnScored.
   Choose SQL data types: numeric for metrics/scores, varchar for customer_id.
   Never use this demo to make decisions about real customers.
*/

-- 1) Overview of synthetic scored customers
SELECT COUNT(*) AS total_customers,
       SUM(CASE WHEN risk_score >= 0.50 THEN 1 ELSE 0 END) AS high_risk_customers,
       CAST(AVG(CAST(risk_score AS FLOAT)) * 100 AS DECIMAL(5,2)) AS mean_predicted_risk_pct
FROM dbo.SyntheticChurnScored;

-- 2) Risk by number of products held
SELECT product_count,
       COUNT(*) AS customers,
       CAST(AVG(CAST(risk_score AS FLOAT)) * 100 AS DECIMAL(5,2)) AS avg_risk_pct,
       SUM(CASE WHEN risk_score >= 0.50 THEN 1 ELSE 0 END) AS high_risk_customers
FROM dbo.SyntheticChurnScored
GROUP BY product_count
ORDER BY product_count ASC;

-- 3) Risk according to recency of engagement
SELECT CASE WHEN inactive_days <= 7 THEN '0-7 days'
            WHEN inactive_days <= 30 THEN '8-30 days'
            ELSE '31+ days' END AS inactive_segment,
       COUNT(*) AS customers,
       CAST(AVG(CAST(risk_score AS FLOAT)) * 100 AS DECIMAL(5,2)) AS avg_risk_pct
FROM dbo.SyntheticChurnScored
GROUP BY CASE WHEN inactive_days <= 7 THEN '0-7 days'
              WHEN inactive_days <= 30 THEN '8-30 days'
              ELSE '31+ days' END
ORDER BY avg_risk_pct DESC;

-- 4) 15 highest-risk synthetic customers (illustrative action queue)
SELECT TOP (15) customer_id, monthly_transactions, app_login_days_30d,
       inactive_days, complaints_90d, risk_score
FROM dbo.SyntheticChurnScored
ORDER BY risk_score DESC, customer_id;
