import pandas as pd
from .features import FEATURE_COLUMNS, TARGET_COLUMN
def load_dataset(path, target=TARGET_COLUMN):
 df=pd.read_csv(path)
 missing=set(FEATURE_COLUMNS+[target])-set(df.columns)
 if missing: raise ValueError(f'Dataset is missing required columns: {sorted(missing)}')
 if not set(df[target].dropna().unique()).issubset({0,1,False,True}): raise ValueError(f'{target} must contain binary 0/1 labels derived from documented historical outcomes.')
 return df[FEATURE_COLUMNS+[target]].copy()
