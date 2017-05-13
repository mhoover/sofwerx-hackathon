#!/usr/bin/python
import base64
import httplib
import json
import os
import re
import requests
import time
import urllib

import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from textblob import TextBlob


# constants
STEEM = 'https://steemit.com'
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': os.getenv('MSFT_EMOTION1'),
}
params = urllib.urlencode({
})

# functions
def get_data(tail, posts=False):
    raw = requests.get('{}/{}'.format(STEEM, tail))
    soup = BeautifulSoup(raw.content, 'html.parser')
    js = json.loads(soup.find('script', type='application/json').text)

    if not posts:
        return js['global']['accounts'], js['global']['content']
    else:
        return js['global']['content']


def get_account_data(tail):
    raw = requests.get('{}/{}'.format(STEEM, tail))
    soup = BeautifulSoup(raw.content, 'html.parser')
    try:
        js = json.loads(soup.find('script', type='application/json').text)
        return js['global']['accounts']
    except AttributeError:
        pass


def pic_sentiment(pic):
    body = str({'url': '{}'.format(pic)})

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        return response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# gather trending and hot data
trend, hot = [get_data(x) for x in ['trending', 'hot']]

# simplify account/user information
users = []
for t in [trend[0], hot[0]]:
    for k, v in t.items():
        try:
            users.append({
                'id': t[k]['id'],
                'name': t[k]['name'],
                'reputation': t[k]['reputation'],
                'post_count': t[k]['post_count'],
                'last_post': t[k]['last_post'],
                'voting_power': t[k]['voting_power'],
                'reward_vesting_bal': t[k]['reward_vesting_balance'],
                'reward_vesting_steem': t[k]['reward_vesting_steem'],
                'sbd_balance': t[k]['sbd_balance'],
                'about': json.loads(t[k]['json_metadata']).get('profile').get('about'),
            })
        except:
            users.append({
                'id': t[k]['id'],
                'name': t[k]['name'],
                'reputation': t[k]['reputation'],
                'post_count': t[k]['post_count'],
                'last_post': t[k]['last_post'],
                'voting_power': t[k]['voting_power'],
                'reward_vesting_bal': t[k]['reward_vesting_balance'],
                'reward_vesting_steem': t[k]['reward_vesting_steem'],
                'sbd_balance': t[k]['sbd_balance'],
                'about': None,
            })
users = np.unique(users)

# simplify content information
content = []
for c in [trend[1], hot[1]]:
    for k, v in c.items():
        content.append({
            'author': k.split('/')[0],
            'id': c[k]['id'],
            'title': c[k]['title'],
            'votes': c[k]['net_votes'],
            'payout_value': c[k]['pending_payout_value'],
            'url': c[k]['url'],
            'pics': json.loads(c[k]['json_metadata']).get('image'),
        })

# chase down posts
posts = [get_data(x, posts=True) for x in [entry['url'] for entry in content]]

# simplify post content
post = []
for p in posts:
    for k, v in p.items():
        post.append({
            'votes': p[k]['stats']['total_votes'],
            'id': p[k]['id'],
            'body': p[k]['body'],
            'url': p[k]['url'],
            'author': p[k]['author'],
        })

# create edgelist
el = np.unique([re.findall('@([A-Za-z0-9]*)', x['url']) for x in post])
el = [x for x in el if len(x) > 1]
el = [x for x in el if x[0] != x[1]]

# go collect all user information
user_info = [get_account_data('@{}'.format(x)) for x in np.unique(el)]
user_info_real = [x for x in user_info if x]
uinfo = []
for u in user_info_real:
    for k, v in u.items():
        try:
            uinfo.append({
                'id': u[k]['id'],
                'name': u[k]['name'],
                'reputation': u[k]['reputation'],
                'post_count': u[k]['post_count'],
                'last_post': u[k]['last_post'],
                'voting_power': u[k]['voting_power'],
                'reward_vesting_bal': u[k]['reward_vesting_balance'],
                'reward_vesting_steem': u[k]['reward_vesting_steem'],
                'sbd_balance': u[k]['sbd_balance'],
                'about': json.loads(u[k]['json_metadata']).get('profile').get('about'),
            })
        except:
            uinfo.append({
                'id': u[k]['id'],
                'name': u[k]['name'],
                'reputation': u[k]['reputation'],
                'post_count': u[k]['post_count'],
                'last_post': u[k]['last_post'],
                'voting_power': u[k]['voting_power'],
                'reward_vesting_bal': u[k]['reward_vesting_balance'],
                'reward_vesting_steem': u[k]['reward_vesting_steem'],
                'sbd_balance': u[k]['sbd_balance'],
                'about': None,
            })

# collect objects as data frames
pictures = [[{'user': x['author'], 'pic': y} for y in x['pics']] for x in content if x['pics']]

user_df = pd.DataFrame(uinfo)
post_df = pd.DataFrame(post)
el_df = pd.DataFrame(el, columns=['rec', 'snd'])
pic_df = pd.DataFrame([item for subl in pictures for item in subl])

# run sentiment analysis on pictures
sentiments = []
for pic in pic_df.pic:
    sentiments.append(pic_sentiment(pic))
    time.sleep(2.7)

sentiments_clean = []
for sentiment in sentiments:
    try:
        sentiments_clean.append(json.loads(sentiment)[0]['scores'])
    except:
        sentiments_clean.append({
            'anger': None,
            'contempt': None,
            'disgust': None,
            'fear': None,
            'happiness': None,
            'neutral': None,
            'sadness': None,
            'surprise': None,
        })
pic_sentiments_df = pd.DataFrame(sentiments_clean)
pic_df = pd.concat([pic_df, pic_sentiments_df], axis=1)
pic_df_agg = (pic_df
              .groupby('user')[['anger', 'contempt', 'disgust', 'fear',
                                'happiness', 'neutral', 'sadness', 'surprise']]
              .mean())
pic_df_agg['dom_pic_emotion'] = pic_df_agg.idxmax(axis=1)
pic_df_agg = pic_df_agg.reset_index()
user_df = user_df.merge(pic_df_agg[['user', 'dom_pic_emotion']], how='left',
                        left_on='name', right_on='user')
user_df.dom_pic_emotion.fillna('Unknown', inplace=True)
user_df.drop('user', axis=1, inplace=True)

# run sentiment analysis on text
text_sentiments = [TextBlob(x).sentiment for x in post_df.body]
post_df['polarity'] = [item[0] for item in text_sentiments]
post_df['subjectivity'] = [item[1] for item in text_sentiments]
post_df_agg = post_df.groupby('author')[['votes', 'polarity', 'subjectivity']].mean().reset_index()
user_df = user_df.merge(post_df_agg, how='left', left_on='name', right_on='author')
user_df.drop('author', axis=1, inplace=True)

# output data
user_df.to_csv('steem_user_attributes.csv', index=False, sep=',', encoding='utf-8')
el_df.to_csv('steem_edgelist.csv', index=False, sep=',', encoding='utf-8')
