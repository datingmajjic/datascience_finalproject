import sqlite3
import chardet
import pandas as pd

# Load kaggle data
with open('Speed_Dating_Data.csv', 'rb') as f:
    result = chardet.detect(f.read())

kaggle_data = pd.read_csv('Speed_Dating_Data.csv', encoding=result['encoding'])

print(kaggle_data)