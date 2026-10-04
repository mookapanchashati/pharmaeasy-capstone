PharmEasy Regional Pulse is a small end-to-end data pipeline built to make monthly regional performance reviews more consistent and easier to trust.

The project starts with a raw monthly order export, cleans the data, checks the schema, verifies regional metrics using SQLite, flags unusual month-on-month movements, generates a reviewable narrative, and finally presents the results through an interactive Streamlit dashboard.

The idea is simple: by the time someone opens the dashboard, the numbers should already have gone through cleaning, validation, SQL checks, and a human review step.

How to run the project

1. Install the required libraries

From the project folder, run:

py -m pip install -r requirements.txt

The project uses:

pandas

streamlit

plotly

sqlite3 from Python's standard library

No API key or paid service is required.

2. Generate the source dataset

Run:

py generate_dataset.py

This creates:

pharmeasy_orders_raw.csv

regions_master.csv

The generator is deterministic, so the same dataset is produced every time.

3. Clean and validate the data

Run:

py clean_data.py

This step:

removes exact duplicate rows

standardizes region names

fills missing category values

fills missing profit values using category-level average profit margins

validates the required schema

saves the cleaned dataset as orders_clean.csv

The final cleaned dataset contains 2100 rows.

4. Build the SQLite database

Run:

py build_db.py

This creates pharmeasy.db and loads regions_master and orders_clean into SQLite tables.

5. Run SQL validation and regional metrics

Run:

py queries.py

This checks:

LEFT JOIN vs INNER JOIN row counts

duplicate order IDs

the COUNT(*) vs COUNT(order_id) difference for Kurnool

per-region order counts

monthly regional sales totals

The monthly sales output is also saved for use in the next stages.

6. Calculate month-on-month changes and alert flags

Run:

py metrics_engine.py

This calculates regional month-on-month sales changes and applies the 8% operational alert threshold.

The threshold is only used as a review trigger. It should not be treated as statistical proof that a real business change has occurred.

The script also saves and reloads previous-month state using JSON so the pipeline can reuse earlier results without recomputing the entire history.

7. Generate the regional narrative

Run:

py draft_report.py

This creates Context–Insight–Implication style summaries for the regions that crossed the operational alert threshold. Regions flagged in both transitions are shown only once, with both movements included in the same summary.

8. Run the human review gate

Run:

py review_gate.py

This tests all three review decisions:

approve

edit

reject

Each review action is written to audit_log.jsonl with:

timestamp

run ID

region

decision

reviewer note

Only an approved report is allowed to move forward for downstream use.

9. Start the dashboard

Run:

py -m streamlit run app.py

The dashboard includes:

total sales

total profit

distinct order count

monthly sales trends

regional sales comparison

category sales share

category-level breakdown

region-by-month detail

The region filter updates the dashboard views together.

Headline Finding

The clearest finding in the dataset is Guntur's April-to-May movement.

Guntur's sales increased from ₹62,442.27 in April to ₹138,738.93 in May 2026, which is a +122.19% month-on-month increase.

The biggest category contributor to this increase was Wellness & Nutrition, which rose from ₹19,297.59 to ₹53,085.01. This category alone contributed roughly 44.3% of Guntur's total sales increase.

This is a strong signal worth reviewing, but the dataset does not prove why the increase happened. The underlying cause still needs human investigation