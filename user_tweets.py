#!/usr/bin/env python
"""
user_tweets.py

command line tool to print out a users first 25 tweets of
their timeline
"""
from textwrap import wrap
import sys
from twender import tweepy_api

USAGE = '\nUsage: ./print_tweets <screen_name>\n'


def print_user_tweets(user):
    tweets = tweepy_api.user_timeline(screen_name=user, count=25)
    print('Number of Tweets {count}\n'.format(count=len(tweets)))
    for tweet in tweets:
        separator = '*' * 20 + '\n'
        user_name = tweet.user.name
        tweet_body = '\n'.join(wrap(tweet.text, 80, break_long_words=False))
        created_at = tweet.created_at
        output = '{user} says:\n{tweet}\nat {time}\n'.format(user=user_name,
                tweet=tweet_body,
                time=created_at)
        output = separator + output + separator
        print(output)


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        print_user_tweets(args[1])
    else:
        print(USAGE)
