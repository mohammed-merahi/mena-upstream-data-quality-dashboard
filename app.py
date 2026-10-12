import pandas as pd
from src.validator import validate_data
from src.report_generator import export_issues
from src.executive_summary import print_executive_summary 
from src.history_tracker import save_history

df = pd.read_csv("data/well_data.csv")

results, issue_details = validate_data(df)

print_executive_summary(
    df,
    results,
    issue_details
)

print("\n" + "=" * 50)
print("MENA WELL DATA QUALITY REPORT")
print("=" * 50)

print(f"\nRecords Analyzed: {len(df)}\n")

for metric, value in results.items():

    if metric != "data_quality_score":

        print(
            f"{metric.replace('_', ' ').title()}: {value}"
        )

print("\n" + "-" * 50)

print(
    f"Data Quality Score: {results['data_quality_score']}%"
)

print("\n" + "=" * 50)
print("ISSUE DETAILS")
print("=" * 50)

for issue, wells in issue_details.items():

    if wells:

        print(
            f"\n{issue.replace('_', ' ').title()}:"
        )

        for well in wells:

            print(f"  - {well}")


export_issues(issue_details)


from collections import Counter

severity_counter = Counter()

for issue, wells in issue_details.items():

    severity = {
        "future_spud_date": "Critical",
        "duplicate_wells": "Critical",

        "missing_spud_date": "High",
        "missing_completion_date": "High",
        "missing_operator": "High",

        "invalid_depth": "Medium",
        "invalid_status": "Medium",
        "missing_depth": "Medium"
    }.get(issue, "Low")

    severity_counter[severity] += len(wells)

print("\n" + "=" * 50)
print("SEVERITY SUMMARY")
print("=" * 50)

for severity in ["Critical", "High", "Medium", "Low"]:

    print(
        f"{severity}: {severity_counter[severity]}"
    )


save_history(results)


