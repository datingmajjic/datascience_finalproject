import sqlite3
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare
from scipy import stats

'''
counts the number of people in the Kaggle dataset who would go on another date
 with someone of the same occupation

    returns array where each column is an occupation and row 0 represents the
    number of people who would go on another date with the same occupation and
    row 1 represents the number of  people who would not go on another date with
    the same occupation
'''
def sameOCCKaggle(demo):
    #first row is date
    #second row is not date
    #columns are the occupations
    occupations = np.zeros((2,17))
    # for i in range(len(demo)):
    #     id = demo.loc[i, "iid"]
    #     occ =  demo.loc[i, "career_c"]
    #     if not math.isnan(id) and  not math.isnan(occ):
    #
    #         colname = str(int(occ))+"_decision"
    #         for j in range(len(career)):
    #             #finding the person by their id in the career table
    #             if career.loc[j,"iid"] == id:
    #                 #finding if they would date the person with the same career
    #                 if career.loc[j,colname] > 0.5:
    #                 # if career.loc[j,colname] > 0.5 and not math.isnan(career.loc[j,colname]):
    #                     # dateAgain += 1
    #                     occupations[0][int(occ-1)]+= 1
    #                 # else:
    #                 elif not math.isnan(career.loc[j,colname]):
    #                     # notDate += 1
    #                     occupations[1][int(occ-1)]+= 1
    for i in range(len(demo.index)):
        if demo.loc[i, "dec"] == 1:
            occ = demo.loc[i, "career_c"]
            if demo.loc[i, "same_career"] == 1 and not math.isnan(occ):
                occupations[0][int(occ-1)]+= 1
            elif not math.isnan(occ):
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
def sameFieldKaggle(demo):
    #first row is date
    #second row is not date
    #columns are the occupations
    fields = np.zeros((2,18))
    # for i in range(len(demo)):
    #     id = demo.loc[i, "iid"]
    #     f =  demo.loc[i, "field_cd"]
    #     if not math.isnan(id) and  not math.isnan(f):
    #
    #         colname = str(int(f))+"_decision"
    #         for j in range(len(field)):
    #             #finding the person by their id in the career table
    #             if field.loc[j,"iid"] == id:
    #                 #finding if they would date the person with the same career
    #                 if field.loc[j,colname] > 0.5:
    #                     # dateAgain += 1
    #                     fields[0][int(f-1)]+= 1
    #                 elif not math.isnan(field.loc[j,colname]):
    #                     # notDate += 1
    #                     fields[1][int(f-1)]+= 1


    for i in range(len(demo.index)):
        if demo.loc[i, "dec"] == 1:
            f = demo.loc[i, "field_cd"]
            if demo.loc[i, "same_field"] == 1 and not math.isnan(f):
                fields[0][int(f-1)]+= 1
            elif not math.isnan(f):
                fields[1][int(f-1)]+= 1
    return np.asarray(fields)

'''
counts the number of people in the Kaggle dataset who would go on another date
 with someone of the same occupation

returns information as list containing number of people who would go on another
 date with someone of the same occupation and the number of people who would not go on another
date with someone of the same occupation
'''
def sameOCCKaggleAll(demo):

    #first row is date
    #second row is not date
    #columns are the occupations
    # dateAgain = 0
    # notDate = 0
    #
    # occupations = np.zeros((2,17))
    # for i in range(len(demo)):
    #     id = demo.loc[i, "iid"]
    #     occ =  demo.loc[i, "career_c"]
    #     if not math.isnan(id) and  not math.isnan(occ):
    #
    #         colname = str(int(occ))+"_decision"
    #         for j in range(len(career)):
    #             #finding the person by their id in the career table
    #             if career.loc[j,"iid"] == id:
    #                 #finding if they would date the person with the same career
    #                 if career.loc[j,colname] > 0.5 :
    #                     dateAgain += 1
    #                 elif not math.isnan(career.loc[j,colname]):
    #                     notDate += 1

    ####pandas
    dateAgain = 0
    notDate = 0
    for i in range(len(demo.index)):
        if demo.loc[i, "dec"] == 1:
            dateAgain+= demo.loc[i, "same_career"]
            notDate += 1 - demo.loc[i, "same_career"]


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
def sameFieldKaggleAll(demo):
    # dateAgain = 0
    # notDate = 0
    # for i in range(len(demo)):
    #     id = demo.loc[i, "iid"]
    #     f =  demo.loc[i, "field_cd"]
    #     if not math.isnan(id) and  not math.isnan(f):
    #
    #         colname = str(int(f))+"_decision"
    #         for j in range(len(field)):
    #             #finding the person by their id in the career table
    #             if field.loc[j,"iid"] == id:
    #                 #finding if they would date the person with the same career
    #                 if field.loc[j,colname] > 0.5:
    #                     dateAgain += 1
    #                 elif not math.isnan(field.loc[j,colname]):
    #                     notDate += 1

    ##pandas
    dateAgain = 0
    notDate = 0
    for i in range(len(demo.index)):
        if demo.loc[i, "dec"] == 1:
            dateAgain+= demo.loc[i, "same_field"]
            notDate += 1 - demo.loc[i, "same_field"]


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
    # # dfK = load_file("kaggle_clean.db", "SELECT * FROM demographics")
    # dfKCareer = load_file("kaggle_clean.db", "SELECT * FROM career")
    # dfKField = load_file("kaggle_clean.db", "SELECT * FROM field_of_study")

    dfK = pd.read_csv('Kaggle_Data-Individual_Dates_Clean.csv')
    # print(dfKaggle)

##############################################################################################
#Chi-squared test comparing the number of people who marry the same occupation in both datasets
##############################################################################################

    obsKO = sameOCCKaggleAll(dfK)
    obsCO = sameOCCCensusAll(dfC)
    obsO = np.array((obsKO,obsCO))
    chi2, p, dof, expected = stats.chi2_contingency(obsO)
    print("chi squared test comparing same occuptions on both datasets")
    print("p-value = " + str(p))

##############################################################################################
#Chi-squared test comparing the number of people who marry the same field in both datasets
##############################################################################################
    obsKF = sameFieldKaggleAll(dfK)
    obsCF = sameFieldCensusAll(dfC)
    obsF = np.array((obsKF,obsCF))
    chi2, p, dof, expected = stats.chi2_contingency(obsF)
    print("chi squared test comparing same fields on both datasets")
    print("p-value = " + str(p))
    print()

    '''
    listL columns each represent one occupation and row 0 stores the number of
    people who would data/marry same occupation and row 1 stores the number of
    people who would data/marry different occupation
    '''
    sameOccupationKaggle = sameOCCKaggle(dfK)
    sameOccupationCensus = sameOCCCensus(dfC)


##############################################################################################
#chi-squared test comparing the proportion of people who are a specific occuption and marry
#the same occupation to the total number of people who marry the same occupation in each dataset
##############################################################################################

    print("Chi squared tests comparing proportion of each occupation with the proportion from the Kaggle dataset")
    for occ in range(17):
        obs = np.array((sameOccupationKaggle[0][occ], sameOccupationKaggle[1][occ]))
        proportion = obsKO[0]/(sum(obsKO))
        total = sum(obs)
        EXP = np.array([total*proportion, total - (total*proportion)])
        stat, p = chisquare(obs, f_exp = EXP)
        print("occupation = " + str(occ+1) + " p-value = " + str(p))

    print()

    print("Chi squared tests comparing proportion of each occupation with the proportion from the Census dataset")
    for occ in range(17):
        obs = np.array((sameOccupationCensus[0][occ], sameOccupationCensus[1][occ]))
        proportion = obsCO[0]/(sum(obsCO))
        total = sum(obs)
        EXP = np.array([total*proportion, total - (total*proportion)])
        stat, p = chisquare(obs, f_exp = EXP)
        print("occupation = " + str(occ+1) + " p-value = " + str(p))

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
    sameFKaggle = sameFieldKaggle(dfK)
    sameFCensus = sameFieldCensus(dfC)

    print("Chi squared tests comparing proportion of each field with the proportion from the Kaggle dataset")
    for field in range(18):
        obs = np.array((sameFKaggle[0][field], sameFKaggle[1][field]))
        proportion = obsKF[0]/(sum(obsKF))
        total = sum(obs)
        EXP = np.array([total*proportion, total - (total*proportion)])
        stat, p = chisquare(obs, f_exp = EXP)
        print("field = " + str(field+1) + " p-value = " + str(p))

    print()

    print("Chi squared tests comparing proportion of each field with the proportion from the Census dataset")
    sameFCensus = sameFieldCensus(dfC)
    obsCF = sameFieldCensusAll(dfC)
    for field in range(18):
        obs = np.array((sameFCensus[0][field], sameFCensus[1][field]))
        proportion = obsCF[0]/(sum(obsCF))
        total = sum(obs)
        EXP = np.array([total*proportion, total - (total*proportion)])
        stat, p = chisquare(obs, f_exp = EXP)
        print("field = " + str(field+1) + " p-value = " + str(p))

        # #chi2
        # obsF = np.array((obs,obsCF))
        # # print(obsF)
        # if np.array_equal(obs, [0,0]):
        #     print("field = " + str(field+1) + " no data")
        # else:
        #     chi2, p, dof, expected = stats.chi2_contingency(obsF)
        #     print("field = " + str(field+1) + " p-value = " + str(p))



##############################################################################################
    #graphs
##############################################################################################
#graphs for fields

    sameFKaggle = sameFieldKaggle(dfK)
    sameFCensus = sameFieldCensus(dfC)

    obsKF = sameFieldKaggleAll(dfK)
    obsCF = sameFieldCensusAll(dfC)
    #field
    labels = [x for x in range(1,19)]
    same = sameFKaggle[0,:]
    diff = sameFKaggle[1,:]
    # labels.append("Total")
    # same = np.append(sameFKaggle[0,:],obsKF[0])
    # diff = np.append(sameFKaggle[1,:],obsKF[1])

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
    ax.set_title('Effect of Field of Study on Initial Attraction using Kaggle Dataset')
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
    # labels.append("Total")
    # sameC = np.append(sameFCensus[0,:], obsCF[0])
    # diffC = np.append(sameFCensus[1,:], obsCF[1])

    ax2 = fig.add_subplot(212)
    rects1_2 = ax2.bar(x - width/2, sameC, width, label='Same Field')
    rects2_2 = ax2.bar(x + width/2, diffC, width, label='Different Field')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax2.set_ylabel('Number of People')
    ax2.set_xlabel('Fields')
    ax2.set_title('Effect of Field of Study on Marriage using Census Dataset')
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

    sameOccKaggle = sameOCCKaggle(dfK)
    sameOccCensus = sameOCCCensus(dfC)
    obsCO = sameOCCCensusAll(dfC)
    obsKO = sameOCCKaggleAll(dfK)

    labels = [x for x in range(1,18)]
    same = sameOccKaggle[0,:]
    diff = sameOccKaggle[1,:]
    # labels.append("Total")
    # same = np.append(sameOccKaggle[0,:],obsKO[0])
    # diff = np.append(sameOccKaggle[1,:], obsKO[1])

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
    ax.set_title('Effect of Intended Career on Initial Attraction using Kaggle Dataset')
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
    # labels.append("Total")
    # sameC = np.append(sameOccCensus[0,:],obsCO[0])
    # diffC = np.append(sameOccCensus[1,:], obsCO[1])

    ax2 = fig.add_subplot(212)
    rects1_2 = ax2.bar(x - width/2, sameC, width, label='Same OCC')
    rects2_2 = ax2.bar(x + width/2, diffC, width, label='Different OCC')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax2.set_ylabel('Number of People')
    ax2.set_xlabel('Occupations')
    ax2.set_title('Effect of Career on Marriage using Census Dataset')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend()

    autolabel(ax2, rects1_2)
    autolabel(ax2, rects2_2)

    fig.tight_layout()

    plt.show()
#######################################################################################
#compare census to kaggle
#######################################################################################
    fig = plt.figure()

    #occupation
    labels = ["Kaggle", "Census"]
    same = np.array((obsKO[0], obsCO[0]))
    diff = np.array((obsKO[1], obsCO[1]))

    x = np.arange(len(labels))  # the label locations
    width = 0.35

    ax3 = fig.add_subplot(211)
    rects1 = ax3.bar(x - width/2, same, width, label='Same OCC')
    rects2 = ax3.bar(x + width/2, diff, width, label='Different OCC')

    ax3.set_ylabel('Number of People')
    ax3.set_xlabel('Dataset')
    ax3.set_title('Compare effect Occupation on Initial Attraction and Marriage')
    ax3.set_xticks(x)
    ax3.set_xticklabels(labels)
    ax3.legend()

    autolabel(ax3, rects1)
    autolabel(ax3, rects2)

    fig.tight_layout()

#######################################################################################


    #occupation
    labels = ["Kaggle", "Census"]
    # maxVal = max(obsKF[0], obsCF[0], obsKF[1], obsCF[1])
    sameF = np.array((obsKF[0], obsCF[0]))
    # sameF = np.true_divide(sameF, maxVal)
    diffF = np.array((obsKF[1], obsCF[1]))
    # diffF = np.true_divide(diffF, maxVal)

    x = np.arange(len(labels))  # the label locations
    width = 0.35

    ax4 = fig.add_subplot(212)
    rects1_1 = ax4.bar(x - width/2, sameF, width, label='Same field')
    rects2_1 = ax4.bar(x + width/2, diffF, width, label='Different field')

    ax4.set_ylabel('Number of People')
    ax4.set_xlabel('Dataset')
    ax4.set_title('Compare effect of Field on Initial Attraction and Marriage')
    ax4.set_xticks(x)
    ax4.set_xticklabels(labels)
    ax4.legend()

    autolabel(ax4, rects1_1)
    autolabel(ax4, rects2_1)

    fig.tight_layout()




    plt.show()
