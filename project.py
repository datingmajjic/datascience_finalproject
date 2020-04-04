import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# load data
df = pd.read_csv('census_19-10.csv')

# strip whitespace from headers
df.columns = df.columns.str.strip()

con = sqlite3.connect("census_stuff.db")

c = con.cursor()
c.execute('DROP TABLE IF EXISTS "people";')
c.execute('DROP TABLE IF EXISTS "matchKaggleEduc";')
c.execute('DROP TABLE IF EXISTS "matchKaggleCareer";')
c.execute('DROP TABLE IF EXISTS "original";')
c.execute('DROP TABLE IF EXISTS "actual_original";')
# drop data into database
# df.to_sql("actual_original", con)
df.to_sql("original", con)


command1 = '''
SELECT
  *
FROM
  original
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
FROM original
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

command_onlyGrad = '''
DELETE
FROM original
WHERE (EDUCD_SP <> 114 AND EDUCD_SP <> 115 AND EDUCD_SP <> 116)
OR (EDUCD <> 114 AND EDUCD <> 115 AND EDUCD <> 116)
'''
c.execute(command_onlyGrad)


command_hasDeg = '''
DELETE
FROM original
WHERE DEGFIELD = 0 OR DEGFIELD_SP = 0
'''
c.execute(command_hasDeg)

command_updateSex = '''
UPDATE original
SET SEX = 0
WHERE SEX = 2
'''
command_updateSexSpouse = '''
UPDATE original
SET SEX_SP = 0
WHERE SEX_SP = 2
'''
c.execute(command_updateSexSpouse)


command_updateRace1 = '''
UPDATE original
SET RACE = 1
WHERE RACE = 2
'''
command_updateRace2 = '''
UPDATE original
SET RACE = 2
WHERE RACE = 1
'''
command_updateRace3 = '''
UPDATE original
SET RACE = 4
WHERE RACE = 5 OR RACE = 6
'''
command_updateRace4 = '''
UPDATE original
SET RACE = 5
WHERE RACE = 3
'''
command_updateRace5 = '''
UPDATE original
SET RACE = 6
WHERE RACE = 7 OR RACE = 8 OR RACE = 9
'''
c.execute(command_updateRace1)
c.execute(command_updateRace2)
c.execute(command_updateRace3)
c.execute(command_updateRace4)
c.execute(command_updateRace5)


command_updateRaceSpouse1 = '''
UPDATE original
SET RACE_SP = 1
WHERE RACE_SP = 2
'''
command_updateRaceSpouse2 = '''
UPDATE original
SET RACE_SP = 2
WHERE RACE_SP = 1
'''
command_updateRaceSpouse3 = '''
UPDATE original
SET RACE_SP = 4
WHERE RACE_SP = 5 OR RACE_SP = 6
'''
command_updateRaceSpouse4 = '''
UPDATE original
SET RACE_SP = 5
WHERE RACE_SP = 3
'''
command_updateRaceSpouse5 = '''
UPDATE original
SET RACE_SP = 6
WHERE RACE_SP = 7 OR RACE_SP = 8 OR RACE_SP = 9
'''
c.execute(command_updateRaceSpouse1)
c.execute(command_updateRaceSpouse2)
c.execute(command_updateRaceSpouse3)
c.execute(command_updateRaceSpouse4)
c.execute(command_updateRaceSpouse5)





command9 = '''
CREATE TABLE people(
    YEAR INT,
    SAMPLE INT,
    SERIAL INT,
    PERNUM INT,
    BIRTHYR INT,
    EDUCD INT,
    DEGFIELD INT,
    OCC INT,
    BIRTHYR_SP INT,
    EDUCD_SP INT,
    DEGFIELD_SP INT,
    OCC_SP INT,
    SEX INT,
    SEX_SP INT,
    RACE INT,
    RACE_SP INT
);
'''
command10 = '''
INSERT INTO people (YEAR, SAMPLE, SERIAL, PERNUM, BIRTHYR, EDUCD, DEGFIELD, OCC, BIRTHYR_SP, EDUCD_SP, DEGFIELD_SP, OCC_SP, SEX, SEX_SP,
RACE, RACE_SP)
SELECT
YEAR, SAMPLE, SERIAL, PERNUM, BIRTHYR, EDUCD, DEGFIELD, OCC, BIRTHYR_SP, EDUCD_SP, DEGFIELD_SP, OCC_SP, SEX, SEX_SP, RACE, RACE_SP
FROM original
;
'''

c.execute(command9)
c.execute(command10)

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
    (62,8),
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

#start converting eduction to right values
command_matchTableC = '''
CREATE TABLE matchKaggleCareer(
    censusID INT,
    kaggleID INT,
    minVAL INT,
    maxVAL INT
);
'''



#kaggleID 0 is unemployed, I added this bc interesting
command_insertValC = '''
INSERT INTO matchKaggleCareer
    (censusID, kaggleID, minVAL, maxVAL)
VALUES
    (0, 0, NULL, NULL),
    ( NULL, 1, 2100, 2140),
    (NULL, 2, 1600, 1860),
    (1820, 3, NULL, NULL),
    (NULL, 4, 3000, 3540),
    (NULL, 4, 3600, 3655),
    (NULL, 5, 1310, 1560),
    (NULL, 5, 1000, 1240),
    (NULL, 6, 2600, 2920),
    (NULL, 7, 0020, 0430),
    (NULL, 7, 0500, 0740),
    (NULL, 7, 0800, 0950),
    (NULL, 7, 4700, 4965),
    (4920, 8, NULL, NULL),
    (0810, 8, NULL, NULL),
    (NULL, 11, 2000, 2060),
    (NULL, 11, 3700, 3950),
    (4650, 11, NULL, NULL),
    (3230, 12, NULL, NULL),
    (0010, 13, NULL, NULL),
    (2720, 14, NULL, NULL),
    (NULL, 15, 1900, 1965),
    (1840, 15, NULL, NULL),
    (NULL, 15, 2200, 2550),
    (NULL, 15, 4000, 4150),
    (NULL, 15, 4200, 4250),
    (NULL, 15, 4300, 4640),
    (NULL, 15, 5000, 5940),
    (NULL, 15, 6000, 6130),
    (NULL, 15, 6200, 6940),
    (NULL, 15, 7000, 7610),
    (NULL, 15, 7700, 8950),
    (NULL, 15, 9000, 9750),
    (NULL, 15, 9800, 9920),
    (2810, 16, NULL, NULL),
    (2840, 16, NULL, NULL),
    (2850, 16, NULL, NULL),
    (1300, 16, NULL, NULL);
'''

c.execute(command_matchTableC);
c.execute(command_insertValC);


con.commit()
#########
#add columns for careers and join
command5C = '''
ALTER TABLE people
ADD COLUMN kagOCC INT;
'''
command6C = '''
ALTER TABLE people
ADD COLUMN kagOCC_SP INT;
'''

command7C1 = '''
UPDATE people
SET kagOCC =(
    SELECT kaggleID
    FROM matchKaggleCareer as m
    WHERE m.censusID IS NOT NULL AND people.OCC = m.censusID
);
'''
command7C2 = '''
UPDATE people

SET kagOCC = (
    SELECT m.kaggleID
    FROM matchKaggleCareer as m
    WHERE
    (m.maxVAL IS NOT NULL
    AND m.minVAL IS NOT NULL
    AND (people.OCC <= m.maxVAL
    AND people.OCC >= m.minVAL))
)
WHERE people.kagOCC IS NULL
;
'''

command8C1 = '''
UPDATE people
SET kagOCC_SP =(
    SELECT kaggleID
    FROM matchKaggleCareer as m
    WHERE m.censusID IS NOT NULL AND people.OCC_SP = m.censusID
);
'''
command8C2 = '''
UPDATE people

SET kagOCC_SP = (
    SELECT m.kaggleID
    FROM matchKaggleCareer as m
    WHERE
    (m.maxVAL IS NOT NULL
    AND m.minVAL IS NOT NULL
    AND (people.OCC_SP <= m.maxVAL
    AND people.OCC_SP >= m.minVAL))
)
WHERE people.kagOCC_SP IS NULL
;
'''

c.execute(command5C)
c.execute(command6C)
c.execute(command7C1)
c.execute(command7C2)
c.execute(command8C1)
c.execute(command8C2)
con.commit()


# MAKING GRAPHS FOR DISTRIBUTION OF COLLEGE MAJORS
#(Based on ACS codes)
command1 = '''
SELECT
  DEGFIELD, COUNT(DEGFIELD)
FROM
  people
GROUP BY
    DEGFIELD
;
'''

# c.execute(command1)
# degrees = []
# num_per_degree = []
# for r in c:
#     degrees.append(str(r[0]))
#     num_per_degree.append(r[1])
#
# x_pos = np.arange(len(degrees))
# plt.bar(degrees, num_per_degree, align='center', alpha=0.5)
# plt.title('Distribution of College Degree Fields for Married Individuals in New York who have obtained a degree higher than a Bachelor’s')
# plt.ylabel('Number of people')
# plt.xlabel('College Degree Field Code (based on ACS PUMS data)')
# xlocs, xlabs = plt.xticks()
# for i, v in enumerate(num_per_degree):
#     plt.text(xlocs[i] - 0.5, v + 0.01, str(v))
# plt.show()

#(Based on Kaggle codes)
command1 = '''
SELECT
  kagEDUC, COUNT(kagEDUC)
FROM
  people
GROUP BY
    kagEDUC
;
'''
# c.execute(command1)
# degrees = []
# num_per_degree = []
# for r in c:
#     if r[0]!=None:
#         degrees.append(str(r[0]))
#         num_per_degree.append(r[1])
#
# x_pos = np.arange(len(degrees))
# plt.bar(degrees, num_per_degree, align='center', alpha=0.5)
# plt.title('Distribution of College Degree Fields for Married Individuals in New York who have obtained a degree higher than a Bachelor’s')
# plt.ylabel('Number of people')
# plt.xlabel('College Degree Field Code (based on Kaggle data)')
# xlocs, xlabs = plt.xticks()
# for i, v in enumerate(num_per_degree):
#     plt.text(xlocs[i] - 0.5, v + 0.01, str(v))
# plt.show()

# MAKING GRAPHS FOR DISTRIBUTION OF OCCUPATIONS

command1 = '''
SELECT
  OCC, COUNT(*)
FROM
  people
GROUP BY
    OCC
;
'''
# c.execute(command1)
# occupations = []
# num_per_occ = []
# for r in c:
#     occupations.append(str(r[0]))
#     num_per_occ.append(r[1])
#
# x_pos = np.arange(len(occupations))
# plt.bar(occupations, num_per_occ, align='center', alpha=0.5)
# plt.title('Distribution of Occupations for Married Individuals in New York who have obtained a degree higher than a Bachelor’s')
# plt.ylabel('Number of people')
# plt.xlabel('Occupation Code (based on ACS IPUMS data)')
# xlocs, xlabs = plt.xticks(rotation=90)
# for i, v in enumerate(num_per_occ):
#     plt.text(xlocs[i] - 0.5, v + 0.01, str(v))
# plt.show()



command1 = '''
SELECT
  kagOCC, COUNT(kagOCC)
FROM
  people
GROUP BY
    kagOCC
;
'''
# c.execute(command1)
# occupations = []
# num_per_occ = []
# for r in c:
#     if r[0]!=None:
#         occupations.append(str(r[0]))
#         num_per_occ.append(r[1])
#
# x_pos = np.arange(len(occupations))
# plt.bar(occupations, num_per_occ, align='center', alpha=0.5)
# plt.title('Distribution of Occupations for Married Individuals in New York who have obtained a degree higher than a Bachelor’s')
# plt.ylabel('Number of people')
# plt.xlabel('Occupation Code (based on Kaggle data)')
# xlocs, xlabs = plt.xticks()
# for i, v in enumerate(num_per_occ):
#     plt.text(xlocs[i] - 0.5, v + 0.01, str(v))
# plt.show()



con.close()
