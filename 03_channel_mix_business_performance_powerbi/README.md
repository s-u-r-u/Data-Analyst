# Channel Mix and Business Performance: A Retail KPI Case Study

**Portfolio case study | SQL + Python + pandas + Power Query + Power BI + DAX**

A fictional omnichannel retailer wants to understand how category, channel, region and discounting relate to revenue, order volume and average order value. The business questions, schema and generated records were created for this portfolio. All transaction records are synthetic.

## Run
```bash
pip install -r requirements.txt
python src/prepare_retail_data.py
```
Load `data/retail_transactions.csv` into MySQL using `sql/schema.sql`, run `sql/retail_analysis.sql`, and import `outputs/retail_clean.csv` into Power BI. Use the Power BI guides to build your own `.pbix`.
