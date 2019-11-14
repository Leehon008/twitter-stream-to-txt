import json
import pandas as pd
import matplotlib.pyplot as plt
import re

#Next we will read the data in into an array that we call tweets.
tweets_data_path = '../data/twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

#We can print the number of tweets using the command below
print (len(tweets_data))

#structure the tweets data into a pandas DataFrame to simplify the data manipulation
tweets = pd.DataFrame()
# we will add 3 columns to the tweets DataFrame called text, lang, and country. text column contains the tweet, 
# lang column contains the language in which the tweet was written, and country the country from which 
# the tweet was sent.
tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)
#Next, we will create 2 charts: The first one describing the Top 5 languages 
# in which the tweets were written, 
tweets_by_lang = tweets['lang'].value_counts()
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

#and the second the Top 5 countries from which the tweets were sent.
tweets_by_country = tweets['country'].value_counts()
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')

#First, we will create a function that checks if a specific keyword is present in a text.
# We will do this by using regular expressions.
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

#we will add columns to our tweets DataFrame. 'ZimWildlife', 'ZimParks', 'ZimbabweWildlie','Zim Tourism']
tweets['ZimWildlife'] = tweets['text'].apply(lambda tweet: word_in_text('ZimWildlife', tweet))
tweets['ZimParks'] = tweets['text'].apply(lambda tweet: word_in_text('ZimParks', tweet))
tweets['ZimbabweWildlife'] = tweets['text'].apply(lambda tweet: word_in_text('ZimbabweWildlife', tweet))
tweets['Zim Tourism'] = tweets['text'].apply(lambda tweet: word_in_text('Zim Tourism', tweet))

#We can calculate the number of tweets for each programming language as follows:
print (tweets['ZimWildlife'].value_counts()[True])
print (tweets['ZimParks'].value_counts()[True])
print (tweets['ZimbabweWildlife'].value_counts()[True])
print (tweets['Zim Tourism'].value_counts()[True])

#We can make a simple comparaison chart by executing the following:
prg_langs = ['ZimWildlife', 'ZimParks', 'ZimbabweWildlife','Zim Tourism']
tweets_by_prg_lang = [tweets['ZimWildlife'].value_counts()[True], tweets['ZimParks'].value_counts()[True], tweets['ZimbabweWildlife'].value_counts()[True], tweets['Zim Tourism'].value_counts()[True]]]
x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')
# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: ZimWildlife vs. ZimParks vs. ZimbabweWildlife vs. Zim Tourism (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()

#Targeting relevant tweets
tweets['Tourism'] = tweets['text'].apply(lambda tweet: word_in_text('tourism', tweet))
tweets['wildlife'] = tweets['text'].apply(lambda tweet: word_in_text('wildlife', tweet))
#add an additional column called relevant that take value True if the tweet has either "programming" or "tutorial" keyword, otherwise it takes value False.
tweets['relevant'] = tweets['text'].apply(lambda tweet: word_in_text('Tourism', tweet) or word_in_text('wildlife', tweet))
#print the counts of relevant tweet by executing the commands below.
print tweets['ZimWildlife'].value_counts()[True]
print tweets['ZimParks'].value_counts()[True]
print tweets['ZimbabweWildlife'].value_counts()[True]
print tweets['Zim Tourism'].value_counts()[True]

#We can compare now the popularity of the programming languages by executing the commands below.
print tweets[tweets['relevant'] == True]['ZimWildlife'].value_counts()[True]
print tweets[tweets['relevant'] == True]['ZimParks'].value_counts()[True]
print tweets[tweets['relevant'] == True]['ZimbabweWildlife'].value_counts()[True]
print tweets[tweets['relevant'] == True]['Zim Tourism'].value_counts()[True]

#We can make a comparaison graph by executing the commands below:
tweets_by_prg_lang = [tweets[tweets['relevant'] == True]['ZimWildlife'].value_counts()[True], 
                      tweets[tweets['relevant'] == True]['ZimParks'].value_counts()[True], 
                      tweets[tweets['relevant'] == True]['ZimbabweWildlife'].value_counts()[True],
                      tweets[tweets['relevant'] == True]['Zim Tourism'].value_counts()[True]]
x_pos = list(range(len(prg_langs)))
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width,alpha=1,color='g')
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: ZimWildlife vs. ZimParks vs. ZimbabweWildlife vs. Zim Tourism (Relevant data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()

#we want to retrieve links to wildlife points on the web. We will start by creating a function that uses 
#regular expressions for retrieving link that start with "http://" or "https://" from a text. 
#This function will return the url if found, otherwise it returns an empty string.
def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''

#Next, we will add a column called link to our tweets DataFrame. This column will contain the urls information.
tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))
Next we will create a new DataFrame called tweets_relevant_with_link. This DataFrame is a subset of tweets DataFrame and contains all relevant tweets that have a link.

tweets_relevant = tweets[tweets['relevant'] == True]
tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != '']
#We can now print out all links for python, javascript, and ruby by executing the commands below:
print tweets_relevant_with_link[tweets_relevant_with_link['ZimWildlife'] == True]['link']
print tweets_relevant_with_link[tweets_relevant_with_link['ZimParks'] == True]['link']
print tweets_relevant_with_link[tweets_relevant_with_link['ZimbabweWildlife'] == True]['link']
print tweets_relevant_with_link[tweets_relevant_with_link['Zim Tourism'] == True]['link']