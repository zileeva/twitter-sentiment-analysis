#!/usr/bin/python
# -*- coding: utf-8 -*-

import oauth2 as oauth
from config import data, geocodes
import json

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
        print user_name + ' tweeted: ' + tweet


def geo_tweets(coast, http_method="GET", post_body="", http_headers=None):
    # Check what coast we are looking for
    if coast == 'east' or coast == 'west':
        cities = geocodes[coast]
        for city in cities:
            lat = cities[city][0]
            lng = cities[city][1]
            print city + ' has geocode of: ' + str(lat) + ',' + str(lng)
    elif coast == 'both':
        print 'TO-DO: Return all cities'
    else:
        raise Exception(coast + ' is not a valid coast. Options are east, west, both')
