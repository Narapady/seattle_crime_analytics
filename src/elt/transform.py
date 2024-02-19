import pandas as pd
import duckdb


class Transform:
    def __init__(self, csv_file_path: str) -> None:
        conn = duckdb.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM read_csv_auto(?)", (csv_file_path,))
        result = cursor.fetchall()
        self.df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

    def rename_cols(self) -> pd.DataFrame:
        renamed_df = self.df.rename(
            columns={
                "crime_against_category": "crime_category",
                "offense_parent_group": "parent_group",
                "offense": "description",
                "_100_block_address": "address_100_block",
            }
        )
        renamed_df = renamed_df.drop(columns=["beat"])
        return renamed_df

    def preprocess(self) -> None:
        df = self.rename_cols()
        print(df.columns)

    def load_to_postgres():
        pass

    def load_files_to_postgres():
        pass

    def run():
        pass
