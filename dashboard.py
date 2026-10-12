import pandas as pd
import streamlit as st
import plotly.express as px

from src.validator import validate_data
from io import BytesIO


def to_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Issues",
            index=False
        )

    return output.getvalue()


st.set_page_config(
    page_title="MENA Upstream Data Quality Dashboard",
    layout="wide"
)

st.title("MENA Upstream Data Quality Dashboard")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    # Load Data
    df = pd.read_csv(uploaded_file)

    # Run Validation
    results, issue_details = validate_data(df)

    total_issues = sum(
        value
        for key, value in results.items()
        if key != "data_quality_score"
    )

    # ==========================
    # KPI CARDS
    # ==========================

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.metric(
            "Quality Score",
            f"{results['data_quality_score']}%"
        )

    with kpi2:
        st.metric(
            "Total Issues",
            total_issues
        )

    with kpi3:
        st.metric(
            "Records",
            len(df)
        )

    # ==========================
    # EXECUTIVE SUMMARY
    # ==========================

    critical = 0
    high = 0
    medium = 0

    for issue, records in issue_details.items():

        if issue in [
            "future_spud_date",
            "duplicate_wells"
        ]:
            critical += len(records)

        elif issue in [
            "missing_spud_date",
            "missing_completion_date",
            "missing_operator"
        ]:
            high += len(records)

        elif issue in [
            "invalid_depth",
            "invalid_status",
            "missing_depth"
        ]:
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

    st.subheader("Executive Summary")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.error(
            f"🔴 Critical Issues\n\n# {critical}"
        )

    with s2:
        st.warning(
            f"🟠 High Issues\n\n# {high}"
        )

    with s3:
        st.info(
            f"🟡 Medium Issues\n\n# {medium}"
        )

    with s4:
        st.success(
            f"🏆 Top Issue\n\n{top_issue.replace('_', ' ').title()}"
        )

    st.caption(
        f"Analyzed {len(df)} records • "
        f"{total_issues} issues found • "
        f"Data Quality Score {results['data_quality_score']}%"
    )

    # ==========================
    # ISSUE BREAKDOWN
    # ==========================

    breakdown = pd.DataFrame({
        "Issue": [
            k.replace("_", " ").title()
            for k in results.keys()
            if k != "data_quality_score"
        ],
        "Count": [
            v
            for k, v in results.items()
            if k != "data_quality_score"
        ]
    })

    st.subheader("Data Quality Issues")

    fig = px.bar(
        breakdown,
        x="Issue",
        y="Count",
        color="Count",
        title="Data Quality Issues"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================
    # ISSUE DETAILS
    # ==========================

    # ==========================
    # ISSUE DETAILS
    # ==========================

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

    issue_rows = []

    for issue, records in issue_details.items():

        severity = severity_map.get(
            issue,
            "Low"
        )

        for record in records:

            details = {
                k: v
                for k, v in record.items()
                if k != "Well_ID"
            }

            issue_rows.append({
                "Well ID": record.get("Well_ID"),
                "Issue": issue.replace(
                    "_",
                    " "
                ).title(),
                "Severity": severity,
                "Value": (
                    "Missing"
                    if not details
                    else str(details)
                )
            })

    issues_df = pd.DataFrame(issue_rows)

    st.subheader("Issue Details")

    # Download Button
    # Download Buttons

    col1, col2 = st.columns(2)

    with col1:

        csv = issues_df.to_csv(
            index=False
        )

        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name="data_quality_issues_report.csv",
            mime="text/csv"
        )
    
    with col2:

        excel_file = to_excel(
            issues_df
        )

        st.download_button(
            label="📊 Download Excel",
            data=excel_file,
            file_name="data_quality_issues_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


    # Issue Table
    st.dataframe(
        issues_df,
        use_container_width=True
    )