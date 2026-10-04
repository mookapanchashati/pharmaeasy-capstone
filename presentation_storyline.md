# PharmEasy Regional Pulse — Presentation Storyline

## Finding

Guntur recorded a +122.19% month-on-month sales increase from April to May 2026.

---

# 1. Executive Audience — Situation, Complication, Resolution

## Situation

The PharmEasy Regional Pulse pipeline compares regional sales performance across April, May and June 2026 using cleaned and SQL-verified order data.

Guntur was monitored alongside the other active regions using the same month-on-month calculation and 8% operational alert threshold.

## Complication

Guntur's sales increased by 122.19% between April and May.

This is the largest-magnitude April-to-May flagged movement in the dataset and therefore deserves closer review.

The percentage increase identifies a meaningful movement for investigation, but it does not establish why the increase occurred.

## Resolution

Before treating the increase as evidence of sustained regional growth, the regional lead should review the underlying Guntur orders.

The next review should compare order volumes, category mix and the distribution of sales across April and May.

The movement should also be checked against June performance to determine whether it continued or reversed.

---

# 2. Regional Manager Audience — Overview, Category, Detail

## Overview

Guntur's total sales increased by 122.19% from April to May 2026, triggering the project's operational alert threshold.

## Category

The category analysis shows that 

month    category              
2026-04  Lab Tests                 12578.92
         Medical Devices            9490.63
         OTC Medicines              6170.02
         Personal Care              5383.35
         Prescription Medicines     9521.76
         Wellness & Nutrition      19297.59
2026-05  Lab Tests                 23590.94
         Medical Devices           32766.69
         OTC Medicines              8226.44
         Personal Care              9320.26
         Prescription Medicines    11749.59
         Wellness & Nutrition      53085.01
2026-06  Lab Tests                 21126.69
         Medical Devices           30211.77
         OTC Medicines              5094.17
         Personal Care              7494.54
         Prescription Medicines    11518.90
         Wellness & Nutrition      24299.11
Name: sales_inr, dtype: float64

 was an important contributor to Guntur's May sales.

 ## Category

Wellness & Nutrition was the largest contributor to Guntur's May sales, increasing from ₹19,297.59 in April to ₹53,085.01 in May.

This represents an increase of ₹33,787.42 and accounts for approximately 44.3% of Guntur's total April-to-May sales increase.

Medical Devices was also a major contributor, increasing from ₹9,490.63 to ₹32,766.69.

These category movements help explain where the increase occurred within the dataset, but they do not establish the underlying business reason for the change.

The category result comes directly from the cleaned order-level dataset and should be reviewed alongside the remaining categories rather than treated as proof of the cause of the increase.

## Detail

Guntur's total sales increased from ₹62,442.27 in April to ₹138,738.93 in May 2026.

Using the month-on-month formula:

(Current Month Sales - Previous Month Sales)
/
Previous Month Sales
× 100

the calculated increase is +122.19%.

The largest category-level increase came from Wellness & Nutrition, which rose by ₹33,787.42. Medical Devices recorded the second-largest increase, rising by ₹23,276.06.

These figures are derived directly from the cleaned order data and the SQL-based regional and monthly metrics pipeline.

---

# Anticipated Stakeholder Questions

## Question 1 — Why should I believe this number?

### Acknowledge

It is reasonable to question a 122.19% increase because it is substantially larger than the project's 8% alert threshold.

### Verified vs. Not Verified

The April and May sales values and the resulting 122.19% change are verified from the cleaned dataset and SQL metrics pipeline.

The pipeline does not, however, verify the business reason behind the increase.

### Resolution

The number can be rechecked directly against the Guntur order-level records and SQL aggregation before the review is signed off.

---

## Question 2 — What if another explanation is driving this increase?

### Acknowledge

The increase could result from changes in order volume, category mix or unusually large orders rather than a broad improvement in regional performance.

### Verified vs. Not Verified

The sales movement itself is verified.

The underlying cause has not been established by the current analysis.

### Resolution

The regional lead should compare April and May order counts, category contribution and order-value distribution during the current review before assigning a cause.

---

## Question 3 — What did you not check?

### Acknowledge

The current pipeline is designed to identify regional performance movements, not to establish every external factor affecting those movements.

### Verified vs. Not Verified

The order, sales, profit, region, month and category information in the supplied dataset has been checked.

External factors such as competitor activity, promotions or local market events were not included in the dataset and therefore were not verified.

### Resolution

If those factors are needed for a business decision, they should be investigated separately before the regional lead concludes why Guntur's performance changed.