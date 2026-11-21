from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"outputs"; OUT.mkdir(exist_ok=True)
df=pd.read_csv(ROOT/"data"/"catalogue_sample.csv")
df["listed_price"]=pd.to_numeric(df.listed_price,errors="coerce")
df["customer_rating"]=pd.to_numeric(df.customer_rating,errors="coerce")
print("Rows:",len(df),"| duplicate SKUs:",int(df.catalogue_sku.duplicated().sum()))
df=df.drop_duplicates(subset=["catalogue_sku"]).dropna(subset=["listed_price","customer_rating","category"])
df=df[df.listed_price>=0]
df["price_band"]=pd.cut(df.listed_price,[-.01,20,50,100,float("inf")],
 labels=["Under 20","20 to 50","50 to 100","Over 100"])
df.to_csv(OUT/"catalogue_clean.csv",index=False)
category=df.groupby("category",as_index=False).agg(items=("catalogue_sku","nunique"),
 median_price=("listed_price","median"),average_rating=("customer_rating","mean"))
category.to_csv(OUT/"category_positioning.csv",index=False)
band=df.groupby("price_band",observed=True,as_index=False).agg(items=("catalogue_sku","nunique"),
 average_rating=("customer_rating","mean"))
band.to_csv(OUT/"price_band_rating.csv",index=False)
print("\nCategory positioning:\n",category.sort_values("median_price",ascending=False))
print("Median price:",round(df.listed_price.median(),2),"| average rating:",round(df.customer_rating.mean(),2))
sns.set_theme()
plt.figure(figsize=(10,5)); sns.boxplot(data=df,x="category",y="listed_price")
plt.xticks(rotation=30,ha="right"); plt.title("Catalogue price spread by category")
plt.tight_layout(); plt.savefig(OUT/"price_spread_by_category.png",dpi=160); plt.close()
plt.figure(figsize=(8,5)); sns.scatterplot(data=df,x="listed_price",y="customer_rating",hue="category",alpha=.75)
plt.title("Listed price and customer rating"); plt.tight_layout()
plt.savefig(OUT/"price_rating_relationship.png",dpi=160); plt.close()
print("Outputs written to",OUT)
