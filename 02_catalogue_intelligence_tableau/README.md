# Catalogue Intelligence: Price Positioning and Customer Ratings

**Portfolio case study | Requests + Beautiful Soup + pandas + EDA + Tableau**

A fictional online discovery team wants to understand catalogue price positioning and customer rating patterns across product categories. The case framing and sample data were created for this portfolio; included sample records are synthetic.

## Run
```bash
pip install -r requirements.txt
python src/analyze_catalogue.py
```
For optional live practice extraction, run `python src/scrape_practice_catalogue.py --pages 2` after checking the practice website's current access rules. The scraper saves a separate file and never overwrites the synthetic sample.

Use `tableau/DASHBOARD_SPEC.md` to build a workbook. Respect website terms, use low request rates and stop if access is denied. Never bypass login, CAPTCHA or technical restrictions.
