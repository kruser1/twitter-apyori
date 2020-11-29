# -*- coding: utf-8 -*-
"""Twitter API Crawler.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nRrJwvvg6wRDEsNUwsiGFbYALYoEjUe0

# Twitter API Crawler

Ryan Kruse and Tharindu Lokukatagoda

### Import Packages
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd

"""Mount Google Drive so we can save resulting data as CSV"""

from google.colab import drive
drive.mount('/content/gdrive')

"""### Twitter Authorization

Set up Twitter authorization and check that it works.
"""

#imporitng tweepy lib
import tweepy

#setting up twitter credentials and accessing API
auth = tweepy.OAuthHandler('***************','*****************')
auth.set_access_token('***********************','*******************')
api = tweepy.API(auth)

#get twitter followers count of the current handle 
follower_count = api.get_user('realDonaldTrump').followers_count
print('Number of followers: ',follower_count)

print()
#declaring variable screen_name to current handle
screen_name = 'realDonaldTrump'

"""### Define Target Followers Function

Define our API crawler function to get the followers of a given account.
"""

def getTargetFollowers(screen_name, n=100, m=150):
  target_followers = list()
  n = m
  f = tweepy.Cursor(api.followers, screen_name).items(n)
  for fol in f:
    if not fol.protected:
      target_followers.append(fol.screen_name)
    if len(target_followers) == n:
      break
  print(len(target_followers))
  dff = pd.DataFrame(columns=target_followers)
  print(dff.shape)
  return(dff)

"""### Crawl API for Target Followers

Each column is an account that follows our target account.
"""

biden_df = getTargetFollowers('JoeBiden')
biden_df.head()

# rs = list(dff.index)
# for r in rs:
#   dff = dff.drop(r)
# dff

"""Optionally, write to CSV to save and read back in later."""

# dff=pd.read_csv("/content/gdrive/My Drive/twitter_arl.csv", index_col='Unnamed: 0')
# dff.head(3)

"""### Define Followers Functions

These functions help to get the data we want: other accounts followed by Biden and Trump's Twitter followers.
"""

def getFollowing(name, n):
  f = tweepy.Cursor(api.friends, name).items(n)
  following = list()
  for fol in f:
    following.append(fol.screen_name)
  print(len(following))
  return(following)

def getFollowingCount(name):
  c = api.get_user(name).friends_count
  return(c)

dff = biden_df.copy()

dff = pd.read_csv("/content/gdrive/My Drive/twitter_arl_biden.csv").set_index('Unnamed: 0')
print(dff.index)
print(dff.shape)
dff.head()

# time.sleep(60*15)
n = 100
count = 0
print(len(dff.sum()[dff.sum()==0]))
for col in dff.sum()[dff.sum()==0].index:
  print("Columns left:", len(dff.sum()[dff.sum()==0]))
  count += 1
  c = getFollowingCount(col)
  if c > n:
    c = n
  count += c
  print("Counts:")
  print(c)
  print(count)
  print("\n")
  if count < 204:
    following = getFollowing(col, n)
    for f in following:
      if f in dff.index:
        print("in")
        dff.loc[f, col] = 1
      else:
        dff.loc[f] = 0
        dff.loc[f, col] = 1
  else:
    print(dff)
    print("Sleeping for 15 minutes")
    time.sleep(15*60)
    count = c
    following = getFollowing(col, n)
    for f in following:
      if f in dff.index:
        print("in")
        dff.loc[f, col] = 1
      else:
        dff.loc[f] = 0
        dff.loc[f, col] = 1
  dff.to_csv("/content/gdrive/My Drive/twitter_arl_biden.csv")
dff

dff

dff.to_csv("/content/gdrive/My Drive/twitter_arl_biden.csv")

dff

# time.sleep(60*15)
n = 100
count = 0
print(len(dff.sum()[dff.sum()==0]))
for col in dff.sum()[dff.sum()==0].index:
  count += 1
  c = getFollowingCount(col)
  if c > n:
    c = n
  count += c
  print("Counts:")
  print(c)
  print(count)
  print("\n")
  if count < 200:
    following = getFollowing(col, n)
    for f in following:
      if f in dff.index:
        print("in")
        dff.loc[f, col] = 1
      else:
        dff.loc[f] = 0
        dff.loc[f, col] = 1
  else:
    print(dff)
    print("Sleeping for 15 minutes")
    time.sleep(15*60)
    count = c
    following = getFollowing(col, n)
    for f in following:
      if f in dff.index:
        print("in")
        dff.loc[f, col] = 1
      else:
        dff.loc[f] = 0
        dff.loc[f, col] = 1
  dff.to_csv("/content/gdrive/My Drive/twitter_arl_biden.csv")
dff

col

dff.sum()[dff.sum()==0].index

col

dff

dff.to_csv("/content/gdrive/My Drive/twitter_arl.csv")

dff.head(3)

count = 0
for col in dff.columns:
  if 1 not in dff[col].values:
    print(col)
    break
  count +=1
print(count)

dff['MD09166004'].values
