from __future__ import division

import os
import sys

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from smote import SMOTE
from pdb import set_trace


root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

from old.Prediction import rforest

def getTunings(fname):
    raw = pd.read_csv(root + '/old/tunings.csv').transpose().values.tolist()
    formatd = pd.DataFrame(raw[1:], columns=raw[0])
    try:
        return formatd[fname].values.tolist()
    except KeyError:
        return None


def df2thing(dframe):
    dframe.to_csv('temp.csv', index=False)
    new_thing = createTbl(['temp.csv'], isBin=True)
    os.remove('temp.csv')
    return new_thing


def rf_model(source, target):
    clf = RandomForestClassifier(n_estimators=90, random_state=1)

    # Binarize source
    source.loc[source[source.columns[-1]] == True, source.columns[-1]] = 1
    source.loc[source[source.columns[-1]] == False, source.columns[-1]] = 0
    target.loc[target[target.columns[-1]] == True, target.columns[-1]] = 1
    target.loc[target[target.columns[-1]] == False, target.columns[-1]] = 0
    # source = SMOTE(source, k=1)
    # set_trace()
    features = source.columns[:-1]
    klass = source[source.columns[-1]]
    clf.fit(source[features], klass)
    preds = clf.predict(target[target.columns[:-1]])
    distr = clf.predict_proba(target[target.columns[:-1]])
    return preds, distr[:,1]


def rf_model_old(source, target):

    def df2thing(dframe):
        dframe.to_csv('temp.csv', index=False)
        new_thing = createTbl(['temp.csv'], isBin=True)
        os.remove('temp.csv')
        return new_thing

    train = df2thing(source)
    test = df2thing(target)

    return rforest(train, test)



def rf_model0(source, target, name):
    train = df2thing(source)
    test = df2thing(target)
    return rforest(train, test, tunings=getTunings(name))



def logistic_model(source, target):
    # Binarize source
    clf = LogisticRegression()
    source.loc[source[source.columns[-1]] > 0, source.columns[-1]] = 1
    source.loc[source[source.columns[-1]] < 1, source.columns[-1]] = 0
    # set_trace()
    source = SMOTE(source, k=1)
    # set_trace()set_trace
    features = source.columns[:-1]
    klass = [1 if k>0 else 0 for k in source[source.columns[-1]]]
    clf.fit(source[features], klass)
    preds = clf.predict(target[target.columns[:-1]])
    distr = clf.predict_proba(target[target.columns[:-1]])
    return preds, distr[:,1]


def _test_model():
    pass


if __name__ == '__main__':
    _test_model()
