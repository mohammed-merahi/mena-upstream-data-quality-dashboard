import pandas as pd

SEVERITY_MAP = {
    "future_spud_date": "Critical",
    "duplicate_wells": "Critical",

    "missing_spud_date": "High",
    "missing_completion_date": "High",
    "missing_operator": "High",

    "invalid_depth": "Medium",
    "invalid_status": "Medium",
    "missing_depth": "Medium"
}


def export_issues(issue_details):

    rows = []

    for issue, wells in issue_details.items():

        for well in wells:

            rows.append({
                "Well_ID": well,
                "Issue_Type": issue,
                "Severity": SEVERITY_MAP.get(
                    issue,
                    "Low"
                )
            })

    issues_df = pd.DataFrame(rows)

    issues_df.to_csv(
        "reports/data_quality_issues.csv",
        index=False
    )

    print(
        "\nReport exported: reports/data_quality_issues.csv"
    )