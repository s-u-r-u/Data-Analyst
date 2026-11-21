# Power BI model and DAX
Import `outputs/retail_clean.csv` as `Retail`. Create a Calendar table, mark it as the date table and relate Calendar[Date] to Retail[transaction_date].

```DAX
Net Revenue = SUM(Retail[net_sales])
Transactions = DISTINCTCOUNT(Retail[transaction_id])
Units Sold = SUM(Retail[quantity])
Average Order Value = DIVIDE([Net Revenue], [Transactions])
Revenue Share = DIVIDE([Net Revenue], CALCULATE([Net Revenue], REMOVEFILTERS(Retail[category])))
Previous Month Revenue = CALCULATE([Net Revenue], DATEADD(Calendar[Date], -1, MONTH))
Month-over-Month Change % = DIVIDE([Net Revenue]-[Previous Month Revenue], [Previous Month Revenue])
Average Discount % = AVERAGE(Retail[discount_rate])
```
Validate totals against CSV and SQL outputs before interpretation.
