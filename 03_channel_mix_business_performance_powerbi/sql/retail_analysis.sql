-- MySQL 8+: import data/retail_transactions.csv into retail_transactions.
SELECT DATE_FORMAT(transaction_date,'%Y-%m') AS sales_month,
 SUM(net_sales) AS net_revenue, COUNT(DISTINCT transaction_id) AS transactions,
 SUM(quantity) AS units, SUM(net_sales)/COUNT(DISTINCT transaction_id) AS average_order_value
FROM retail_transactions GROUP BY DATE_FORMAT(transaction_date,'%Y-%m') ORDER BY sales_month;

SELECT sales_channel, SUM(net_sales) AS net_revenue,
 COUNT(DISTINCT transaction_id) AS transactions,
 SUM(net_sales)/COUNT(DISTINCT transaction_id) AS average_order_value
FROM retail_transactions GROUP BY sales_channel ORDER BY net_revenue DESC;

SELECT region, COALESCE(category,'Unclassified') AS category,
 SUM(net_sales) AS net_revenue, SUM(quantity) AS units
FROM retail_transactions GROUP BY region,COALESCE(category,'Unclassified')
ORDER BY region,net_revenue DESC;

SELECT CASE WHEN discount_rate=0 THEN 'No discount'
 WHEN discount_rate<=0.05 THEN 'Up to 5%'
 WHEN discount_rate<=0.10 THEN '5% to 10%' ELSE 'Above 10%' END AS discount_band,
 COUNT(*) AS transactions, AVG(net_sales) AS average_net_sales
FROM retail_transactions GROUP BY discount_band ORDER BY average_net_sales DESC;
