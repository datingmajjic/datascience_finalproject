import sqlite3
import chardet
import pandas as pd
import csv

# Load Kaggle data
kaggle_data = []

with open('Speed_Dating_Data.csv', 'r', encoding='mac_roman', newline='') as csvDataFile:
    csvReader = csv.reader(csvDataFile, delimiter = ',')
    for row in csvReader:
        kaggle_data.append(row)

tracker_list = []

# Field of study and career list
occupation_list = [['iid', 'field_cd', 'career_c']]

for index in range(1, len(kaggle_data)):
    iid = kaggle_data[index][0]
    if iid not in tracker_list:
        # iid 118 does not exist in kaggle_data :(
        if iid == '119':
            occupation_list.append([118, None, None])
        # Column position of field_cd is: 35
        # Column position of career_c is: 49
        if kaggle_data[index][35] != '' and kaggle_data[index][49] != '':
            occupation_list.append([int(iid), int(kaggle_data[index][35]), int(kaggle_data[index][49])])
        else:
            if kaggle_data[index][35] == '' and kaggle_data[index][49] == '':
                occupation_list.append([int(iid), None, None])
            elif kaggle_data[index][35] == '':
                occupation_list.append([int(iid), None, int(kaggle_data[index][49])])
            elif kaggle_data[index][49] == '':
                occupation_list.append([int(iid), int(kaggle_data[index][35]), None])
        tracker_list.append(iid)

# Determine number of iids in dataset
num_iids = len(tracker_list)
tracker_list = []

# Age and race list
demographics_list = [['iid', 'age', 'race']]

for index in range(1, len(kaggle_data)):
    iid = kaggle_data[index][0]
    if iid not in tracker_list:
        # iid 118 does not exist in kaggle_data :(
        if iid == '119':
            demographics_list.append([118, None, None])
        # Column position of age is: 33
        # Column position of race is: 39
        if kaggle_data[index][33] != '' and kaggle_data[index][39] != '':
            demographics_list.append([int(iid), int(kaggle_data[index][33]), int(kaggle_data[index][39])])
        else:
            if kaggle_data[index][33] == '' and kaggle_data[index][39] == '':
                demographics_list.append([int(iid), None, None])
            elif kaggle_data[index][33] == '':
                demographics_list.append([int(iid), None, int(kaggle_data[index][39])])
            elif kaggle_data[index][39] == '':
                demographics_list.append([int(iid), int(kaggle_data[index][35]), None])
        tracker_list.append(iid)

participant_info = [a + b[1:] for (a,b) in zip(occupation_list, demographics_list)]

###############################################################################
# Create a database for how each iid rated a certain field of study
results = ['decision', 'attractive', 'sincere', 'intelligent', 'fun', 'ambitious', 'share', 'like', 'probability', 'total']
fos_date_results = []
for index in range(1, 19):
    for result in results:
        new_column = str(index) + '_' + result
        fos_date_results.append(new_column)

fos_date_results = [['iid'] + fos_date_results]
for index in range(num_iids + 1):
    new_iid = [index + 1]
    scores = [None for x in fos_date_results[0][1:]]
    new_entry = new_iid + scores
    fos_date_results.append(new_entry)

previous_iid = 0
total_tracker = [None for x in range(len(fos_date_results[0]))]

for entry in kaggle_data[1:]:
    # Column position of iid is: 0
    current_iid = int(entry[0])

    if current_iid != previous_iid and previous_iid != 0:
        new = [previous_iid]
        for (num, den) in zip(fos_date_results[previous_iid][1:], total_tracker[1:]):
            if den != None and num != None:
                new.append(num / den)
            else:
                new.append(None)
        fos_date_results[previous_iid] = new
        total_tracker = [0 for x in range(len(fos_date_results[0]))]

    # Column position of pid is: 11
    if entry[11] == '':
        previous_iid = current_iid
        continue
    else:
        partner_iid = int(entry[11])

    partner_field = participant_info[partner_iid][1]
    if partner_field == None:
        previous_iid = current_iid
        continue

    # Indices for where to find findings in entry:
    # Column position of dec/decision is: 97
    # Column position of prob/probability is: 105
    entry_indices = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106]

    # Index for where to start logging findings in fos_date_results:
    fdr_start_index = ((partner_field - 1) * 10) + 1

    for index in entry_indices:
        if index != 106:
            if entry[index] != '':
                if fos_date_results[current_iid][fdr_start_index] == None:
                    fos_date_results[current_iid][fdr_start_index] = 0
                if total_tracker[fdr_start_index] == None:
                    total_tracker[fdr_start_index] = 0

                fos_date_results[current_iid][fdr_start_index] += float(entry[index])
                total_tracker[fdr_start_index] += 1
        else:
            if fos_date_results[current_iid][fdr_start_index] == None:
                fos_date_results[current_iid][fdr_start_index] = 0
            if total_tracker[fdr_start_index] == None:
                total_tracker[fdr_start_index] = 0

            fos_date_results[current_iid][fdr_start_index] += 1
            total_tracker[fdr_start_index] = 1

        fdr_start_index += 1

    previous_iid = current_iid

new = [previous_iid]
for (num, den) in zip(fos_date_results[previous_iid][1:], total_tracker[1:]):
    if den != None and num != None:
        new.append(num / den)
    else:
        new.append(None)
fos_date_results[previous_iid] = new
# fos_date_results is where data for results based on field of study is stored
###############################################################################

###############################################################################
# Create a database for how each iid rated a certain occupation
results = ['decision', 'attractive', 'sincere', 'intelligent', 'fun', 'ambitious', 'share', 'like', 'probability', 'total']
career_date_results = []
for index in range(1, 18):
    for result in results:
        new_column = str(index) + '_' + result
        career_date_results.append(new_column)

career_date_results = [['iid'] + career_date_results]
for index in range(num_iids + 1):
    new_iid = [index + 1]
    scores = [None for x in career_date_results[0][1:]]
    new_entry = new_iid + scores
    career_date_results.append(new_entry)

previous_iid = 0
total_tracker = [None for x in range(len(career_date_results[0]))]

for entry in kaggle_data[1:]:
    # Column position of iid is: 0
    current_iid = int(entry[0])

    if current_iid != previous_iid and previous_iid != 0:
        new = [previous_iid]
        for (num, den) in zip(career_date_results[previous_iid][1:], total_tracker[1:]):
            if den != None and num != None:
                new.append(num / den)
            else:
                new.append(None)
        career_date_results[previous_iid] = new
        total_tracker = [None for x in range(len(career_date_results[0]))]

    # Column position of pid is: 11
    if entry[11] == '':
        previous_iid = current_iid
        continue
    else:
        partner_iid = int(entry[11])

    partner_career = participant_info[partner_iid][2]
    if partner_career == None:
        previous_iid = current_iid
        continue

    # Indices for where to find findings in entry:
    # Column position of dec/decision is: 97
    # Column position of prob/probability is: 105
    entry_indices = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106]

    # Index for where to start logging findings in career_date_results:
    career_start_index = ((partner_career - 1) * 10) + 1

    for index in entry_indices:
        if index != 106:
            if entry[index] != '':
                if career_date_results[current_iid][career_start_index] == None:
                    career_date_results[current_iid][career_start_index] = 0
                if total_tracker[career_start_index] == None:
                    total_tracker[career_start_index] = 0

                career_date_results[current_iid][career_start_index] += float(entry[index])
                total_tracker[career_start_index] += 1
        else:
            if career_date_results[current_iid][career_start_index] == None:
                career_date_results[current_iid][career_start_index] = 0
            if total_tracker[career_start_index] == None:
                total_tracker[career_start_index] = 0

            career_date_results[current_iid][career_start_index] += 1
            total_tracker[career_start_index] = 1

        career_start_index += 1

    previous_iid = current_iid

new = [previous_iid]
for (num, den) in zip(career_date_results[previous_iid][1:], total_tracker[1:]):
    if den != None and num != None:
        new.append(num / den)
    else:
        new.append(None)
career_date_results[previous_iid] = new
# career_date_results is where data for results based on intended career is stored
###############################################################################

# ###############################################################################
# # Create a database for how each iid rated a certain race
# results = ['decision', 'attractive', 'sincere', 'intelligent', 'fun', 'ambitious', 'share', 'like', 'probability', 'total']
# race_date_results = []
# for index in range(1, 7):
#     for result in results:
#         new_column = str(index) + '_' + result
#         race_date_results.append(new_column)

# race_date_results = [['iid'] + race_date_results]
# for index in range(num_iids + 1):
#     new_iid = [index + 1]
#     scores = [0 for x in race_date_results[0][1:]]
#     new_entry = new_iid + scores
#     race_date_results.append(new_entry)

# previous_iid = 0
# total_tracker = [0 for x in range(len(race_date_results[0]))]

# for entry in kaggle_data[1:]:
#     # Column position of iid is: 0
#     current_iid = int(entry[0])

#     if current_iid != previous_iid and previous_iid != 0:
#         new = [previous_iid]
#         for (num, den) in zip(race_date_results[previous_iid][1:], total_tracker[1:]):
#             if den != 0:
#                 new.append(num / den)
#             else:
#                 new.append(0)
#         race_date_results[previous_iid] = new
#         total_tracker = [0 for x in range(len(race_date_results[0]))]

#     # Column position of pid is: 11
#     if entry[11] == '':
#         previous_iid = current_iid
#         continue
#     else:
#         partner_iid = int(entry[11])

#     partner_race = participant_info[partner_iid][4]
#     if partner_race == None:
#         previous_iid = current_iid
#         continue

#     # Indices for where to find findings in entry:
#     # Column position of dec/decision is: 97
#     # Column position of prob/probability is: 105
#     entry_indices = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106]

#     # Index for where to start logging findings in race_date_results:
#     race_start_index = ((partner_race - 1) * 10) + 1

#     for index in entry_indices:
#         if index != 106:
#             if entry[index] != '':
#                 race_date_results[current_iid][race_start_index] += float(entry[index])
#                 total_tracker[race_start_index] += 1
#         else:
#             race_date_results[current_iid][race_start_index] += 1
#             total_tracker[race_start_index] = 1

#         race_start_index += 1

#     previous_iid = current_iid

# new = [previous_iid]
# for (num, den) in zip(race_date_results[previous_iid][1:], total_tracker[1:]):
#     if den != 0:
#         new.append(num / den)
#     else:
#         new.append(0)
# race_date_results[previous_iid] = new

# for entry in race_date_results:
#     print(entry)
# # race_date_results is where data for results based on race is stored
# ###############################################################################

###############################################################################
# Insert array into sql

# Create connection to database
conn = sqlite3.connect('kaggle_clean.db')
c = conn.cursor()

# Added by student (because of sql lab):
c.execute('PRAGMA foreign_keys = ON')

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "field_of_study";')
c.execute('DROP TABLE IF EXISTS "career";')
c.execute('DROP TABLE IF EXISTS "demographics";')

# Commands to create the 'field_of_study' and 'career' tables
commands = ['decision', 'attractive', 'sincere', 'intelligent', 'fun', 'ambitious', 'share', 'like', 'probability', 'total']
create_field_of_study = '''CREATE TABLE field_of_study (iid INT PRIMARY KEY NOT NULL,'''
create_career = '''CREATE TABLE career (iid INT PRIMARY KEY NOT NULL,'''

for index in range(1, 19):
    for entry in commands:
        create_field_of_study = create_field_of_study + ' "' + str(index) + '_' + entry + '" FLOAT,'
create_field_of_study = create_field_of_study[:-1] + ');'

for index in range(1, 18):
    for entry in commands:
        create_career = create_career + ' "' + str(index) + '_' + entry + '" FLOAT,'
create_career = create_career[:-1] + ');'

create_demographics = '''CREATE TABLE demographics
                         (iid INT PRIMARY KEY NOT NULL,
                         field_cd INT,
                         career_c INT,
                         age INT,
                         race INT);'''

# Execute the create tables commands
c.execute(create_field_of_study)
conn.commit()

c.execute(create_career)
conn.commit()

c.execute(create_demographics)
conn.commit()

# Insert values into tables
for entry in fos_date_results[1:]:
    insert_fos = 'INSERT INTO field_of_study VALUES ('
    for value in entry:
        if value == None:
            insert_fos += 'NULL'
        else:
            insert_fos += str(value)
        insert_fos += ', '
    insert_fos = insert_fos[:-2] + ');'

    # Execute and commit the commands
    c.execute(insert_fos)
    conn.commit()

for entry in career_date_results[1:]:
    insert_career = 'INSERT INTO career VALUES ('
    for value in entry:
        if value == None:
            insert_career += 'NULL'
        else:
            insert_career += str(value)
        insert_career += ', '
    insert_career = insert_career[:-2] + ');'

    # Execute and commit the commands
    c.execute(insert_career)
    conn.commit()

for entry in participant_info[1:]:
    insert_demographic = 'INSERT INTO demographics VALUES ('
    for value in entry:
        if value == None:
            insert_demographic += 'NULL'
        else:
            insert_demographic += str(value)
        insert_demographic += ', '
    insert_demographic = insert_demographic[:-2] + ');'

    # Execute and commit the commands
    c.execute(insert_demographic)
    conn.commit()









