from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"outputs"; OUT.mkdir(exist_ok=True)
df=pd.read_csv(ROOT/"data"/"service_events.csv",parse_dates=["event_time"])
print("Input event rows:",len(df),"| duplicate rows:",int(df.duplicated().sum()))
print("Missing values:\n",df.isna().sum())
df=df.drop_duplicates().dropna(subset=["request_id","event_name","event_time"])
df["service_region"]=df["service_region"].fillna("Unspecified")
df=df.sort_values(["request_id","event_time"])
df.to_csv(OUT/"clean_service_events.csv",index=False)
request=(df.groupby("request_id",as_index=False)
 .agg(opened_at=("event_time","min"),closed_at=("event_time","max"),
      priority=("priority","first"),service_region=("service_region","first"),
      asset_family=("asset_family","first"),event_count=("event_name","nunique")))
request["elapsed_hours"]=(request.closed_at-request.opened_at).dt.total_seconds()/3600
request["opened_month"]=request.opened_at.dt.to_period("M").astype(str)
request.to_csv(OUT/"request_metrics.csv",index=False)
df["next_event"]=df.groupby("request_id").event_name.shift(-1)
df["next_time"]=df.groupby("request_id").event_time.shift(-1)
df["wait_hours"]=(df.next_time-df.event_time).dt.total_seconds()/3600
transition=(df.dropna(subset=["next_event"]).groupby(["event_name","next_event"],as_index=False)
 .agg(median_wait_hours=("wait_hours","median"),mean_wait_hours=("wait_hours","mean"),
      observations=("request_id","nunique")))
transition.to_csv(OUT/"transition_waits.csv",index=False)
monthly=request.groupby("opened_month",as_index=False).agg(
 requests=("request_id","nunique"),median_elapsed_hours=("elapsed_hours","median"))
monthly.to_csv(OUT/"monthly_request_trend.csv",index=False)
print("\nPriority comparison:\n",request.groupby("priority").elapsed_hours.agg(["count","median","mean"]))
print("\nLongest median transitions:\n",transition.sort_values("median_wait_hours",ascending=False).head())
sns.set_theme()
plt.figure(figsize=(9,5)); sns.boxplot(data=request,x="priority",y="elapsed_hours",order=["Routine","Priority","Critical"])
plt.title("Request elapsed time by priority"); plt.xlabel("Priority"); plt.ylabel("Elapsed time (hours)")
plt.tight_layout(); plt.savefig(OUT/"elapsed_by_priority.png",dpi=160); plt.close()
plt.figure(figsize=(10,5)); sns.barplot(data=transition.sort_values("median_wait_hours",ascending=False),
 x="median_wait_hours",y="event_name",hue="next_event",dodge=False)
plt.title("Median wait by workflow transition"); plt.xlabel("Median wait (hours)")
plt.ylabel("Transition starts at"); plt.tight_layout(); plt.savefig(OUT/"transition_waits.png",dpi=160); plt.close()
plt.figure(figsize=(10,5)); sns.lineplot(data=monthly,x="opened_month",y="median_elapsed_hours",marker="o")
plt.xticks(rotation=45,ha="right"); plt.title("Monthly median request elapsed time")
plt.xlabel("Opening month"); plt.ylabel("Median elapsed hours")
plt.tight_layout(); plt.savefig(OUT/"monthly_elapsed_trend.png",dpi=160); plt.close()
print("Outputs written to",OUT)
