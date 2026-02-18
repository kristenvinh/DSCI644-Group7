import pandas as pd

def parse_json_to_dataframe(json_code):
    jobs = json_code['jobs']
    df = pd.json_normalize(jobs)
    return df