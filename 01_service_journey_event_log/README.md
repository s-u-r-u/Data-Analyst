# Service Journey Event Log: Where Does a Request Lose Time?

**Portfolio case study | SQL + Python + pandas + NumPy + statistics + Matplotlib + Seaborn**

A fictional multi-region equipment-services business wants to understand why some service requests take longer than others. Requests move through intake, triage, assignment, parts decision, site visit and closure.

The case framing, schema, generated records and analysis workflow were created for this portfolio. All records are synthetic.

## Questions
- Which workflow transitions have the longest waiting times?
- Do priority and service region show different completion-time patterns?
- How often do event sequences contain missing steps, duplicate events or timestamp anomalies?
- Which request characteristics are associated with longer elapsed time?

## Run
```bash
pip install -r requirements.txt
python src/analyze_service_journey.py
```
For SQL, create the MySQL 8 table using `sql/schema.sql`, import `data/service_events.csv`, then run `sql/analysis.sql`. Outputs are written to `outputs/`.

Correlation is not causation. Do not present synthetic results as measured employer impact.
