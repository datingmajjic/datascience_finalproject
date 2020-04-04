import pandas as pd
import sqlite3
from sklearn.preprocessing import OneHotEncoder
from pandas.api.types import CategoricalDtype
import statsmodels.api as sm

def generate_y_majors(df):
    #create col of 1/0 based on if major of person is same as major of spouse or not
    def same_major(row):
        if row["kagEDUC"] == row["kagEDUC_SP"]:
            return 1
        else:
            return 0
    df["SAME_MAJOR"] = df.apply(same_major, axis=1)
    y = df[["SAME_MAJOR"]]
    return y.to_numpy()

def generate_y_occupations(df):
    #create col of 1/0 based on if major of person has same occupation as spouse or not
    def same_occ(row):
        if row["kagOCC"] == row["kagOCC_SP"]:
            return 1
        else:
            return 0
    df["SAME_OCC"] = df.apply(same_occ, axis=1)
    y = df[["SAME_OCC"]]
    return y.to_numpy()

def generate_x(df):
    """
    input : dataframe
    output : list of input vars X
    """
    #get desired columns
    #create dummy columns for RACE
    dummy_race = pd.get_dummies(df['RACE'],prefix='RACE', drop_first=True)
    # print(dummy_race)
    df = pd.concat([df,dummy_race],axis=1)
    df.drop(['RACE'],axis=1, inplace=True)

    # X = df[["RACE","SEX", "kagEDUC","kagOCC"]]

    #create Xs for college major analysis
    X_major = df[[ "RACE_2","RACE_4","RACE_5","RACE_6","SEX", "kagEDUC"]]
    #create dummy columns for kagEDUC (college major), and drop original kagEDUC col
    # categories= CategoricalDtype(categories=[i for i in range(1,19)])
    # X = X.copy()
    # X[['kagEDUC']] = X[['kagEDUC']].astype(categories)
    dummy_major = pd.get_dummies(X_major['kagEDUC'],prefix='kagEDUC', drop_first=True)
    # dummy_major = dummy_major.astype('float64')
    X_major = pd.concat([X_major,dummy_major],axis=1)
    X_major.drop(['kagEDUC'],axis=1, inplace=True)
    # print(dummy_major)
    # print(X.shape)

    #create Xs for occupation  analysis
    X_occupation = df[["RACE_2","RACE_4","RACE_5","RACE_6","SEX","kagOCC"]]
    #create dummy columns for kagOCC (occupation ), and drop original kagOCC col
    # categories= CategoricalDtype(categories=[i for i in range(18)])
    # X = X.copy()
    # X[['kagOCC']] = X[['kagOCC']].astype(categories)
    dummy_occ = pd.get_dummies(X_occupation['kagOCC'],prefix='kagOCC', drop_first=True)
    # dummy_occ = dummy_occ.astype('float64')
    X_occupation = pd.concat([X_occupation,dummy_occ],axis=1)
    X_occupation.drop(['kagOCC'],axis=1, inplace=True)
    # print(dummy_occ)
    # print(X.shape)

    return X_major.to_numpy() , X_occupation.to_numpy()

if __name__=='__main__':
    def load_file(file_path):
        con = sqlite3.connect(file_path)
        data = pd.read_sql_query("SELECT * FROM people", con)
        return data

    df = load_file("census_stuff.db")
    y_majors = generate_y_majors(df)
    y_occupations =generate_y_occupations(df)
    X_major, X_occupation = generate_x(df)

    #Create logistic regression for classifying marriage based on college major
    # print(X.shape)
    X_major = sm.add_constant(X_major)
    model_majors = sm.Logit(y_majors, X_major)
    model_majors_fit = model_majors.fit()
    print(model_majors_fit.summary())

    #Create logistic regression for classifying marriage based on occupation
    X_occupation = sm.add_constant(X_occupation)
    model_occupations = sm.Logit(y_occupations, X_occupation)
    model_occupations_fit = model_occupations.fit()
    print(model_occupations_fit.summary())
