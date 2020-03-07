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

tracker_list = []

# Age and race list
demographics_list = [['iid', 'age', 'race']]
for index in range(1, len(kaggle_data)):
    iid = kaggle_data[index][0]
    if iid not in tracker_list:
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



# for index in range(1, 18):
#     new_column = str(index) + '_'

for entry in fos_list:
    print(entry)