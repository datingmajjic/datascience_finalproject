import sqlite3
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare
from scipy import stats

#counts the number of ppl with this field in both datasets
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

#counts the number of ppl with this occupation in both datasets
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
'''
counts the number of people in the Kaggle dataset who would go on another date
 with someone of the same occupation

    returns array where each column is an occupation and row 0 represents the
    number of people who would go on another date with the same occupation and
    row 1 represents the number of  people who would not go on another date with
    the same occupation
'''
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
                    if career.loc[j,colname] > 0.5:
                    # if career.loc[j,colname] > 0.5 and not math.isnan(career.loc[j,colname]):
                        # dateAgain += 1
                        occupations[0][int(occ-1)]+= 1
                    # else:
                    elif not math.isnan(career.loc[j,colname]):
                        # notDate += 1
                        occupations[1][int(occ-1)]+= 1
    return occupations
'''
counts the number of people in the Census dataset who married someone of the same occupation

    returns array where each column is an occupation and row 0 represents the
    number of people who married the same occupation and
    row 1 represents the number of  people who did not marry someone with the
    same occupation
'''
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

'''
counts the number of people in the Census dataset who married someone of the same field

    returns array where each column is a field and row 0 represents the
    number of people who married the same field and
    row 1 represents the number of  people who did not marry someone with the
    same field
'''
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

    return np.asarray(fields)
'''
counts the number of people in the Kaggle dataset who would go on another date
 with someone of the same field

    returns array where each column is an field and row 0 represents the
    number of people who would go on another date with the same field and
    row 1 represents the number of people who would not go on another date with
    the same field
'''
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
                    if field.loc[j,colname] > 0.5:
                        # dateAgain += 1
                        fields[0][int(f-1)]+= 1
                    elif not math.isnan(field.loc[j,colname]):
                        # notDate += 1
                        fields[1][int(f-1)]+= 1
    return np.asarray(fields)

'''
counts the number of people in the Kaggle dataset who would go on another date
 with someone of the same occupation

returns information as list containing number of people who would go on another
 date with someone of the same occupation and the number of people who would not go on another
date with someone of the same occupation
'''
def sameOCCKaggleAll(demo, career):

    #first row is date
    #second row is not date
    #columns are the occupations
    dateAgain = 0
    notDate = 0

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
                        dateAgain += 1
                    else:
                        notDate += 1
    return [dateAgain, notDate]
'''
counts the number of people in the Census dataset who married someone
 with the same occupation

returns information as list containing number of people who married someone of
the same occupation and the number of people who dod not marry someone with the
same occupation
'''
def sameOCCCensusAll(dfC):
    Married = 0
    notMarried = 0
    for i in range(len(dfC)):
        yourOCC = dfC.loc[i, "kagOCC"]
        spouseOCC = dfC.loc[i, "kagOCC_SP"]
        if not math.isnan(yourOCC) and not math.isnan(spouseOCC):
            if yourOCC == spouseOCC :
                Married+= 1
            else:
                notMarried+= 1

    return [Married, notMarried]

'''
counts the number of people in the Census dataset who married someone
 with the same field

returns information as list containing number of people who married someone of
the same field and the number of people who dod not marry someone with the
same field
'''
def sameFieldCensusAll(dfC):
    married = 0
    notMarried = 0
    for i in range(len(dfC)):
        yourF = dfC.loc[i, "kagEDUC"]
        spouseF = dfC.loc[i, "kagEDUC_SP"]
        if not math.isnan(yourF) and not math.isnan(spouseF):
            if yourF == spouseF :
                married += 1
            else:
                notMarried += 1

    return [married, notMarried]

'''
counts the number of people in the Kaggle dataset who would go on another date
 with someone of the same field

returns information as list containing number of people who would go on another
 date with someone of the same field and the number of people who would not go on another
date with someone of the same field
'''
def sameFieldKaggleAll(demo, field):
    dateAgain = 0
    notDate = 0
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
                        dateAgain += 1
                    else:
                        notDate += 1
    return [dateAgain, notDate]

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

if __name__=='__main__':
    def load_file(file_path, command):
        con = sqlite3.connect(file_path)
        data = pd.read_sql_query(command, con)
        return data

    dfC = load_file("census_stuff.db", "SELECT * FROM people")
    dfK = load_file("kaggle_clean.db", "SELECT * FROM demographics")
    dfKCareer = load_file("kaggle_clean.db", "SELECT * FROM career")
    dfKField = load_file("kaggle_clean.db", "SELECT * FROM field_of_study")

##############################################################################################
#Chi-squared test comparing the number of people who marry the same occupation in both datasets
##############################################################################################

    obsKO = sameOCCKaggleAll(dfK, dfKCareer)
    obsCO = sameOCCCensusAll(dfC)
    obsO = np.array((obsKO,obsCO))
    chi2, p, dof, expected = stats.chi2_contingency(obsO)
    print("chi squared test comparing same occuptions on both datasets")
    print("p-value = " + str(p))

##############################################################################################
#Chi-squared test comparing the number of people who marry the same field in both datasets
##############################################################################################
    obsKF = sameFieldKaggleAll(dfK, dfKField)
    obsCF = sameFieldCensusAll(dfC)
    obsF = np.array((obsKF,obsCF))
    chi2, p, dof, expected = stats.chi2_contingency(obsF)
    print("chi squared test comparing same fields on both datasets")
    print("p-value = " + str(p))

    '''
    listL columns each represent one occupation and row 0 stores the number of
    people who would data/marry same occupation and row 1 stores the number of
    people who would data/marry different occupation
    '''
    sameOccupationKaggle = sameOCCKaggle(dfK, dfKCareer)
    sameOccupationCensus = sameOCCCensus(dfC)


##############################################################################################
#chi-squared test comparing the proportion of people who are a specific occuption and marry
#the same occupation to the total number of people who marry the same occupation in each dataset
##############################################################################################

    print("Chi squared tests comparing proportion of each occupation with the proportion from the Kaggle dataset")
    for occ in range(17):
        obs = np.array(sameOccupationKaggle[0][occ], sameOccupationKaggle[1][occ])
        stat, p = chisquare(obs, f_exp = obsKO)
        print("occupation = " + str(occ +1) + " p-value = " + str(p))

    print()

    print("Chi squared tests comparing proportion of each occupation with the proportion from the Census dataset")
    for occ in range(17):
        obs = np.array(sameOccupationCensus[0][occ], sameOccupationCensus[1][occ])
        proportion = obsCO[0]/(sum(obsCO))
        exp = [obs[0]*sum(obs), obs[1]*sum(obs)]
        stat, p = chisquare(obs, f_exp = exp)
        print("occupation = " + str(occ +1) + " p-value = " + str(p))

    print()
##############################################################################################
#chi-squared test comparing the proportion of people who are a specific field and marry
#the same field to the total number of people who marry the same field in each dataset
##############################################################################################
    '''
    listL columns each represent one major and row 0 stores the number of
    people who would data/marry same major and row 1 stores the number of
    people who would data/marry different major
    '''
    sameFKaggle = sameFieldKaggle(dfK, dfKField)
    sameFCensus = sameFieldCensus(dfC)

    print("Chi squared tests comparing proportion of each field with the proportion from the Kaggle dataset")
    for field in range(18):
        obs = np.array(sameFKaggle[0][field], sameFKaggle[1][field])
        stat, p = chisquare(obs, f_exp = obsKF)
        print("field = " + str(field+1) + " p-value = " + str(p))

    print()

    print("Chi squared tests comparing proportion of each field with the proportion from the Census dataset")
    for field in range(18):
        obs = np.array(sameFCensus[0][field], sameFCensus[1][field])
        stat, p = chisquare(obs, f_exp = obsCF)
        print("field = " + str(field+1) + " p-value = " + str(p))



##############################################################################################
    #graphs
##############################################################################################
#graphs for fields

    sameFKaggle = sameFieldKaggle(dfK, dfKField)
    sameFCensus = sameFieldCensus(dfC)
    #field
    labels = [x for x in range(1,19)]
    same = sameFKaggle[0,:]
    diff = sameFKaggle[1,:]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(211)
    # fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, same, width, label='Same Field')
    rects2 = ax.bar(x + width/2, diff, width, label='Different Field')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of People')
    ax.set_xlabel('Fields')
    ax.set_title('Compare interest Kaggle Dataset from same Field')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(ax, rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(ax, rects1)
    autolabel(ax, rects2)

    fig.tight_layout()

#######################################################################################

    labels = [x for x in range(1,19)]
    sameC = sameFCensus[0,:]
    diffC = sameFCensus[1,:]

    ax2 = fig.add_subplot(212)
    rects1_2 = ax2.bar(x - width/2, sameC, width, label='Same Field')
    rects2_2 = ax2.bar(x + width/2, diffC, width, label='Different Field')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax2.set_ylabel('Number of People')
    ax2.set_xlabel('Fields')
    ax2.set_title('Compare interest Census Dataset from same Field')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend()

    autolabel(ax2, rects1_2)
    autolabel(ax2, rects2_2)

    fig.tight_layout()
    plt.show()

#######################################################################################
#occupation
#######################################################################################

    sameOccKaggle = sameOCCKaggle(dfK, dfKCareer)
    sameOccCensus = sameOCCCensus(dfC)

    labels = [x for x in range(1,18)]
    same = sameOccKaggle[0,:]
    diff = sameOccKaggle[1,:]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(211)
    # fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, same, width, label='Same OCC')
    rects2 = ax.bar(x + width/2, diff, width, label='Different OCC')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of People')
    ax.set_xlabel('Occupations')
    ax.set_title('Compare interest Kaggle Dataset from same occupation')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    autolabel(ax, rects1)
    autolabel(ax, rects2)

    fig.tight_layout()

#######################################################################################

    labels = [x for x in range(1,18)]
    sameC = sameOccCensus[0,:]
    diffC = sameOccCensus[1,:]

    ax2 = fig.add_subplot(212)
    rects1_2 = ax2.bar(x - width/2, sameC, width, label='Same OCC')
    rects2_2 = ax2.bar(x + width/2, diffC, width, label='Different OCC')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax2.set_ylabel('Number of People')
    ax2.set_xlabel('Occupations')
    ax2.set_title('Compare interest Census Dataset from same occupation')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend()

    autolabel(ax2, rects1_2)
    autolabel(ax2, rects2_2)

    fig.tight_layout()
    plt.show()
