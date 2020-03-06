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
fos_list = [['iid', 'field_cd']]
for index in range(1, len(kaggle_data)):
    iid = kaggle_data[index][0]
    if iid not in tracker_list:
        # Column position of field_cd is: 35
        fos_list.append([int(iid), int(kaggle_data[index][35])])
        tracker_list.append(iid)

for index in range(1, 18):
    new_column = str(index) + '_'

for entry in fos_list:
    print(entry)