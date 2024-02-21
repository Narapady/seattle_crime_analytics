import awswrangler as wr
import pandas as pd


# for easy partition by year and month
def fix_col_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    df["report_datetime"] = pd.to_datetime(df["report_datetime"])
    df["report_year"] = df["report_datetime"].dt.year
    df["report_month"] = df["report_datetime"].dt.month
    return df
