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
    # only counting occurences where a person was able to go on a date
    # with someone of the same occupation.
    sameOccupationKaggle = census_analysis.sameOCCKaggle(dfK, dfKCareer)
    objects = ('attracted on average to someone with the same intended career',
        'not attracted on average to someone with same intended career')
    plt.figure(1)
    y_pos = np.arange(len(objects))
    total_sameOcc_kaggle = np.sum(sameOccupationKaggle, axis=1)[0]
    total_diffOcc_kaggle = np.sum(sameOccupationKaggle, axis=1)[1]
    values = [total_sameOcc_kaggle, total_diffOcc_kaggle]
    percent_SameOccKaggle = total_sameOcc_kaggle/(total_sameOcc_kaggle+total_diffOcc_kaggle)
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Total number of people')
    for index, value in enumerate(values):
        plt.text(index, value, str(value))
    plt.title('Attraction based on intended career in Kaggle dataset')

    # hypothesis is that "People tend to be attracted to others in the same occupation"
    # ie. ">50% of people attracted to someone in same occupation"
    # H0 = P >= 50%
    # Ha = P < 50%
    print("Z-test for kaggle data occupation")
    print("Percentage of people attracted on avg to ppl in same occ = %f" % (percent_SameOccKaggle))
    stat, pval = proportion.proportions_ztest(total_sameOcc_kaggle, total_sameOcc_kaggle+total_diffOcc_kaggle, 0.5, 'smaller')
    print("test statistic = %f, pval = %f" % (stat, pval))
    # pval = 0.000 which is less than 0.05, so we reject null hypothesis

    ###########################################################################
    # Analyzing CI for majors for Kaggle dataset
    ###########################################################################
    sameFKaggle = census_analysis.sameFieldKaggle(dfK, dfKField)
    plt.figure(2)
    objects = ('attracted on average to someone in the same major',
        'not attracted on average to someone in same major')
    y_pos = np.arange(len(objects))
    total_sameF_kaggle = np.sum(sameFKaggle, axis=1)[0]
    total_diffF_kaggle = np.sum(sameFKaggle, axis=1)[1]
    values = [total_sameF_kaggle, total_diffF_kaggle]
    percent_SameFKaggle = total_sameF_kaggle/(total_sameF_kaggle+total_diffF_kaggle)
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, wrap=True)
    plt.ylabel('Total number of people')
    for index, value in enumerate(values):
        plt.text(index, value, str(value))
    plt.title('Attraction based on college major in Kaggle dataset')

    # hypothesis is that "People tend to be attracted to others in the same major"
    # ie. ">50% of people attracted to someone in same major"
    # H0 = P >= 50%
    # Ha = P < 50%
    print("Z-test for kaggle data major")
    print("Percentage of people attracted on avg to ppl in same major = %f" % (percent_SameFKaggle))
    stat, pval = proportion.proportions_ztest(total_sameF_kaggle, total_sameF_kaggle+total_diffF_kaggle, 0.5, 'smaller')
    print("test statistic = %f, pval = %f" % (stat, pval))
    # pval = 0.000 which is less than 0.05, so we reject null hypothesis

    ###########################################################################
    # Analyzing CI for occupations for census dataset
    ###########################################################################
    sameOccupationCensus = census_analysis.sameOCCCensus(dfC)
    objects = ('married to someone with same occupation',
        'married to someone with different occupation')
    plt.figure(3)
    y_pos = np.arange(len(objects))
    total_sameOcc_census = np.sum(sameOccupationCensus, axis=1)[0]
    percent_marriedSameOcc = total_sameOcc_census/len(dfC)
    total_diffOcc_census = np.sum(sameOccupationCensus, axis=1)[1]
    # percent_marriedDiffOcc = total_diffOcc/len(dfC)
    values = [total_sameOcc_census, total_diffOcc_census]
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Total number of people')
    for index, value in enumerate(values):
        plt.text(index, value, str(value))
    plt.title('Marriage based on occupation in US census dataset')
    # plt.show()

    # hypothesis is that "People tend to marry others in the same occupation"
    # ie. ">50% of people marry someone in same occupation"
    # H0 = P >= 50%
    # Ha = P < 50%
    print("Z-test for census data occupation")
    print("Percentage of married couples with same occ = %f" % (percent_marriedSameOcc))
    stat, pval = proportion.proportions_ztest(total_sameOcc_census, len(dfC), 0.5, 'smaller')
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
    total_sameField_census = np.sum(sameFCensus, axis=1)[0]
    percent_marriedSameF = total_sameField_census/len(dfC)
    total_diffField_census = np.sum(sameFCensus, axis=1)[1]
    # percent_marriedDiffF = total_diffField/len(dfC)
    values = [total_sameField_census, total_diffField_census]
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    for index, value in enumerate(values):
        plt.text(index, value, str(value))
    plt.ylabel('Total number of people')
    plt.title('Marriage based on major in US census dataset')
    # plt.show()
    # hypothesis is that "People tend to marry others in the same major"
    # ie. ">50% of people marry someone in same major"
    # H0 = P >= 50%
    # Ha = P < 50%
    print("Z-test for census data major")
    stat, pval = proportion.proportions_ztest(total_sameField_census, len(dfC), 0.5, 'smaller')
    print("Percentage of married couples with same major = %f" % (percent_marriedSameF))
    print("test statistic = %f, pval = %f" % (stat, pval))
    # pval = 0.000 which is less than 0.05, so we reject null hypothesis

    ###########################################################################
    # Analyzing occ vs. major for census data set
    ###########################################################################
    # hypothesis is that "Having the same occupation is a better predictor of marriage
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
    for index, value in enumerate(values):
        plt.text(index, value, str(value))
    plt.ylabel('Percentage out of all married individuals')
    plt.title('Marriage based on major and occupation in US census dataset')

    print("Z-test for census data major vs. occupation")
    count = np.array([total_sameOcc_census, total_sameField_census])
    nobs = np.array([ len(dfC),  len(dfC)])
    stat, pval = proportion.proportions_ztest(count,nobs, 0, 'larger')
    print("test statistic = %f, pval = %f" % (stat, pval))
    # pval = 0.000 which is less than 0.05, so we reject null hypothesis
    # plt.show()

    ###########################################################################
    # Analyzing occ vs. major for kaggle data set
    ###########################################################################
    # hypothesis is that "Having the same major is a better predictor of attraction
    # than having the same career interests"
    # ie. "the proportion of people attracted to others with the same major  (p_m) is greater
    # than the proportion of people attracted to others with the same career goals (p_o)"
    # H0 = proportions same
    # Ha = proportions diff (p_m > p_o)))
    plt.figure(6)
    objects = ('attracted to someone with same career interests',
        'attracted to someone with same major')
    y_pos = np.arange(len(objects))
    values = [percent_SameOccKaggle, percent_SameFKaggle]
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    for index, value in enumerate(values):
        plt.text(index, value, str(value))
    plt.ylabel('Percentage out of all people who went on at least one date with someone in the same major or career', wrap=True)
    plt.title('Attracted based on major and occupation in Kaggle dataset')

    print("Z-test for kaggle data major vs. occupation")
    count = np.array([total_sameF_kaggle, total_sameOcc_kaggle])
    nobs = np.array([ total_sameF_kaggle+ total_diffF_kaggle,  total_sameOcc_kaggle+ total_diffOcc_kaggle])
    stat, pval = proportion.proportions_ztest(count,nobs, 0, 'larger')
    print("test statistic = %f, pval = %f" % (stat, pval))
    # pval = 0.000 which is less than 0.05, so we reject null hypothesis

    ###########################################################################
    # Analyzing kaggle vs. census for college major
    ###########################################################################
    # hypothesis is that:
    # "the proportion of people who on average indicated attraction to others
    #  with the same major  (p_a) is greater
    # than the proportion of people who marry someone within the same major (p_m)"
    # H0 = proportions same
    # Ha = proportions diff (p_a > p_m)))
    plt.figure(7)
    objects = ('attracted to someone with same college major',
        'married to someone with same college major')
    y_pos = np.arange(len(objects))
    values = [percent_SameFKaggle, percent_marriedSameF]
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    for index, value in enumerate(values):
        plt.text(index, value, str(value))
    plt.ylabel('Proportions relative to respective datasets')
    plt.title('Attraction vs Marriage based on college major')

    print("Z-test for kaggle vs. census data on college major")
    count = np.array([total_sameF_kaggle, total_sameField_census])
    nobs = np.array([ total_sameF_kaggle+ total_diffF_kaggle,  len(dfC)])
    stat, pval = proportion.proportions_ztest(count,nobs, 0, 'larger')
    print("test statistic = %f, pval = %f" % (stat, pval))

    ###########################################################################
    # Analyzing kaggle vs. census for occupation
    ###########################################################################
    # hypothesis is that:
    # "the proportion of people who on average indicated attraction to others
    #  with the same career aspirations (p_a) is less than
    # than the proportion of people who marry someone within the same occupation (p_m)"
    # H0 = proportions same
    # Ha = proportions diff (p_a < p_m)))
    plt.figure(8)
    objects = ('attracted to someone with same intended career',
        'married to someone with same career')
    y_pos = np.arange(len(objects))
    values = [percent_SameOccKaggle, percent_marriedSameOcc]
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    for index, value in enumerate(values):
        plt.text(index, value, str(value))
    plt.ylabel('Proportions relative to respective datasets')
    plt.title('Attraction vs Marriage based on career')

    print("Z-test for kaggle vs. census data on occupation")
    count = np.array([total_sameOcc_kaggle, total_sameOcc_census])
    nobs = np.array([ total_sameOcc_kaggle+ total_diffOcc_kaggle,  len(dfC)])
    stat, pval = proportion.proportions_ztest(count,nobs, 0, 'larger')
    print("test statistic = %f, pval = %f" % (stat, pval))


    # plt.show()
