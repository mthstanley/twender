#!/usr/bin/env python
"""
testyouaclassifier.py

Command line script to test the accuracy of the classifier built in 
the learnyouaclassifier.py module. A classifier will be trained on 
tweets found in the tweets collection in the twender_db, then it will
be tested on the testing collection in the twender_db
"""
from twender import twender_db
import learnyouaclassifier as learn
import sys
import matplotlib.pyplot as plt

def test_classifier(num_tweets):

    num_male = num_tweets // 2
    num_female = num_tweets - num_male

    # initialize classifer
    classifier = learn.TwenderClassifier()

    # train classfier on tweets collection
    female_training = list(twender_db.tweets.find({'gender': 'F'}).limit(num_female))
    male_training = list(twender_db.tweets.find({'gender': 'M'}).limit(num_male))
    training_tweets = female_training + male_training
    classifier.train(training_tweets)

    # extract testing tweets and labels into separate lists
    # where the indices in each list correspond
    testing_tweets = [tweet for tweet in twender_db.testing.find()]
    labels = [tweet['gender'] for tweet in testing_tweets]

    # calculate predictions
    predictions = classifier.classify(testing_tweets)
    tweets, guesses = zip(*predictions)

    num_correct = 0
    for index, guess in enumerate(guesses):
        if guess == 0:
            if labels[index] == 'M':
                num_correct += 1
        else:
            if labels[index] == 'F':
                num_correct += 1
    return (num_correct/len(testing_tweets))

def graph_increase():
    percents = []
    x_values = []
    num_train = 1000
    total_tweets = twender_db.tweets.find().count()

    while num_train < total_tweets:
        x_values.append(num_train)
        percents.append(test_classifier(num_train)*100)

        num_train += 1000

    plt.plot(x_values, percents)
    plt.xlabel('Number of Tweets in Training Dataset')
    plt.ylabel('Percent Correct (%)')
    plt.title('Percent Correct Classifications vs Training Dataset Size')

    plt.show()

if __name__ == '__main__':

    total_tweets = twender_db.tweets.find().count()
    
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
        num_train = num if num < total_tweets else total_tweets
    else:
        num_train = total_tweets

    percent_correct = test_classifier(num_train)
    # output percentage correct
    print('Percentage Classified Correctly: %.2f%%' % (percent_correct*100))
