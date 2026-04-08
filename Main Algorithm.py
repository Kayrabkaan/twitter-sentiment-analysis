import tweepy
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

df = pd.read_csv('cleaned_dataset_2.csv')

relevant_df = df[df['sentiment'] != 'Irrelevant']

def clean_tweet(tweet):
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r'@\S+', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'\n', ' ', tweet)
    tweet = re.sub(r'[^A-Za-z0-9\s]', '', tweet)
    return tweet

relevant_df['cleaned_tweet'] = relevant_df['tweet'].apply(clean_tweet)

X = relevant_df['cleaned_tweet']
y = relevant_df['sentiment']

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAGJjuAEAAAAAWHKY9MYWIWHNfuhEJ0tW7AVMHsQ%3DnCQGudvvzG3MCG1USo87pN5WwQni1lEKD2jYSG8gWEFfom1Big'

client = tweepy.Client(bearer_token=bearer_token)

query = '#ElonMusk'
tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100)

if tweets.data:
    tweet_list = [tweet.text for tweet in tweets.data]
else:
    tweet_list = []

cleaned_tweet_list = [clean_tweet(tweet) for tweet in tweet_list]

new_tweets_vectorized = vectorizer.transform(cleaned_tweet_list)

new_predictions = clf.predict(new_tweets_vectorized)

for tweet, sentiment in zip(tweet_list, new_predictions):
    print()
    
unique, counts = np.unique(new_predictions, return_counts=True)
sentiment_counts = dict(zip(unique, counts))

colors = {'Positive': 'green', 'Neutral': 'cyan', 'Negative': 'red'}

labels = sentiment_counts.keys()
sizes = sentiment_counts.values()
explode = (0, 0, 0)
plt.pie(sizes, explode=explode, labels=labels, colors=[colors[key] for key in labels], autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Sentiment Analysis of New Tweets')
plt.figure(figsize=(8, 6))
colors = {'Positive': 'green', 'Neutral': 'cyan', 'Negative': 'red'}
plt.bar(sentiment_counts.keys(), sentiment_counts.values(), color=[colors[key] for key in sentiment_counts.keys()])
plt.xlabel('Sentiment')
plt.ylabel('Number of Tweets')
plt.title('Sentiment Analysis of New Tweets')
plt.show()