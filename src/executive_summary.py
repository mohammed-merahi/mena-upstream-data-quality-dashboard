def print_executive_summary(df, results, issue_details):

    total_issues = sum(
        value
        for key, value in results.items()
        if key != "data_quality_score"
    )

    severity_map = {
        "future_spud_date": "Critical",
        "duplicate_wells": "Critical",

        "missing_spud_date": "High",
        "missing_completion_date": "High",
        "missing_operator": "High",

        "invalid_depth": "Medium",
        "invalid_status": "Medium",
        "missing_depth": "Medium"
    }

    critical = 0
    high = 0
    medium = 0

    for issue, records in issue_details.items():

        severity = severity_map.get(issue)

        if severity == "Critical":
            critical += len(records)

        elif severity == "High":
            high += len(records)

        elif severity == "Medium":
            medium += len(records)

    issue_counts = {
        k: v
        for k, v in results.items()
        if k != "data_quality_score"
    }

    top_issue = max(
        issue_counts,
        key=issue_counts.get
    )

    print("\n" + "=" * 50)
    print("EXECUTIVE SUMMARY")
    print("=" * 50)

    print(f"Records Analyzed : {len(df)}")
    print(f"Total Issues     : {total_issues}")
    print(
        f"Quality Score    : {results['data_quality_score']}%"
    )

    print("\nIssue Breakdown")

    print(f"Critical : {critical}")
    print(f"High     : {high}")
    print(f"Medium   : {medium}")

    print(
        f"\nTop Issue: {top_issue.replace('_', ' ').title()}"
    )

    print(
        f"Occurrences: {issue_counts[top_issue]}"
    )

    print("=" * 50)