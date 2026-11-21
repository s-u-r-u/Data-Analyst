CREATE TABLE retail_transactions (
 transaction_id VARCHAR(24), transaction_date DATE, sales_channel VARCHAR(30),
 region VARCHAR(30), product_name VARCHAR(100), category VARCHAR(50),
 quantity INT, unit_price DECIMAL(10,2), discount_rate DECIMAL(5,4),
 gross_sales DECIMAL(12,2), net_sales DECIMAL(12,2), customer_segment VARCHAR(30)
);
