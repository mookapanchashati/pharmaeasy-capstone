import pandas as pd

# Load the SQL-derived monthly sales output from Part 2
sales = pd.read_csv(
    "region_month_sales.csv",
    index_col="region"
)


def percentage_change(current, previous):
    if previous == 0:
        return 0

    return ((current - previous) / previous) * 100


# Build metrics dictionary directly from Part 2 output
metrics = {}

for region in sales.index:

    april = float(sales.loc[region, "2026-04"])
    may = float(sales.loc[region, "2026-05"])
    june = float(sales.loc[region, "2026-06"])

    metrics[region] = {
        "april_sales": april,
        "may_sales": may,
        "june_sales": june,

        "april_to_may_change": round(
            percentage_change(may, april),
            2
        ),

        "may_to_june_change": round(
            percentage_change(june, may),
            2
        )
    }


flagged_regions = {
    "april_to_may": [
        "Hyderabad",
        "Warangal",
        "Visakhapatnam",
        "Guntur",
        "Tirupati",
        "Karimnagar",
        "Bengaluru"
    ],

    "may_to_june": [
        "Hyderabad",
        "Warangal",
        "Vijayawada",
        "Visakhapatnam",
        "Guntur",
        "Tirupati",
        "Karimnagar"
    ]
}

def draft_report_v1(flagged_regions, metrics):

    # Combine both transition lists and remove duplicates
    all_regions = set(
        flagged_regions["april_to_may"]
        + flagged_regions["may_to_june"]
    )

    reports = []

    for region in sorted(all_regions):

        data = metrics[region]

        april_flagged = (
            region in flagged_regions["april_to_may"]
        )

        june_flagged = (
            region in flagged_regions["may_to_june"]
        )

        transitions = []

        if april_flagged:
            transitions.append(
                f"April to May: "
                f"{data['april_to_may_change']}%"
            )

        if june_flagged:
            transitions.append(
                f"May to June: "
                f"{data['may_to_june_change']}%"
            )

        context = (
            f"{region} recorded sales of "
            f"₹{data['april_sales']:.2f} in April, "
            f"₹{data['may_sales']:.2f} in May and "
            f"₹{data['june_sales']:.2f} in June 2026."
        )

        insight = (
            f"The region crossed the 8% operational "
            f"alert threshold for: "
            + "; ".join(transitions)
            + "."
        )

        implication = (
            "The movement is large enough to warrant "
            "human review, but the threshold alone does "
            "not prove that an underlying business change "
            "has occurred."
        )

        reports.append({
            "region": region,
            "Context": context,
            "Insight": insight,
            "Implication": implication
        })

    return reports

reports = draft_report_v1(
    flagged_regions,
    metrics
)

for report in reports:

    print("\n========================")

    print("Region:", report["region"])

    print("\nContext:")
    print(report["Context"])

    print("\nInsight:")
    print(report["Insight"])

    print("\nImplication:")
    print(report["Implication"])



