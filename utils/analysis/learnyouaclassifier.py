"""
learnyouaclassifier.py

This module contains the twender classifier class definition, the classifier
has two methods, train and classify. train is given the set of training tweets
(the full tweet object) and will train the classifier, once this is accomplished
the classify method can be used, this method takes in another set of tweets and
outputs a dictionary of tweets and associated labels
"""

import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

class TweetData:
    """
    class for holding extracted twitter data, holds the tweet text data
    the associated target or label data and the target names M or F
    """

    def __init__(self, data, target, target_names):
        self.data = data
        self.target = target
        self.target_names = target_names


class TwenderClassifier:
    """
    classifier for classifying tweets by gender (based on the text of the tweet)

    Public Methods:
        train(training_tweets)
        classify(tweets)
    """

    def __init__(self):
        
        self.count_vect = CountVectorizer()
        self.tfidf_trans = TfidfTransformer()
        self.classifier = MultinomialNB()
        #self.classifier = SGDClassifier()

    def train(self, training_tweets):
        """
        param:
            training_tweets: a list of tweets (objects) for the classifier to 
            train on 
        return:
            None
        description:
            fits the classifier to the training tweet data
        """
        
        self.extract_tweets(training_tweets)
        
        X_train_counts = self.count_vect.fit_transform(self.training_data.data)
        X_train_tfidf = self.tfidf_trans.fit_transform(X_train_counts)
        self.classifier.fit(X_train_tfidf, self.training_data.target)


    def classify(self, tweets):
        """
        param:
            tweets: a list of tweet objects to classify as male or female
        return: 
            dictionary of classified tweets and their classification label
        description:
            uses the classifier to label the input tweets as male or female
            based on the text of the tweet. Note: retweets are discarded 
        """

        no_retweets = [tweet for tweet in tweets if not is_retweet(tweet)]
        tweet_text = [tweet['text'] for tweet in no_retweets]
        
        X_new_counts = self.count_vect.transform(tweet_text)
        X_new_tfidf = self.tfidf_trans.transform(X_new_counts)
        
        predicted = self.classifier.predict(X_new_tfidf)

        return zip(no_retweets, predicted) 

    
    def extract_tweets(self, tweets):
        """
        param:
            tweets: a list of tweet objects
        return:
            None
        description:
            extracts the given tweets into a list of the text of each tweet,
            a list of labels for each tweet (where the indices align) and
            a list of target names ['M', 'F']

            these are stored in the TweetData object and set as the classifiers
            training_data field
        """

        data = []
        target = []
        target_names = ['M', 'F']
        

        for tweet in tweets:
            text = tweet['text']
            # remove websites from tweets
            #text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            #    '', text, flags=re.MULTILINE)
            # remove user names
            #text = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)',
            #    '', text, flags=re.MULTILINE)
            # remove hashtags
            #text = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z]+[A-Za-z0-9]+)',
            #    '', text, flags=re.MULTILINE)
            data.append(text)
            target.append(target_names.index(tweet['gender']))

        self.training_data = TweetData(data, target, target_names)


def is_retweet(tweet):
    """
    param:
        tweet: a tweet object
    return: 
        True if the tweet is a retweet, false if not
    description:
        determines whether a tweet is a retweet
    """
    retweeted = re.compile('\s*RT.*')
    return retweeted.match(tweet['text']) is not None or tweet['retweeted']


def genderize(tweet_genders):
    """
    param:
        tweet_genders: a list of 1's or 0's (female or male) assumed
        to be the classification of a users tweets
    return:
        an overall classification of a user, 0 for male 1 for female
    description:
        calculates the percentage of the tweet_genders label list
        is male vs female and returns label with a higher percentage
    """

    total = len(tweet_genders)
    total_female = sum(tweet_genders)
    total_male = total - total_female

    per_male = total_male / total
    per_female = total_female / total

    if per_male > per_female:
        return 0
    else:
        return 1
