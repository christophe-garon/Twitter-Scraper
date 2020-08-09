#!/usr/bin/env python
# coding: utf-8

# In[745]:


from datetime import date, datetime, timezone, timedelta

import base64

#Define your keys from the developer portal
client_key = 'zgIy2FjgQsNk3ZAyoxcpB1idB'
client_secret = 'B64nkla0ynrTeo6M0372pMUCQTex64cO33GDGrFeShBMAudXE7'

#Reformat the keys and encode them
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

# Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)

#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')


# In[746]:


#Adding authorization to base URL 

import requests

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

auth_data = {
    'grant_type': 'client_credentials'}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)


#Creating bearer token

access_token = auth_resp.json()['access_token']

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)}


# In[747]:


#Adding search parameters: ('OR' = or)('+' = and)('-' = not) *(space interpreted as &)

search_params = {
    'q': 'from:@DriveTSG OR from:@DFWConnector OR from:@TxDOTDallas OR from:@TxDOTLufkin OR from:@TXDOTWF\
        OR from:@TxDOTParis OR from:@TxDOTFortWorth\
        + shift OR ramp OR switch OR months OR shift OR widening OR closed OR closure OR detour OR long-term OR complete\
        + -wreck -alternating -inside -single -vehicle -left -right -expect -far-left -far-right',}


#Adding Twitter search API to base URL
search_url = '{}1.1/search/tweets.json'.format(base_url)

#Putting all elements together and execute request 
resp_one = requests.get(search_url, headers=search_headers, params=search_params)


#Get the data from the 1st request
import json
scrape_one = json.loads(resp_one.content)


# In[749]:


#Extracting desired data from 1st scrape as lists
users = []
tweet_dates = []
kw_tweets = []


for tweet in scrape_one['statuses']:
    users.append(tweet['user']['screen_name'])
    kw_tweets.append(tweet['text'])
    dates = datetime.strptime(tweet['created_at'][4:-11], '%b %d %H:%M:%S').strftime('%m/%d %H:%M')
    tweet_dates.append(dates)


# In[750]:


#Creating df1 via pandas

import pandas as pd

#Creating columns names and adding their data
scrape1 = {
    "User" : users,
    "Date" : tweet_dates,
    "Tweet" : kw_tweets,   
}

#Create DataFrame
df1 = pd.DataFrame(scrape1)
df1


# In[751]:


#Call the API again for the remaining users

search_params = {
    'q': 'from:@635east OR from:@TxDOTBryan OR from:@TxDOTTyler OR from:@TxDOTAtlanta OR from:@cityofdentontx\
        + shift OR ramp OR switch OR months OR shift OR widening OR closed OR closure OR detour OR long-term OR complete\
        + -wreck -alternating -inside -single -vehicle -left -right -expect -far-left -far-right',}

#Adding Twitter search API to base URL
search_url = '{}1.1/search/tweets.json'.format(base_url)

#Putting all elements together and execute request 
resp_two = requests.get(search_url, headers=search_headers, params=search_params)


#Get the data from the 2st request
import json
scrape_two = json.loads(resp_two.content)


# In[752]:


#Extracting desired data from 2nd scrape as lists

users_two = []
tweet_dates_two = []
kw_tweets_two = []


for tweet in scrape_two['statuses']:
    users_two.append(tweet['user']['screen_name'])
    kw_tweets_two.append(tweet['text'])
    dates = datetime.strptime(tweet['created_at'][4:-11], '%b %d %H:%M:%S').strftime('%m/%d %H:%M')
    tweet_dates_two.append(dates)


# In[696]:


#Creating df2 via pandas

scrape2 = {
        "User" : users_two,
        "Date" : tweet_dates_two,
        "Tweet" : kw_tweets_two
}

#Create DataFrame
df2 = pd.DataFrame(scrape2)
df2


# In[697]:


#Join df1 & df2 and sort by Date

join = pd.concat([df1,df2], ignore_index=True)
join


# In[698]:


join['Tweet'].replace('(https://t.co)/(\w+)', r'\1', regex=True).drop_duplicates()
tweets = join.loc[join['Tweet'].replace('(https://t.co)/(\w+)', r'\1', regex=True).drop_duplicates().index]
tweets = tweets.sort_values(by=['Date'], ascending=False)
tweets.reset_index(drop=True, inplace=True)
tweets


# In[699]:


#Export table to Excel without index column
# writer = pd.ExcelWriter("kw_tweets.xlsx", engine='xlsxwriter')
# df.to_excel(writer, index=False)
# writer.save() 


# In[700]:


#Export data to CSV file
tweets.to_csv("kw_tweets.csv", encoding='utf-8', index=False)


# In[10]:



consumer_key = 'zgIy2FjgQsNk3ZAyoxcpB1idB'
consumer_secret = 'B64nkla0ynrTeo6M0372pMUCQTex64cO33GDGrFeShBMAudXE7'
access_token = '95816074-NCtH7DqHuAESpTnvo4KiP3xu1yIcXBMJ5YK4Lcc96'
access_token_secret = 'BDq4ysbNAtgL3ad3RBvKObJHdYK4PQ4LKPGOAgfa0PeVp'


# In[573]:





# In[ ]:




