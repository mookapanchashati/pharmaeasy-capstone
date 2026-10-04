# Title

Guntur April–May Regional Performance Review [LOW]

## Context

Guntur is one of the regions monitored in the PharmEasy Regional Pulse dataset for April, May and June 2026. [HIGH]

The regional metrics used in this memo were calculated from the cleaned order dataset and verified through the Part 2 SQL pipeline. [LOW]

## Key Insight

Guntur recorded a +122.19% month-on-month sales change from April to May 2026. [HIGH]

This was the largest-magnitude flagged movement identified for the April-to-May comparison in the dataset. [HIGH]

The movement therefore requires human review under the project's 8% operational alert rule. [LOW]

## Evidence

Guntur's April and May sales totals were calculated directly from the `orders_clean` table using SQL aggregation by region and month. [LOW]

The resulting April-to-May percentage change was +122.19%. [HIGH]

This exceeds the 8% operational alert threshold used by the project. [HIGH]

## Recommendation

The regional lead should review Guntur's underlying May orders before taking any business action based only on the percentage change. [MEDIUM]

The review should compare order count, product/category mix and sales distribution between April and May to determine what contributed to the movement. [MEDIUM]

## Next Check

Recheck Guntur when the next month's data becomes available and compare the new month against the existing May and June metrics. [MEDIUM]

Also verify whether the increase is concentrated in a small number of orders or spread across the region's order activity. [MEDIUM]

## Assumptions

The +122.19% change indicates a large movement in the dataset, but it does not by itself establish the cause of that movement. [LOW]

Possible changes in order volume or product mix should therefore be treated as hypotheses until they are verified using the underlying order data. [MEDIUM]

No external explanation, such as competitor behaviour, promotions or local demand events, is assumed in this memo. [LOW]