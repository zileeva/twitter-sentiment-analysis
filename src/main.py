#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.twitter_calls import get_tweets, search_tweets, geo_tweets
import os, sys
import argparse

def _format_url(query='none', count=0):
    if query != 'none':
        # Factoring according to Twitter api conditions
        # %22 is quotes, %20 is space
        query = '%22' + query + '%22'
        url = 'https://api.twitter.com/1.1/search/tweets.json?q=%s&count=%s' % (query, count)
    else:
        url = 'https://api.twitter.com/1.1/statuses/home_timeline.json?count=%s' % (count)

    return url


def _run_args(args):
    if args.t_line:
        count = args.t_line[0]
        url = _format_url(count)
        # Make a call to get tweets
        tweets = get_tweets(url)
    elif args.query:
        query = args.query[0].replace('#', '%23').replace(' ', '%20')
        url = _format_url(query, args.query[1])
        # Search through tweets with given query
        tweets = search_tweets(url)
    elif args.geo:
        count = args.geo[1]
        geo_tweets(args.geo[0].lower())

if __name__ == '__main__':
    # Top Parser
    parser = argparse.ArgumentParser(description='use tweety to search through tweets.')
    parser.add_argument('-t', '--t_line', nargs=1, help='View X most recent posts on home timeline')
    parser.add_argument('-q', '--query', nargs=2, help='Search through X tweets with given query')
    parser.add_argument('-g', '--geo', nargs=2, help='east, west, or both with X many tweets')

    _run_args(parser.parse_args())
