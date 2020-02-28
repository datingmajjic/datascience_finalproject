import sqlite3
import pandas as pd

# load data
df = pd.read_csv('census_2009-10.csv')

# strip whitespace from headers
df.columns = df.columns.str.strip()

con = sqlite3.connect("census_stuff.db")

c = con.cursor()
c.execute('DROP TABLE IF EXISTS "people";')
# drop data into database
df.to_sql("people", con)


command1 = '''
SELECT
  *
FROM
  people
;
'''

# c.execute(command1)
# for r in c:
#     print(r)

# command2 = '''
# SELECT *
# FROM people
# WHERE (EDUC_SP IS NULL)
# OR (FAMUNIT_SP IS NULL)
# OR (SPLOC_SP IS NULL)
# OR (SPRULE_SP IS NULL)
# OR (BIRTHYR_SP IS NULL)
# OR (RACE_SP IS NULL)
# OR (RACED_SP IS NULL)
# OR (BPL_SP IS NULL)
# OR (BPLD_SP IS NULL)
# OR (EDUC_SP IS NULL)
# OR (EDUCD_SP IS NULL)
# OR (OCC_SP IS NULL)
# OR (IND_SP IS NULL)
# OR (INCTOT_SP IS NULL)
# OR (FTOTINC_SP IS NULL)
# OR (INCWAGE_SP IS NULL)
#
# '''
# c.execute(command2)
# for r in c:
#     print(r)

#delete rows where spouse is none
command3_delete_spouse = '''
DELETE
FROM people
WHERE (EDUC_SP IS NULL)
OR (FAMUNIT_SP IS NULL)
OR (SPLOC_SP IS NULL)
OR (SPRULE_SP IS NULL)
OR (BIRTHYR_SP IS NULL)
OR (RACE_SP IS NULL)
OR (RACED_SP IS NULL)
OR (BPL_SP IS NULL)
OR (BPLD_SP IS NULL)
OR (EDUC_SP IS NULL)
OR (EDUCD_SP IS NULL)
OR (OCC_SP IS NULL)
OR (IND_SP IS NULL)
OR (INCTOT_SP IS NULL)
OR (FTOTINC_SP IS NULL)
OR (INCWAGE_SP IS NULL)

'''
c.execute(command3_delete_spouse)

#print out database rows
# c.execute(command1)
# for r in c:
#     print(r)

command_onlyGrad = '''
SELECT EDUCD, EDUCD_SP
FROM people
WHERE (EDUCD_SP = 114 OR  EDUCD_SP = 115 OR EDUCD_SP = 115)
AND (EDUCD = 114 OR  EDUCD = 115 OR EDUCD = 115)
'''
#print out database rows of only masters/grad students
c.execute(command_onlyGrad)
for r in c:
    print(r)




con.close()
