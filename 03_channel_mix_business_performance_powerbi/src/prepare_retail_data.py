from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"outputs"; OUT.mkdir(exist_ok=True)
df=pd.read_csv(ROOT/"data"/"retail_transactions.csv",parse_dates=["transaction_date"])
print("Loaded rows:",len(df),"| duplicate transaction IDs:",int(df.transaction_id.duplicated().sum()))
print("Missing category values:",int(df.category.isna().sum()))
df=df.drop_duplicates(subset=["transaction_id"],keep="first")
df["category"]=df.category.fillna("Unclassified")
for col in ["quantity","unit_price","discount_rate","gross_sales","net_sales"]:
    df[col]=pd.to_numeric(df[col],errors="coerce")
df=df.dropna(subset=["transaction_id","transaction_date","quantity","net_sales"])
df=df[(df.quantity>0)&(df.net_sales>=0)]
df["sales_month"]=df.transaction_date.dt.to_period("M").astype(str)
df.to_csv(OUT/"retail_clean.csv",index=False)
monthly=df.groupby("sales_month",as_index=False).agg(net_revenue=("net_sales","sum"),
 transactions=("transaction_id","nunique"),units=("quantity","sum"))
monthly["average_order_value"]=monthly.net_revenue/monthly.transactions
monthly.to_csv(OUT/"monthly_kpis.csv",index=False)
channel=df.groupby("sales_channel",as_index=False).agg(net_revenue=("net_sales","sum"),
 transactions=("transaction_id","nunique"),average_order_value=("net_sales","mean"))
channel.to_csv(OUT/"channel_kpis.csv",index=False)
mix=df.groupby(["region","category"],as_index=False).agg(net_revenue=("net_sales","sum"),units=("quantity","sum"))
mix.to_csv(OUT/"region_category_mix.csv",index=False)
print("Clean transactions:",len(df),"| synthetic net revenue:",round(df.net_sales.sum(),2))
print("Outputs written to",OUT)
