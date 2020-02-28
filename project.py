import sqlite3
import pandas as pd

# load data
df = pd.read_csv('census_2009-10.csv')

# strip whitespace from headers
df.columns = df.columns.str.strip()

con = sqlite3.connect("census_stuff.db")

# drop data into database
df.to_sql("people", con)




con.close()
