import pandas as pd

def parse_json_to_dataframe(json_code):
    df = pd.json_normalize(json_code)
    return df