import sqlite3
import pandas as pd

# load data
df = pd.read_csv('census_19-10.csv')

# strip whitespace from headers
df.columns = df.columns.str.strip()

con = sqlite3.connect("census_stuff.db")

c = con.cursor()
c.execute('DROP TABLE IF EXISTS "people";')
c.execute('DROP TABLE IF EXISTS "matchKaggleEduc";')
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

# command_onlyGrad = '''
# SELECT *
# FROM people
# WHERE (EDUCD_SP = 114 OR  EDUCD_SP = 115 OR EDUCD_SP = 116)
# AND (EDUCD = 114 OR  EDUCD = 115 OR EDUCD = 116)
#
# '''
# #print out database rows of only masters/grad students
# c.execute(command_onlyGrad)
# for r in c:
#     print(r)

command_onlyGrad = '''
DELETE
FROM people
WHERE (EDUCD_SP <> 114 AND EDUCD_SP <> 115 AND EDUCD_SP <> 116)
OR (EDUCD <> 114 AND EDUCD <> 115 AND EDUCD <> 116)
'''
c.execute(command_onlyGrad)


command_hasDeg = '''
DELETE
FROM people
WHERE DEGFIELD = 0 OR DEGFIELD_SP = 0
'''
c.execute(command_hasDeg)




#start converting eduction to right values
command_matchTable = '''
CREATE TABLE matchKaggleEduc(
    kaggleID INT,
    censusID INT
);
'''
command_insertVal = '''
INSERT INTO matchKaggleEduc
    (censusID, kaggleID)
VALUES
    (32,1),
    (37,2),
    (55,3),
    (52,3),
    (61,4),
    (25,5),
    (24,5),
    (21,5),
    (20,5),
    (34,6),
    (33,6),
    (64,7),
    (49,7),
    (19,8),
    (48,7),
    (15,7),
    (62,19),
    (23,9),
    (50,10),
    (51,10),
    (36,10),
    (11,10),
    (13,10),
    (54,13),
    (60,15),
    (26,16),
    (14,17),
    (59,18),
    (57,18),
    (56,18),
    (53,18),
    (41,18),
    (40,18),
    (38,18),
    (35,18),
    (29,18),
    (22,18);
'''

c.execute(command_matchTable);
c.execute(command_insertVal);


# command_joinTables = '''
# SELECT *
# FROM people as p
# LEFT JOIN matchKaggleEduc as m
# ON p.DEGFIELD = m.censusID
# '''
# c.execute(command_joinTables)



command5 = '''
ALTER TABLE people
ADD COLUMN kagEDUC INT;
'''
command6 = '''
ALTER TABLE people
ADD COLUMN kagEDUC_SP INT;
'''

command7 = '''
UPDATE people
SET kagEDUC =(
    SELECT kaggleID
    FROM matchKaggleEduc as m
    WHERE people.DEGFIELD = m.censusID
);
'''

command8 = '''
UPDATE people
SET kagEDUC_SP =(
    SELECT kaggleID
    FROM matchKaggleEduc as m
    WHERE people.DEGFIELD_SP = m.censusID
);

'''

c.execute(command5)
c.execute(command6)
c.execute(command7)
c.execute(command8)


#########
#now do careers
#########






con.commit()
con.close()
