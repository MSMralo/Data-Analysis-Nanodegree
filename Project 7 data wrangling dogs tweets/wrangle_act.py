#!/usr/bin/env python
# coding: utf-8

# ## **Gathering and Extracting Data:**

# >in this section we will collect data of WeRateDogs from Twitter using Tweepy API and tweets ids provided in twitter-archive-enhanced.csv file

# In[1]:


#imporing all needed libraries

import tweepy
import requests as req
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from io import BytesIO
import seaborn as sns
import re 

get_ipython().run_line_magic('matplotlib', 'inline')


# **Tweepy API authorization**

# In[2]:


#providing all authorization keys to connect with Tweepy API

consumer_key = 'Hidden'
consumer_secret = 'Hidden'
access_token = 'Hidden'
access_secret = 'Hidden'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


# #testing Api connection and extracting one tweet 
# tweet = api.get_status('1198860382976106496', tweet_mode='extended')
# print(tweet.retweet_count)
# print(tweet.favorite_count)
# print(tweet.full_text)

# In[3]:


#reading twitter-archive-enhanced.csv in pandas
twitter_archive_df = pd.read_csv('twitter-archive-enhanced.csv')


# In[4]:


twitter_archive_df


# In[5]:


#check if there is any null values in tweet_id coloumn
pd.to_numeric(twitter_archive_df['tweet_id'], errors='coerce').notnull().all()


# #extracting tweets contents from tweepy Api using ids saved in twitter-archive-enhanced.csv file
# #storing extracted data in tweet_json.text file containing every tweet details
# 
# with open("tweet_json.txt", "w") as outfile:
#     for tweet_id in twitter_archive_df['tweet_id']:
#         #checking that all tweets ids has valid 18 length numbers
#         if len(str(tweet_id)) == 18:
#             try:
#                 tweet_json = api.get_status(tweet_id, tweet_mode='extended', wait_on_rate_limit=True)
#                 json.dump(tweet_json._json, outfile) 
#                 outfile.write("\n") 
#         #ignoring invalid tweet ids and printing error
#             except Exception as exp:
#                     print(str(tweet_id) + str(exp))

# In[6]:


json_data = []
with open('tweet_json.txt', 'r') as file: 
    json_tweet = file.readline()
    while json_tweet:
        json_dict = json.loads(json_tweet)
        json_data.append(json_dict)
        json_tweet = file.readline()
        
api_df = pd.DataFrame.from_dict(json_data)


# **Image prediction data**

# In[7]:


image_predict= req.get('https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv', allow_redirects=True)

image_predict_df = pd.read_csv(BytesIO(image_predict.content), sep='\t')
image_predict_df.to_csv('image-predict.tsv', sep='\t', )


# ## Assessing Data
# image_predict.content

# In[8]:


#exploring json file and favorites and retweets counts
api_df


# In[9]:


api_df.info()


# In[10]:


api_df.describe()


# In[11]:


api_df.duplicated(subset=['id']).any()


# In[12]:


api_df.extended_entities[0]


# In[13]:


api_df.possibly_sensitive_appealable.value_counts()


# In[14]:


api_df.possibly_sensitive.value_counts()


# In[15]:


api_df.entities[0]


# In[16]:


api_df[api_df.retweeted.notnull()].retweeted[0]


# In[17]:


api_df[api_df.retweeted_status.notnull()].retweeted_status[31]


# In[18]:


#exploring image_predict file content
image_predict_df


# In[19]:


image_predict_df.describe()


# In[20]:


image_predict_df.info()


# In[21]:


image_predict_df.duplicated(subset=['tweet_id']).any()


# In[22]:


#exploring twitter-archive-enhanced file data 
twitter_archive_df


# In[23]:


twitter_archive_df.describe()


# In[24]:


twitter_archive_df.info()


# In[25]:


twitter_archive_df.doggo.value_counts()


# In[26]:


twitter_archive_df.pupper.value_counts()


# In[27]:


twitter_archive_df.floofer.value_counts()


# In[28]:


twitter_archive_df.puppo.value_counts()


# In[29]:


twitter_archive_df[twitter_archive_df['rating_numerator'] < 10]


# In[30]:


twitter_archive_df[twitter_archive_df['rating_denominator'] != 10]


# ## Quality issues

# **api_df table**
# 
# <ul>
# <li>Zero Values columns (possibly_sensitive , possibly_sensitive_appealable ) which adds no value to our data</li>
# <li>values in column Source contains href a html tag which we won't be using in any of our analysis. </li>
# <li>not related columns data to the scope of our analysis ( user, favorited, retweeted ) </li>
# <li>Null values columns (contributors, coordinates, geo, place, quoted status id, quoted status id str) which adds no value to our data</li>
# </ul>

# **image_predict table**
# <p>
# data is seperated in many different ways in columns (p1, p2, p3) like the use of (-, _)
# 

# **twitter_archive_df table**
# <ul>
# <li>different prefix of dog names ( a , an)</li>
# <li>empty cells are not defined as null but instead defined as string</li>
# <li>rating is not correctly defined/entered as mentioned</li>
# <li>Column( doggo, floofer, puppo, and pupper )values either None or its column name</li>
# <li>timestamp is not defined as datetime but instead defined as string</li>
# </ul>

# ## Tideness issues

# <ul>
# <li>the p1, p2, p3 contain redundancy since the p1, p2, p3 is not unique throughout the row in image_predict</li>
# <li>created_at / timestamp, source, text, in_reply_to_status_id, in_reply_to_user_id are duplicated in api_df table and twitter_archive table</li>
# <li>api_df and image_predict should be part of twitter_archive table</li>
# <li>Entities data seems to contain image information which are already contain in the twitter archive data, like the image_url and extended url</li>
# <li>Extended entities column contains duplicate information of the entities column</li>
# </ul>

# # Cleaning Data

# In[31]:


#taking copies of all tables for cleaning and to confirm cleaning after
twitter_archive_df_clean = twitter_archive_df.copy()
image_predict_clean = image_predict_df.copy()
api_clean = api_df.copy()


# In[32]:


twitter_archive_df_clean


# ## Tidiness

# some of api_df data are retweets

# **Define**

# we only need the genuine tweets so we are going to drop all retweets and their data

# **Code**

# In[33]:


tweets_without_retweet = api_clean[api_clean.retweeted_status.notnull()].retweeted_status
tweets_without_retweet = pd.DataFrame(tweets_without_retweet.tolist())


# In[34]:


api_clean = api_clean[api_clean.retweeted_status.isnull()]

api_clean = api_clean.drop(['retweeted_status'], axis=1)


# In[35]:


api_clean = api_clean.append(tweets_without_retweet)


# **Test**

# In[36]:


api_clean.shape[0] == api_df.shape[0]


# **Define**

# data is seperated in many different ways in columns (p1, p2, p3) like the use of (-, _)
# 

# **Code**

# In[37]:


predict_clean = pd.DataFrame()
temp = pd.DataFrame()


# In[38]:


col_to_use = ['p1','p2', 'p3']

for col in col_to_use:
    temp = pd.DataFrame()
    temp['prediction'] = image_predict_clean[col]
    temp['is_dog'] = image_predict_clean[col+'_dog']
    if (col == 'p1'):
        predict_is_dog_clean = temp
    else:
        predict_is_dog_clean.append(temp)


# **Test**

# In[39]:


predict_is_dog_clean.drop_duplicates(inplace=True)


# In[40]:


image_predict_clean = image_predict_clean.drop(['p1_dog', 'p2_dog', 'p3_dog'], axis=1)


# In[41]:


predict_is_dog_clean.duplicated(['prediction']).any()


# In[42]:


image_predict_clean.info()


# **Define**

# timestamp is not defined as datetime but instead defined as string

# **Code**

# In[43]:


twitter_archive_df_clean = twitter_archive_df_clean.drop([
    'timestamp', 'text', 'source', 'in_reply_to_status_id', 'in_reply_to_user_id'], axis=1)


# **Test**

# In[44]:


all_columns = pd.Series(list(api_clean) + list(twitter_archive_df_clean))
all_columns[all_columns.duplicated()]


# **Define**

# Merging the api_df and image_predict table to the twitter_archive table, joining on tweet_id and id.

# **Code**

# In[45]:


twitter_archive_df_clean = pd.merge(api_clean, twitter_archive_df_clean,
                            left_on='id', right_on='tweet_id', how='right')


# In[46]:


twitter_archive_df_clean = twitter_archive_df_clean.drop([
    'tweet_id'], axis=1)


# In[47]:


twitter_archive_df_clean.info()


# In[48]:


twitter_archive_df_clean = pd.merge(twitter_archive_df_clean, image_predict_clean, left_on='id', right_on='tweet_id', how='left')


# **Test**

# In[49]:


twitter_archive_df_clean.info()


# ## Quality

# Removing columns which has empty values

# **Define**

# Dropping Null values columns (contributors, coordinates, geo, place, quoted status id, quoted status id str) which adds no value to our data

# **Code**

# In[50]:


twitter_archive_df_clean = twitter_archive_df_clean.drop([
    'user', 'favorited', 'retweeted', 'contributors', 
    'coordinates', 'geo', 'place', 'quoted_status_id', 
    'quoted_status_id_str'], axis=1)


# **Test**

# In[51]:


twitter_archive_df_clean.info()


# **Define**

# Column in twitter_archive_df ( doggo, floofer, puppo, and pupper )values either None or its column name

# **Code**

# In[52]:


def use_true_or_false_for_column(archive, col_name):
    if archive[col_name] == col_name:
        return True
    else:
        return False
    
twitter_archive_df_clean['doggo'] = twitter_archive_df_clean.apply(
    use_true_or_false_for_column, args=('doggo',), axis=1)
twitter_archive_df_clean['floofer'] = twitter_archive_df_clean.apply(
    use_true_or_false_for_column, args=('floofer',), axis=1)
twitter_archive_df_clean['puppo'] = twitter_archive_df_clean.apply(
    use_true_or_false_for_column, args=('puppo',), axis=1)
twitter_archive_df_clean['pupper'] = twitter_archive_df_clean.apply(
    use_true_or_false_for_column, args=('pupper',), axis=1)


# **Test**

# In[53]:


twitter_archive_df_clean.info()


# **Define**

# Zero Values columns (possibly_sensitive , possibly_sensitive_appealable ) which adds no value to our data

# **Code**

# In[54]:


twitter_archive_df_clean = twitter_archive_df_clean.drop([
    'possibly_sensitive','possibly_sensitive_appealable'], axis=1)


# **Test**

# In[55]:


twitter_archive_df_clean.info()


# **Define**

# values in column Source contains href a html tag which we won't be using so we are going to extract only the link 

# **Code**

# In[56]:


twitter_archive_df_clean['source'] = twitter_archive_df_clean.source.str.extract(r'href="(.+?)"')


# **Test**

# In[57]:


twitter_archive_df_clean['source'].value_counts()


# **Define**

# empty cells are not defined as null but instead defined as string
# 

# **Code**

# In[58]:


twitter_archive_df_clean.name.replace('None', np.nan, inplace=True)


# **Test**

# In[59]:


(twitter_archive_df_clean.name == 'None').any()


# **Define**

# 
# different prefix of dog names ( a , an)

# **Code**

# In[60]:


twitter_archive_df_clean['name'][twitter_archive_df_clean['name'].str.match('[a-z]+', na= False)] = np.nan


# **Test**

# In[61]:


(twitter_archive_df_clean.name == 'a').any()


# In[62]:


(twitter_archive_df_clean.name == 'an').any()


# In[63]:


(twitter_archive_df_clean.name == 'the').any()


# **Define**

# rating is not correctly defined/entered as mentioned we will look up wrong ratings and correct them manually
# 

# **Code**

# In[64]:


#checking rows with wrong rating_numerator
pd.set_option('display.max_colwidth', -1) #show full text in full_text column
twitter_archive_df_clean[twitter_archive_df_clean.full_text.str.contains(r"(\d+\.\d*\/\d+)", na=False)][['full_text', 'rating_numerator']]


# In[65]:


#converting rating_numerator to float to be able to add decimal values
twitter_archive_df_clean.rating_numerator= twitter_archive_df_clean.rating_numerator.astype(dtype='float64', copy=True)


# In[66]:


#correcting rows showing above manually
twitter_archive_df_clean.at[42,'rating_numerator'] = 13.5
twitter_archive_df_clean.at[605,'rating_numerator'] = 9.75
twitter_archive_df_clean.at[606,'rating_numerator'] = 9.75
twitter_archive_df_clean.at[677,'rating_numerator'] = 11.27
twitter_archive_df_clean.at[1625,'rating_numerator'] = 9.50
twitter_archive_df_clean.at[1648,'rating_numerator'] = 11.26


# **Test**

# In[67]:


#checking column data type
twitter_archive_df_clean.info()


# In[68]:


# Check all values are filled
twitter_archive_df_clean.rating_numerator.isnull().sum()


# In[69]:


#taking a look on the fixed data
twitter_archive_df_clean[twitter_archive_df_clean.full_text.str.contains(r"(\d+\.\d*\/\d+)", na=False)][['full_text', 'rating_numerator']]


# In[70]:


with open('twitter_archive_master.csv', 'w') as outfile:  
    outfile.write(twitter_archive_df_clean.to_csv(index=False))
    
with open('predictions_mapping_master.csv', 'w') as outfile:  
    outfile.write(predict_is_dog_clean.to_csv(index=False))


# # Visualization

# In[71]:


predict_mappings = pd.read_csv('predictions_mapping_master.csv')


# In[72]:


twitter_archive_master = pd.read_csv('twitter_archive_master.csv')

predictions_mapping_master = pd.read_csv('predictions_mapping_master.csv')


# In[73]:


sns.set(rc={'figure.figsize':(11.5,8.5)})
def setlabels(xlabel, ylabel):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


# In[74]:


#Counts of Names - Histograms
twitter_archive_master.name.value_counts()[:10].sort_values(ascending=True).plot.barh(width=0.9,color=sns.color_palette('deep',10))
plt.title('Counts of Names')
setlabels('Count', 'Name')


# Based on the above histogram, Charlie is the most popular name, followed by Bo and cooper

# **what is the correlation between retweet count and favorite count?**

# In[75]:


#Favorite and Retweet Count - Regplot
sns.set_palette("deep")
sns.regplot(
    x='retweet_count', 
    y='favorite_count', data=twitter_archive_master)
setlabels("Retweet Count", "Favorite Count")

plt.title('Favorite and Retweet Count')


# From the above Regplot, its clear there is a correlation between favorite count and retweet count.

# **what patterns for the rating given in the tweet?** <p>
# based on the time the tweet was made.

# In[76]:


#Median of dog tweet per day - subplot

twitter_archive_master['created_at'] = pd.to_datetime(twitter_archive_master.created_at)

plt.subplots(figsize=(12,10))
twitter_archive_master.groupby(twitter_archive_master['created_at'].dt.date).median()['rating_numerator'].plot()
setlabels('Day where tweet are created', 'Median Rating')
plt.title('The median rate of dog tweet per day')


# The above plot, not clear enough, it indicate an increase in the rating of the dog given. We will it divide it to bigger interval.

# In[77]:


#Median of dog tweet per day - subplot

twitter_archive_master.groupby(twitter_archive_master['created_at'].dt.to_period("M")).median()['rating_numerator'].plot()
setlabels('Month of tweet created', 'Median Rating')
plt.title('The Median rate of dog tweet per month')


# From the above plot, the rating given to dogs increases by time.

# **Does @weRateDogs tweets get more tweets by popularity?** <p>
# Let's first plot the number of tweet data per month.

# In[78]:


twitter_archive_master.groupby(twitter_archive_master['created_at'].dt.to_period("M")).count()['id'].plot()


# Ignoring the sharp drop in July 2017, which might be due to the time we collected the data, the plot above shows that @weRateDogs does not become more active in rating dogs by time. Actually, the tweet count has decreased.

# **what about the retweet count and the favorite count per month?** <p>
# To measure the account popularity, its better to use median of the retweet count and favorite count instead of the sum, as median is less affected by outlier and the sum may be affected by the number of tweets made per month, which differs each month.

# In[79]:



twitter_archive_master.groupby(twitter_archive_master['created_at'].dt.to_period("M")).median()['retweet_count'].plot(label='Retweet Count')
twitter_archive_master.groupby(twitter_archive_master['created_at'].dt.to_period("M")).median()['favorite_count'].plot(label='Favorite Count')

plt.legend()
setlabels('Tweet created date', 'Count')
plt.title('Median of Favorite Count and Retweet Count for each month')


# From the above, we can see that there is retweet count and favorite count is increasing, despite the decrease of the number of dog rating tweet made.

# **How about confidence is the image prediction?**

# In[80]:


#image prediction - boxplot
fig = plt.figure()
ax = fig.add_subplot(111)
plot = ax.boxplot([
    twitter_archive_master.p1_conf[twitter_archive_master.p1_conf.notnull()],
    twitter_archive_master.p2_conf[twitter_archive_master.p2_conf.notnull()],
    twitter_archive_master.p3_conf[twitter_archive_master.p3_conf.notnull()]], 
    labels=[
    'p1 confidence', 'p2 confidence', 'p3 confidence'])
plt.title('Boxplot of first, second, and third prediction confidence')
plt.ylabel('Confidence')


# From the above boxplot, we can see that first prediction tend to have higher confidence than the second and third prediction. We can also see that for the first prediction is more than 50% of the image has more than 50% confidence.

# ## Resources
# https://stackoverflow.com/questions/51068498/valueerror-cannot-index-with-vector-containing-na-nan-values/51969304
# https://stackoverflow.com/questions/25351968/how-to-display-full-non-truncated-dataframe-information-in-html-when-convertin
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_numeric.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.astype.html

# In[ ]:




