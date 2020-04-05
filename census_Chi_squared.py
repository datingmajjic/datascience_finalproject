import sqlite3
import pandas as pd
import math
# import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare
from scipy import stats

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

def sameOCCKaggle(demo, career):

    #first row is date
    #second row is not date
    #columns are the occupations
    occupations = np.zeros((2,17))
    for i in range(len(demo)):
        id = demo.loc[i, "iid"]
        occ =  demo.loc[i, "career_c"]
        if not math.isnan(id) and  not math.isnan(occ):

            colname = str(int(occ))+"_decision"
            for j in range(len(career)):
                #finding the person by their id in the career table
                if career.loc[j,"iid"] == id:
                    #finding if they would date the person with the same career
                    if career.loc[j,colname] > 0.5 and not math.isnan(career.loc[j,colname]):
                        # dateAgain += 1
                        occupations[0][int(occ-1)]+= 1
                    else:
                        # notDate += 1
                        occupations[1][int(occ-1)]+= 1
    return occupations

def sameOCCCensus(dfC):
    occupations = np.zeros((2,17))

    for i in range(len(dfC)):
        yourOCC = dfC.loc[i, "kagOCC"]
        spouseOCC = dfC.loc[i, "kagOCC_SP"]
        if not math.isnan(yourOCC) and not math.isnan(spouseOCC):
            if yourOCC == spouseOCC :
                occupations[0][int(yourOCC-1)]+= 1
            else:
                occupations[1][int(yourOCC-1)]+= 1

    return occupations

def sameFieldCensus(dfC):
    fields = np.zeros((2,18))

    for i in range(len(dfC)):
        yourF = dfC.loc[i, "kagEDUC"]
        spouseF = dfC.loc[i, "kagEDUC_SP"]
        if not math.isnan(yourF) and not math.isnan(spouseF):
            if yourF == spouseF :
                fields[0][int(yourF-1)]+= 1
            else:
                fields[1][int(yourF-1)]+= 1

    return fields

def sameFieldKaggle(demo, field):
    #first row is date
    #second row is not date
    #columns are the occupations
    fields = np.zeros((2,18))
    for i in range(len(demo)):
        id = demo.loc[i, "iid"]
        f =  demo.loc[i, "field_cd"]
        if not math.isnan(id) and  not math.isnan(f):

            colname = str(int(f))+"_decision"
            for j in range(len(field)):
                #finding the person by their id in the career table
                if field.loc[j,"iid"] == id:
                    #finding if they would date the person with the same career
                    if field.loc[j,colname] > 0.5 and not math.isnan(field.loc[j,colname]):
                        # dateAgain += 1
                        fields[0][int(f-1)]+= 1
                    else:
                        # notDate += 1
                        fields[1][int(f-1)]+= 1
    return fields


if __name__=='__main__':
    def load_file(file_path, command):
        con = sqlite3.connect(file_path)
        data = pd.read_sql_query(command, con)
        return data

    dfC = load_file("census_stuff.db", "SELECT * FROM people")
    dfK = load_file("kaggle_clean.db", "SELECT * FROM demographics")
    dfKCareer = load_file("kaggle_clean.db", "SELECT * FROM career")
    dfKField = load_file("kaggle_clean.db", "SELECT * FROM field_of_study")

    #18 field
    obsCensusField = []
    obsKagField = []

    for i in range(1,19):
        countFCensus, countFKag = countField(dfC, dfK, i)
        obsCensusField.append(countFCensus)
        obsKagField.append(countFKag)

    TotalColSum = np.add(np.array(obsCensusField), np.array(obsKagField))
    # print('check')
    # print(TotalColSum)

    TotalSamples = sum(obsCensusField) + sum(obsKagField)
    ExpectedC = []
    ExpectedK = []
    for i in range(18):
        C = (sum(obsCensusField)) * TotalColSum[i] / TotalSamples
        ExpectedC.append(C)
        K = (sum(obsKagField)) * TotalColSum[i] / TotalSamples
        ExpectedK.append(K)

    print("fields:")
    print(chisquare([obsCensusField, obsKagField], f_exp = [ExpectedC, ExpectedK]))
    # print(chisquare(obsKagField, f_exp = ExpectedK))

    # testing = np.array([obsCensusField, obsKagField])
    # print(stats.chi2_contingency(testing))

    #17 occupation
    obsCensusOCC = []
    obsKagOCC = []

    for i in range(1,18):
        countOCensus, countOKag = countOCC(dfC, dfK, i)
        obsCensusOCC.append(countOCensus)
        obsKagOCC.append(countOKag)

    TotalSamplesO = sum(obsCensusOCC) + sum(obsKagOCC)
    TotalColSumOCC = np.add(np.array(obsCensusOCC), np.array(obsKagOCC))

    ExpectedCO = []
    ExpectedKO = []
    for i in range(17):
        C = (sum(obsCensusOCC)) * TotalColSumOCC[i] / TotalSamplesO
        ExpectedCO.append(C)
        K = (sum(obsKagOCC)) * TotalColSumOCC[i] / TotalSamplesO
        ExpectedKO.append(K)


    print("occupations:")
    print(chisquare([obsCensusOCC, obsKagOCC], f_exp = [ExpectedCO, ExpectedKO]))
    # print(chisquare(obsKagOCC, f_exp = ExpectedKO))


    ####################################
    #chi square for marrying/dating same careers

    sameOccupationKaggle = sameOCCKaggle(dfK, dfKCareer)
    sameOccupationCensus = sameOCCCensus(dfC)

    # occ = occ -1

    for occ in range(17): #17

        obsC = [sameOccupationCensus[0][occ], sameOccupationCensus[1][occ]]
        obsK = [sameOccupationKaggle[0][occ], sameOccupationKaggle[1][occ]]

        colTot = obsC + obsK
        ActualTotal = sum(obsC) + sum(obsK)
        ExpC = [sum(obsC) + colTot[0] /ActualTotal, sum(obsC) + colTot[1] /ActualTotal]
        ExpK = [sum(obsK) + colTot[0] /ActualTotal, sum(obsK) + colTot[1] /ActualTotal]
        print("occupation = " + str(occ +1))
        print(chisquare([obsC, obsK], f_exp = [ExpC, ExpK]))



    sameFKaggle = sameFieldKaggle(dfK, dfKField)
    # print(len(sameFKaggle[0]))
    sameFCensus = sameFieldCensus(dfC)
    # print(len(sameFCensus[0]))



    for field in range(18):

        obsC = [sameFCensus[0][field], sameFCensus[1][field]]
        obsK = [sameFKaggle[0][field], sameFKaggle[1][field]]

        colTot = obsC + obsK
        ActualTotal = sum(obsC) + sum(obsK)
        ExpC = [sum(obsC) + colTot[0] /ActualTotal, sum(obsC) + colTot[1] /ActualTotal]
        ExpK = [sum(obsK) + colTot[0] /ActualTotal, sum(obsK) + colTot[1] /ActualTotal]
        print("field= " + str(field +1))
        print(chisquare([obsC, obsK], f_exp = [ExpC, ExpK]))









    # print(countO)
