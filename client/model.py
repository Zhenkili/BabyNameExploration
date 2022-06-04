import os.path
import pickle

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from app import training_df


def trainModel():
    names = training_df.fillna(0)

    namechart = names.groupby(['Name', 'Gender'], as_index=False)['Count'].sum()

    namechartdiff = namechart.reset_index().pivot('Name', 'Gender', 'Count')
    namechartdiff = namechartdiff.fillna(0)
    namechartdiff["Mpercent"] = ((namechartdiff["M"] - namechartdiff["F"]) / (namechartdiff["M"] + namechartdiff["F"]))
    namechartdiff['gender'] = np.where(namechartdiff['Mpercent'] > 0.001, 'male', 'female')

    char_vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 2))
    X = char_vectorizer.fit_transform(namechartdiff.index)
    X = X.tocsc()
    y = (namechartdiff.gender == 'male').values.astype(np.int)

    itrain, itest = train_test_split(range(namechartdiff.shape[0]), train_size=0.9)
    mask = np.ones(namechartdiff.shape[0], dtype='int')
    mask[itrain] = 1
    mask[itest] = 0
    mask = (mask == 1)

    Xtrainthis = X[mask]
    Ytrainthis = y[mask]
    clf = MultinomialNB(alpha=1)
    clf.fit(Xtrainthis, Ytrainthis)
    filename = 'finalized_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    pickle.dump(char_vectorizer, open("vectorizer.pickle", "wb"))


def getGender(name):
    file_path = './finalized_model.sav'
    vectorizer_path = './vectorizer.pickle'
    if os.path.exists(file_path):
        loaded_model = pickle.load(open(file_path, 'rb'))
        char_vectorizer = pickle.load(open(vectorizer_path, 'rb'))
    else:
        trainModel()
        loaded_model = pickle.load(open(file_path, 'rb'))
        char_vectorizer = pickle.load(open(vectorizer_path, 'rb'))

    new = char_vectorizer.transform([str(name)])
    y_pred = loaded_model.predict(new)
    if y_pred == 1:
        return 1
    else:
        return 0
