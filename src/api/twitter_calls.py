#!/usr/bin/python
# -*- coding: utf-8 -*-

import oauth2 as oauth
import sentiment
from config import data, geocodes
import json
import re
import pdb

def _pre_process_tweets(tweet):
    # Convert to lower
    tweet = tweet.lower()
    # Convert www.* or https?://* to ' '
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', tweet)
    # Convert @user to user (remove @)
    tweet = re.sub(r'@([^\s]+)', r'\1', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+',' ', tweet)
    # Replace #hastags with hashtags (remove #)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # Trim
    tweet = tweet.strip('\'"')

    return tweet


# Return tweets to analyze
def get_tweets(url, http_method="GET", post_body="", http_headers=None):
    consumer = oauth.Consumer(key=data['CONSUMER_KEY'], secret=data['CONSUMER_SECRET'])
    token = oauth.Token(key=data['ACCESS_TOKEN'], secret=data['ACCESS_SECRET'])

    try:
        # Checking if consumer/token are valid
        client = oauth.Client(consumer, token)
    except ValueError as e:
        raise Exception(e.message)

    # Response from API endpoint
    response = client.request(url, method=http_method, body=post_body, headers=http_headers)
    # Convert to JSON
    json_response = json.loads(response[1])

    # Response status
    response_status = response[0].status
    if response_status == 200:
        json_response = json_response
    else:
        msg = json_response['errors'][0]['message']
        server_message = '' if msg is None else msg
        raise Exception(str(response_status) + ' status returned, ' + server_message)

    # print json_response
    # Go through tweets
    for user in json_response:
        user_name = '@' + user['user']['screen_name']
        tweet = user['text']
        print user_name + ' tweeted: ' + tweet


def search_tweets(url, http_method="GET", post_body="", http_headers=None):
    consumer = oauth.Consumer(key=data['CONSUMER_KEY'], secret=data['CONSUMER_SECRET'])
    token = oauth.Token(key=data['ACCESS_TOKEN'], secret=data['ACCESS_SECRET'])

    try:
        # Checking if consumer/token are valid
        client = oauth.Client(consumer, token)
    except ValueError as e:
        raise Exception(e.message)

    # Response from API endpoint
    response = client.request(url, method=http_method, body=post_body, headers=http_headers)
    # Convert to JSON
    json_response = json.loads(response[1])

    # Response status
    response_status = response[0].status
    if response_status == 200:
        json_response = json_response
    else:
        msg = json_response['errors'][0]['message']
        server_message = '' if msg is None else msg
        raise Exception(str(response_status) + ' status returned, ' + server_message)

    # Go through tweets
    for user in json_response['statuses']:
        user_name = '@' + user['user']['screen_name']
        tweet = user['text']
        combined = user_name + ' tweeted: ' + tweet

        print _pre_process_tweets(combined)

def _reverse_geocode(locations, query, http_method="GET", post_body="", http_headers=None):
    consumer = oauth.Consumer(key=data['CONSUMER_KEY'], secret=data['CONSUMER_SECRET'])
    token = oauth.Token(key=data['ACCESS_TOKEN'], secret=data['ACCESS_SECRET'])

    try:
        # Checking if consumer/token are valid
        client = oauth.Client(consumer, token)
    except ValueError as e:
        raise Exception(e.message)

    tweets = []

    for geo in locations:

        lat = geo[0]
        lng = geo[1]
        url = 'https://api.twitter.com/1.1/search/tweets.json?q=%s&geocode=%s%%2C%s%%2C15mi&lang=en&count=10' % (query, lat, lng)

        response = client.request(url, method=http_method, body=post_body, headers=http_headers)
        # Convert to JSON
        json_response = json.loads(response[1])

        for user in json_response['statuses']:
            tweet = user['text']
            tweets.append(tweet)

    print len(tweets)
    return tweets


def geo_tweets(coast, query, http_method="GET", post_body="", http_headers=None):
    locations = []
    # Check what coast we are looking for
    if coast == 'east' or coast == 'west':
        cities = geocodes[coast]
        for city in cities:
            lat = cities[city][0]
            lng = cities[city][1]
            # print city + ' has geocode of: ' + str(lat) + ',' + str(lng)

            locations.append([lat, lng])

        _reverse_geocode(locations, query) # change 10 with user tweets
    elif coast == 'both':
        print 'TO-DO: Return all cities'
    else:
        raise Exception(coast + ' is not a valid coast. Options are east, west, both')
