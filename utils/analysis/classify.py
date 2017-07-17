#!/usr/bin/env python
"""
classify.py

command line tool to classify tweets, the user may specify a file
which is assumed to have a tweet's text on each line, the classification
for each of these tweets will be printed out, the classifier is built based
on the twender database
"""
from twender import twender_db
import learnyouaclassifier as learn
import sys

def file_to_list(filename):
    lines = []
    with open(filename, 'r') as fdata:

        for line in fdata:
            lines.append(line.strip())
    return lines



if __name__ == '__main__':

    if len(sys.argv) > 1:
        filename = sys.argv[1]

        tweets = twender_db.tweets
        trained = learn.build_classifier(tweets.find())
        
        new_docs = file_to_list(filename)

        X_new_counts = trained.count_vect.transform(new_docs)
        X_new_tfidf = trained.tfidf_trans.transform(X_new_counts)

        predicted = trained.text_clf.predict(X_new_tfidf)

        for doc, category in zip(new_docs, predicted):
            print('%r => %s' % (doc, trained.target_names[category]))


