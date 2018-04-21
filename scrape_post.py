# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 11:04:33 2018

@author: Varun
"""

import json, requests

subreddit = 'news'

r = requests.get(
    'http://www.reddit.com/r/{}.json'.format(subreddit),
    headers={'user-agent': 'Mozilla/5.0'}
)

# view structure of an individual post
#print(json.dumps(r.json()['data']['children'][0]))

for post in r.json()['data']['children']:
    print(post['data']['title'])
    print(post['data']['selftext'])
    print('------------------------------------------')