import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare
import census_Chi_squared as census_analysis
from statsmodels.stats import proportion

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


    ###########################################################################
    # Analyzing CI
    ###########################################################################
    dfKCareer = load_file("kaggle_clean.db", "SELECT * FROM career")
    dfKField = load_file("kaggle_clean.db", "SELECT * FROM field_of_study")

    ###########################################################################
    # Analyzing CI for occupations for Kaggle dataset
    ###########################################################################
    sameOccupationKaggle = census_analysis.sameOCCKaggle(dfK, dfKCareer)
    objects = ('Num people who said yes more times to go on another date with \
        someone of the same occupation',
        'Num people who said no more times to go on another date with \
            someone of the same occupation')
    plt.figure(1)
    y_pos = np.arange(len(objects))
    total_sameOcc = np.sum(sameOccupationKaggle, axis=1)[0]
    total_diffOcc = np.sum(sameOccupationKaggle, axis=1)[1]
    values = [total_sameOcc, total_diffOcc]
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Total number of people')
    plt.title('Attraction based on occupation in Kaggle dataset')
    # plt.show()

    ###########################################################################
    # Analyzing CI for majors for Kaggle dataset
    ###########################################################################
    sameFKaggle = census_analysis.sameFieldKaggle(dfK, dfKField)
    plt.figure(3)


    ###########################################################################
    # Analyzing CI for occupations for census dataset
    ###########################################################################
    sameOccupationCensus = census_analysis.sameOCCCensus(dfC)
    objects = ('married to someone with same occupation',
        'married to someone with different occupation')
    plt.figure(2)
    y_pos = np.arange(len(objects))
    total_sameOcc = np.sum(sameOccupationCensus, axis=1)[0]
    percent_marriedSameOcc = total_sameOcc/len(dfC)
    total_diffOcc = np.sum(sameOccupationCensus, axis=1)[1]
    percent_marriedDiffOcc = total_diffOcc/len(dfC)
    values = [total_sameOcc, total_diffOcc]
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Total number of people')
    plt.title('Marriage based on occupation in US census dataset')
    # plt.show()

    # hypothesis is that "People tend to marry others in the same occupation"
    # ie. ">50% of people marry someone in same occupation"
    # H0 = P >= 50%
    # Ha = P < 50%
    print("Z-test for census data occupation")
    print("Percentage of married couples with same occ = %f" % (percent_marriedSameOcc))
    stat, pval = proportion.proportions_ztest(total_sameOcc, len(dfC), 0.5, 'smaller')
    print("test statistic = %f, pval = %f" % (stat, pval))
    # pval = 0.000 which is less than 0.05, so we reject null hypothesis


    ###########################################################################
    # Analyzing CI for majors for census dataset
    ###########################################################################
    sameFCensus = census_analysis.sameFieldCensus(dfC)
    plt.figure(4)
    objects = ('married to someone with same major',
        'married to someone with different major')
    y_pos = np.arange(len(objects))
    total_sameField = np.sum(sameFCensus, axis=1)[0]
    percent_marriedSameF = total_sameField/len(dfC)
    total_diffField = np.sum(sameFCensus, axis=1)[1]
    percent_marriedDiffF = total_diffField/len(dfC)
    values = [total_sameField, total_diffField]
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Total number of people')
    plt.title('Marriage based on major in US census dataset')
    # plt.show()
    # hypothesis is that "People tend to marry others in the same major"
    # ie. ">50% of people marry someone in same major"
    # H0 = P >= 50%
    # Ha = P < 50%
    print("Z-test for census data major")
    stat, pval = proportion.proportions_ztest(total_sameField, len(dfC), 0.5, 'smaller')
    print("Percentage of married couples with same major = %f" % (percent_marriedSameF))
    print("test statistic = %f, pval = %f" % (stat, pval))
    # pval = 0.000 which is less than 0.05, so we reject null hypothesis

    ###########################################################################
    # Analyzing occ vs. major for census data set
    ###########################################################################
    # hypothesis is that "Having the occupation is a better predictor of marriage
    # than having the same college major"
    # ie. "the proportion of married people with the same occupation  (p_o) is greater
    # than the proportion of married people with the same college major (p_m)"
    # H0 = proportions same
    # Ha = proportions diff (p_o > p_m)))
    plt.figure(5)
    objects = ('married to someone with same occupation',
        'married to someone with same major')
    y_pos = np.arange(len(objects))
    values = [percent_marriedSameOcc, percent_marriedSameF]
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Percentage out of all married couples')
    plt.title('Marriage based on major and occupation in US census dataset')

    print("Z-test for census data major vs. occupation")
    count = np.array([total_sameOcc, total_sameField])
    nobs = np.array([ len(dfC),  len(dfC)])
    stat, pval = proportion.proportions_ztest(count,nobs, 0, 'larger')
    print("test statistic = %f, pval = %f" % (stat, pval))
    # pval = 0.000 which is less than 0.05, so we reject null hypothesis
    plt.show()
