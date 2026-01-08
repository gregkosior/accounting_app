import pandas as pd

def clean_data(df):
    # Przykładowe czyszczenie: usuwanie duplikatów, uzupełnianie braków
    df = df.drop_duplicates()
    df = df.fillna(0)
    return df
