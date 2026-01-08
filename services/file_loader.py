import pandas as pd
import os

def load_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.csv':
        return pd.read_csv(filepath)
    elif ext == '.xlsx':
        return pd.read_excel(filepath)
    else:
        raise ValueError('Nieobsługiwany typ pliku')
