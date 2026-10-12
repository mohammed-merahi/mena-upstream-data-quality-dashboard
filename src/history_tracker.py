import os
import pandas as pd
from datetime import datetime


def save_history(results):

    history_file = "reports/history.csv"

    row = {
        "Run_Date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "Quality_Score":
            results["data_quality_score"],
        "Total_Issues":
            sum(
                value
                for key, value in results.items()
                if key != "data_quality_score"
            )
    }

    new_df = pd.DataFrame([row])

    if os.path.exists(history_file):

        history_df = pd.read_csv(history_file)

        history_df = pd.concat(
            [history_df, new_df],
            ignore_index=True
        )

    else:

        history_df = new_df

    history_df.to_csv(
        history_file,
        index=False
    )

    print(
        "\nHistory updated: reports/history.csv"
    )