from pathlib import Path
import argparse,time
import pandas as pd,requests
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
PAGE="https://books.toscrape.com/catalogue/page-{}.html"
RATING={"One":1,"Two":2,"Three":3,"Four":4,"Five":5}
def scrape(pages,delay):
    session=requests.Session()
    session.headers["User-Agent"]="SurajPortfolioCatalogueStudy/1.0 (educational, low-rate)"
    records=[]
    for number in range(1,pages+1):
        response=session.get(PAGE.format(number),timeout=20); response.raise_for_status()
        soup=BeautifulSoup(response.text,"html.parser")
        for card in soup.select("article.product_pod"):
            classes=card.select_one("p.star-rating").get("class",[])
            rating=next((x for x in classes if x in RATING),None)
            records.append({"item_label":card.h3.a.get("title","").strip(),
              "listed_price_gbp":float(card.select_one(".price_color").get_text(strip=True).replace("£","").replace("Â","")),
              "customer_rating":RATING.get(rating),
              "stock_text":card.select_one(".availability").get_text(" ",strip=True),
              "source_page":PAGE.format(number)})
        time.sleep(delay)
    dest=ROOT/"data"/"practice_site_extract.csv"
    pd.DataFrame(records).to_csv(dest,index=False); print("Saved",len(records),"rows to",dest)
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--pages",type=int,default=2); ap.add_argument("--delay",type=float,default=2.0)
    a=ap.parse_args()
    if a.pages<1 or a.delay<1: raise SystemExit("Use >=1 page and >=1 second delay.")
    scrape(a.pages,a.delay)
