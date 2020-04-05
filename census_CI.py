import sqlite3
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare

#counts the number of ppl with that career in both datasets
def countField(dfC, dfK, field):
    #census
    # print(dfC["kagEDUC"])
    countCensus = 0
    for i in range(len(dfC)):
        if dfC.loc[i, "kagEDUC"] == field:
            countCensus += 1
    countKaggle = 0
    for i in range(len(dfK)):
        if dfK.loc[i, "field_cd"] == field:
            countKaggle += 1

    return (countCensus, countKaggle)

def countOCC(dfC, dfK, career):
    #census
    # print(dfC["kagEDUC"])
    countCensus = 0
    for i in range(len(dfC)):
        if dfC.loc[i, "kagOCC"] == career:
            countCensus += 1
    countKaggle = 0
    for i in range(len(dfK)):
        if dfK.loc[i, "career_c"] == career:
            countKaggle += 1

    return (countCensus, countKaggle)


if __name__=='__main__':
    def load_file(file_path, command):
        con = sqlite3.connect(file_path)
        data = pd.read_sql_query(command, con)
        return data

    dfC = load_file("census_stuff.db", "SELECT * FROM people")
    dfK = load_file("kaggle_clean.db", "SELECT * FROM demographics")

    #18 field
    obsCensusField = []
    obsKagField = []

    for i in range(1,19):
        countFCensus, countFKag = countField(dfC, dfK, i)
        obsCensusField.append(countFCensus)
        obsKagField.append(countFKag)
    ExpectedC = [(sum(obsCensusField))/18]*18
    ExpectedK = [(sum(obsKagField))/18]*18
    print("fields:")
    print(chisquare(obsCensusField, f_exp = ExpectedC))
    print(chisquare(obsKagField, f_exp = ExpectedK))


    #17 occupation
    obsCensusOCC = []
    obsKagOCC = []

    for i in range(1,18):
        countOCensus, countOKag = countOCC(dfC, dfK, i)
        obsCensusOCC.append(countOCensus)
        obsKagOCC.append(countOKag)
    ExpectedCO = [sum(obsCensusOCC)/17]*17
    ExpectedKO = [sum(obsKagOCC)/17]*17
    print("occupations:")
    print(chisquare(obsCensusOCC, f_exp = ExpectedCO))
    print(chisquare(obsKagOCC, f_exp = ExpectedKO))







    # print(countO)
