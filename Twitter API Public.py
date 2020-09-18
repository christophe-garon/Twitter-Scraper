#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
from datetime import date, datetime
import sys
import base64
import requests
import re


def get_usernames():
    while True:
        try: 
            usernames = input("Enter the Twitter usernames you'd like to track, sperated by a comma (example: @TxDOTDallas, @TxDOTFortWorth): ")
            if usernames[0][0] != '@':
                raise ValueError # this will send it to the print message and back to the input option            
            else:
                username_list = usernames.replace(" ", "").replace("@", "from:@").replace(",", " OR ")
            
            return username_list
        
        except ValueError:
            print("Hmmm... " + usernames + " do not look like a valid usernames. Let's try that again.")




def get_keywords():
    while True:
        try: 
            keywords = input("Enter the keywords you'd like to track, sperated by a comma (example: ramp, closure): ")
            keywords = keywords.replace(", ", ",").split(",")
            
            for keyword in keywords:
                if (" ") in keyword:
                    raise ValueError # this will send it to the print message and back to the input option            
            
            keywords = " OR ".join(keywords)
            return keywords
        
        except ValueError:
            print("Hmmm...keywords can only be single words, not phrases. Let's try that again.")



def get_blacklist():
    while True:
        try: 
            blacklist = input("Enter the words you'd like to avoid in your search, sperated by a comma (example: traffic, wreck): ")
            blacklist = blacklist.replace(", ", ",").split(",")
            
            for word in blacklist:
                if (" ") in word:
                    raise ValueError # this will send it to the print message and back to the input option  
            
            blacklist = " -".join(blacklist)
            blacklist = "-" + blacklist
            return blacklist
        
        except ValueError:
            print("Hmmm...blacklisted words can only be single words, not phrases. Let's try that again.")


# In[45]:


def format_usernames():
   
   # Format usernames for search
   usernames = user['usernames'][0]
   usernames = usernames.replace(" ", "").split("OR")
   
   # Organize first set of usernames
   usernames_one = usernames[0]
   for item in usernames[1:12]:
       usernames_one += ' OR ' + item
       
   # Organize second set if > 12 usernames   
   try: 
       usernames_two = usernames[12]
   
       for item in usernames[13:24]:
           usernames_two += ' OR ' + item

   except IndexError:
       usernames_two = []
       
       
   # Organize second set if > 24 usernames    
   try: 
       usernames_three = usernames[24]
   
       for item in usernames[25:36]:
           usernames_three += ' OR ' + item

   except IndexError:
       usernames_three = []
       
       
   # Organize second set if > 36 usernames   
   try: 
       usernames_four = usernames[36]
   
       for item in usernames[37:48]:
           usernames_four += ' OR ' + item

   except IndexError:
       usernames_four = []
       
       
    # Organize second set if > 48 usernames   
   try: 
       usernames_five = usernames[48]
   
       for item in usernames[49:60]:
           usernames_five += ' OR ' + item

   except IndexError:
       usernames_five = []
              
       
    # Organize second set if > 60 usernames   
   try: 
       usernames_six = usernames[60]
   
       for item in usernames[61:72]:
           usernames_six += ' OR ' + item

   except IndexError:
       usernames_six = []
       
   return usernames_one, usernames_two, usernames_three, usernames_four, usernames_five, usernames_six


# In[47]:


try:
    user = pd.read_csv("twitter_settings.csv", index_col=0)
    keywords = user['keywords'][0]
    blacklist = user['blacklist'][0]
    
    usernames_one, usernames_two, usernames_three, usernames_four, usernames_five, usernames_six = format_usernames()
    

except IOError:
    
    print("Let's get you setup!")
    
    # Get Scrape Settings
    usernames = get_usernames()
    keywords = get_keywords()
    blacklist = get_blacklist()
    date = date.today().strftime('%Y-%m-%d')
    filename = sys.argv[0]
    
    # create user dataframe
    col = {"usernames":usernames, "keywords":keywords, "blacklist":blacklist}
    user = pd.DataFrame(col, index= [date])
    user.to_csv("twitter_settings.csv", encoding='utf-8', index=True)
    
    usernames_one, usernames_two, usernames_three, usernames_four, usernames_five, usernames_six = format_usernames()
        
    print("Your twitter settings are all setup! You can edit these search settings directly    through the file named 'twitter_settings.csv'. You can find this file at " + filename)


# In[51]:


usernames_two


# In[32]:


#Define your keys from the developer portal
client_key = 'Insert Client Key'
client_secret = 'Insert Client Secret'

#Reformat the keys and encode them
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

# Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)

#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')


# In[33]:


#Adding authorization to base URL 

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


# In[34]:


#Adding search parameters: ('OR' = or)('+' = and)('-' = not) *(space interpreted as &)

search_params = {'q': usernames_one + " + " + keywords + " + " + blacklist,}

#Adding Twitter search API to base URL
search_url = '{}1.1/search/tweets.json'.format(base_url)

#Putting all elements together and execute request 
resp_one = requests.get(search_url, headers=search_headers, params=search_params)


#Get the data from the 1st request
import json
scrape_one = json.loads(resp_one.content)

search_params


# In[35]:


#Extracting desired data from 1st scrape as lists
users = []
tweet_dates = []
kw_tweets = []


for tweet in scrape_one['statuses']:
    users.append(tweet['user']['screen_name'])
#     tweet['text'] = re.sub(r'RT @(\w+): ','', tweet['text'])
    kw_tweets.append(tweet['text'])
    dates = datetime.strptime(tweet['created_at'][4:-11], '%b %d %H:%M:%S').strftime('%m/%d %H:%M')
    tweet_dates.append(dates)


# In[36]:


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


# In[37]:


if usernames_two != []:
    
    #Call the API again for the remaining users

    search_params = {'q': usernames_two + " + " + keywords + " + " + blacklist,}

    #Adding Twitter search API to base URL
    search_url = '{}1.1/search/tweets.json'.format(base_url)

    #Putting all elements together and execute request 
    resp_two = requests.get(search_url, headers=search_headers, params=search_params)


    #Get the data from the 2st request
    import json
    scrape_two = json.loads(resp_two.content)
    
    
    #Extracting desired data from 2nd scrape as lists
    users_two = []
    tweet_dates_two = []
    kw_tweets_two = []


    for tweet in scrape_two['statuses']:
        users_two.append(tweet['user']['screen_name'])
    #     tweet['text'] = re.sub(r'RT @(\w+): ','', tweet['text']) 
        kw_tweets_two.append(tweet['text'])
        dates = datetime.strptime(tweet['created_at'][4:-11], '%b %d %H:%M:%S').strftime('%m/%d %H:%M')
        tweet_dates_two.append(dates)

        
    #Create DataFrame two    
    scrape2 = {
            "User" : users_two,
            "Date" : tweet_dates_two,
            "Tweet" : kw_tweets_two
    }

    #Create DataFrame
    df2 = pd.DataFrame(scrape2)
    df2
    
    # Join DataFrames into one
    join = pd.concat([df1,df2], ignore_index=True)
    join

    
else:
    join = df1


# In[38]:


if usernames_three != []:
    
    #Call the API again for the remaining users

    search_params = {'q': usernames_three + " + " + keywords + " + " + blacklist,}

    #Adding Twitter search API to base URL
    search_url = '{}1.1/search/tweets.json'.format(base_url)

    #Putting all elements together and execute request 
    resp_two = requests.get(search_url, headers=search_headers, params=search_params)


    #Get the data from the 2st request
    import json
    scrape_two = json.loads(resp_two.content)
    
    
    #Extracting desired data from 2nd scrape as lists
    users_two = []
    tweet_dates_two = []
    kw_tweets_two = []


    for tweet in scrape_two['statuses']:
        users_two.append(tweet['user']['screen_name'])
    #     tweet['text'] = re.sub(r'RT @(\w+): ','', tweet['text']) 
        kw_tweets_two.append(tweet['text'])
        dates = datetime.strptime(tweet['created_at'][4:-11], '%b %d %H:%M:%S').strftime('%m/%d %H:%M')
        tweet_dates_two.append(dates)

        
    #Create DataFrame two    
    scrape2 = {
            "User" : users_two,
            "Date" : tweet_dates_two,
            "Tweet" : kw_tweets_two
    }

    #Create DataFrame
    df3 = pd.DataFrame(scrape2)
    df3
    
    # Join DataFrames into one
    join = pd.concat([join,df3], ignore_index=True)
    join

    
else:
    pass


# In[39]:


if usernames_four != []:
    
    #Call the API again for the remaining users

    search_params = {'q': usernames_four + " + " + keywords + " + " + blacklist,}

    #Adding Twitter search API to base URL
    search_url = '{}1.1/search/tweets.json'.format(base_url)

    #Putting all elements together and execute request 
    resp_two = requests.get(search_url, headers=search_headers, params=search_params)


    #Get the data from the 2st request
    import json
    scrape_two = json.loads(resp_two.content)
    
    
    #Extracting desired data from 2nd scrape as lists
    users_two = []
    tweet_dates_two = []
    kw_tweets_two = []


    for tweet in scrape_two['statuses']:
        users_two.append(tweet['user']['screen_name'])
    #     tweet['text'] = re.sub(r'RT @(\w+): ','', tweet['text']) 
        kw_tweets_two.append(tweet['text'])
        dates = datetime.strptime(tweet['created_at'][4:-11], '%b %d %H:%M:%S').strftime('%m/%d %H:%M')
        tweet_dates_two.append(dates)

        
    #Create DataFrame two    
    scrape2 = {
            "User" : users_two,
            "Date" : tweet_dates_two,
            "Tweet" : kw_tweets_two
    }

    #Create DataFrame
    df4 = pd.DataFrame(scrape2)
    df4
    
    # Join DataFrames into one
    join = pd.concat([join,df4], ignore_index=True)
    join

    
else:
    pass


# In[40]:


if usernames_five != []:
    
    #Call the API again for the remaining users

    search_params = {'q': usernames_five + " + " + keywords + " + " + blacklist,}

    #Adding Twitter search API to base URL
    search_url = '{}1.1/search/tweets.json'.format(base_url)

    #Putting all elements together and execute request 
    resp_two = requests.get(search_url, headers=search_headers, params=search_params)


    #Get the data from the 2st request
    import json
    scrape_two = json.loads(resp_two.content)
    
    
    #Extracting desired data from 2nd scrape as lists
    users_two = []
    tweet_dates_two = []
    kw_tweets_two = []


    for tweet in scrape_two['statuses']:
        users_two.append(tweet['user']['screen_name'])
    #     tweet['text'] = re.sub(r'RT @(\w+): ','', tweet['text']) 
        kw_tweets_two.append(tweet['text'])
        dates = datetime.strptime(tweet['created_at'][4:-11], '%b %d %H:%M:%S').strftime('%m/%d %H:%M')
        tweet_dates_two.append(dates)

        
    #Create DataFrame two    
    scrape2 = {
            "User" : users_two,
            "Date" : tweet_dates_two,
            "Tweet" : kw_tweets_two
    }

    #Create DataFrame
    df5 = pd.DataFrame(scrape2)
    df5
    
    # Join DataFrames into one
    join = pd.concat([join,df5], ignore_index=True)
    join

    
else:
    pass


# In[41]:


if usernames_six != []:
    
    #Call the API again for the remaining users

    search_params = {'q': usernames_six + " + " + keywords + " + " + blacklist,}

    #Adding Twitter search API to base URL
    search_url = '{}1.1/search/tweets.json'.format(base_url)

    #Putting all elements together and execute request 
    resp_two = requests.get(search_url, headers=search_headers, params=search_params)


    #Get the data from the 2st request
    import json
    scrape_two = json.loads(resp_two.content)
    
    
    #Extracting desired data from 2nd scrape as lists
    users_two = []
    tweet_dates_two = []
    kw_tweets_two = []


    for tweet in scrape_two['statuses']:
        users_two.append(tweet['user']['screen_name'])
    #     tweet['text'] = re.sub(r'RT @(\w+): ','', tweet['text']) 
        kw_tweets_two.append(tweet['text'])
        dates = datetime.strptime(tweet['created_at'][4:-11], '%b %d %H:%M:%S').strftime('%m/%d %H:%M')
        tweet_dates_two.append(dates)

        
    #Create DataFrame two    
    scrape2 = {
            "User" : users_two,
            "Date" : tweet_dates_two,
            "Tweet" : kw_tweets_two
    }

    #Create DataFrame
    df6 = pd.DataFrame(scrape2)
    df6
    
    # Join DataFrames into one
    join = pd.concat([join,df6], ignore_index=True)
    join

    
else:
    pass


# In[42]:


# Remove any duplicate tweets and sort

join['Tweet'].replace('(https://t.co)/(\w+)', r'\1', regex=True).drop_duplicates()
tweets = join.loc[join['Tweet'].replace('(https://t.co)/(\w+)', r'\1', regex=True).drop_duplicates().index]
tweets = tweets.sort_values(by=['Date'], ascending=False)
tweets.reset_index(drop=True, inplace=True)
tweets


# In[43]:


#Export table to Excel without index column
# writer = pd.ExcelWriter("kw_tweets.xlsx", engine='xlsxwriter')
# df.to_excel(writer, index=False)
# writer.save() 


# In[44]:


#Export data to CSV file
tweets.to_csv("kw_tweets.csv", encoding='utf-8', index=False)





