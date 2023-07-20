from typing import List
import pandas as pd

def replace_in_df_column(mydf: pd.DataFrame(), column_list: List[str], pat_str: str, repl_str: str):
    for column in column_list:
        mydf[column] = mydf[column].str.replace(pat_str,repl_str)