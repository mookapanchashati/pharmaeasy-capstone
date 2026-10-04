import pandas as pd
import json

def compute_percentage_change_v1(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100


print(compute_percentage_change_v1(150, 100))  # Output: 50.0
print(compute_percentage_change_v1(100, 150))  # Output: -33.33333333333333

sales = pd.read_csv("region_month_sales.csv", index_col="region")

april_to_may = {}

for region in sales.index:
    april_sales = sales.loc[region, '2026-04'] if '2023-04' in sales.columns else 0
    may_sales = sales.loc[region, '2026-05'] if '2023-05' in sales.columns else 0
    percentage_change = compute_percentage_change_v1(may_sales, april_sales)
    april_to_may[region] = percentage_change

april_to_may[region] = round(percentage_change, 2)
print(april_to_may)


may_to_june = {}

for region in sales.index:
    may_sales = sales.loc[region, '2026-05'] if '2023-04' in sales.columns else 0
    june_sales = sales.loc[region, '2026-06'] if '2023-05' in sales.columns else 0
    percentage_change = compute_percentage_change_v1(june_sales, may_sales)
    may_to_june[region] = percentage_change

may_to_june[region] = round(percentage_change, 2)
print(may_to_june)


def flag_significant_regions_v1(
    changes,
    threshold=8
):

    flagged = {}

    for region, change in changes.items():
         if abs(change) > threshold:
                flagged[region] = change
    return flagged

flagged_april_may = (
    flag_significant_regions_v1(
        april_to_may,
        threshold=8
    )
)

flagged_may_june = (
    flag_significant_regions_v1(
        may_to_june,
        threshold=8
    )
)

print("\nSignificant April -> May")
print(flagged_april_may)

print("\nSignificant May -> June")
print(flagged_may_june)

# saving

def save_state_v1(month_summary, path):
    with open(path, "w") as file:
        json.dump(
            month_summary,
            file,
            indent=4
        )

def load_previous_state_v1(path):
    with open(path, "r") as file:
        return json.load(file)

april_summary = {}

for region in sales.index:
    april_summary[region] = sales.loc[
        region,
        "2026-04"
    ]   

april_summary = {}

for region in sales.index:
    april_summary[region] = float(
        sales.loc[
            region,
            "2026-04"
        ]
    )

save_state_v1(
    april_summary,
    "april_state.json"
)

# Loading

loaded_april = load_previous_state_v1(
    "april_state.json"
)

print("\nSaved April summary:")
print(april_summary)

print("\nLoaded April summary:")
print(loaded_april)

print(
    "State matches:",
    april_summary == loaded_april
)

may_summary = {}

for region in sales.index:
    may_summary[region] = float(
        sales.loc[
            region,
            "2026-05"
        ]
    )

state_based_changes = {}

for region in may_summary:
    state_based_changes[region] = round(
        compute_percentage_change_v1(
            may_summary[region],
            loaded_april[region]
        ),
        2
    )

print(
    "\nApril -> May calculated using saved state:"
)

print(state_based_changes)

