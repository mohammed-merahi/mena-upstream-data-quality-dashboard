import pandas as pd

VALID_STATUSES = [
    "Active",
    "Completed",
    "Shut-In",
    "Suspended"
]


def validate_data(df):

    results = {}
    issue_details = {}

    # Missing Spud Date
    missing_spud = df[df["Spud_Date"].isnull()]
    results["missing_spud_date"] = len(missing_spud)
    issue_details["missing_spud_date"] = (
        missing_spud[["Well_ID"]]
        .to_dict("records")
    )

    # Missing Completion Date
    missing_completion = df[df["Completion_Date"].isnull()]
    results["missing_completion_date"] = len(missing_completion)
    issue_details["missing_completion_date"] = (
        missing_completion[["Well_ID"]]
        .to_dict("records")
    )

    # Missing Operator
    missing_operator = df[df["Operator"].isnull()]
    results["missing_operator"] = len(missing_operator)
    issue_details["missing_operator"] = (
        missing_operator[["Well_ID"]]
        .to_dict("records")
    )

    # Duplicate Wells
    duplicate_wells = df[df["Well_ID"].duplicated()]
    results["duplicate_wells"] = len(duplicate_wells)
    issue_details["duplicate_wells"] = (
        duplicate_wells[["Well_ID"]]
        .to_dict("records")
    )

    # Invalid Status
    invalid_status = df[
        ~df["Status"].isin(VALID_STATUSES)
    ]

    results["invalid_status"] = len(invalid_status)

    issue_details["invalid_status"] = (
        invalid_status[
            ["Well_ID", "Status"]
        ]
        .to_dict("records")
    )

    # Future Spud Date
    today = pd.Timestamp.today()

    future_dates = df[
        pd.to_datetime(
            df["Spud_Date"],
            errors="coerce"
        ) > today
    ]

    results["future_spud_date"] = len(future_dates)

    issue_details["future_spud_date"] = (
        future_dates[
            ["Well_ID", "Spud_Date"]
        ]
        .to_dict("records")
    )

    # Depth Validation
    depth = pd.to_numeric(
        df["Depth_m"],
        errors="coerce"
    )

    missing_depth = df[depth.isnull()]

    results["missing_depth"] = len(missing_depth)

    issue_details["missing_depth"] = (
        missing_depth[["Well_ID"]]
        .to_dict("records")
    )

    invalid_depth = df[
        (depth < 500)
        | (depth > 8000)
    ]

    results["invalid_depth"] = len(invalid_depth)

    issue_details["invalid_depth"] = (
        invalid_depth[
            ["Well_ID", "Depth_m"]
        ]
        .to_dict("records")
    )

    # Data Quality Score
    total_issues = sum(results.values())

    total_records = len(df)

    max_possible_issues = (
        total_records * len(results)
    )

    quality_score = (
        1 - (total_issues / max_possible_issues)
    ) * 100

    results["data_quality_score"] = round(
        quality_score,
        2
    )

    return results, issue_details