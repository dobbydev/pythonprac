import pandas as pd
from collections import Counter
from prettytable import PrettyTable
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk import FreqDist
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
import nltk

def top_retweeets(tweetdf,topN):
    tweetdf.sort('retweet_count',ascending=False, inplace=True)    
    pt = PrettyTable(field_names=['Count', 'Text'])
    count=0
    for index, row in tweetdf.iterrows():
        print(count)
        if count> topN:
            break
        pt.add_row( [row['text'].encode('utf-8'),row['retweet_count']])
        pt.max_width['Text'] = 50
        pt.align= 'l'
        count+= 1
    print(pt)    

tweet_df = pd.DataFrame.from_csv("narendramodi_tweets.csv",encoding='utf-8')
top_retweeets(tweet_df,5)

status_texts = tweet_df['text']
words = [ w 
          for t in status_texts 
              for w in t.split() ]

stopwords = set(stopwords.words('english'))
more_stop = ['.','!','?','&',"'",'(',')',',','-',':',';','..','...','|','||','~','im',"i'm"] 
for extra in more_stop:
    stopwords.add(extra)
vectorizer = CountVectorizer( stop_words=stopwords, min_df=0.01, max_df=.99)
dtm = vectorizer.fit_transform(tweet_df['text']).toarray()
vocab  = vectorizer.get_feature_names()
vocab = np.array(vocab)

tfvectorizer = TfidfVectorizer(min_df=2,stop_words='english')
d=tfvectorizer.fit_transform(status_texts)
vocab  = tfvectorizer.get_feature_names()
vocab = np.array(vocab)

word_counts = sorted(Counter(vocab).values(), reverse=True)
plt.loglog(word_counts)
plt.ylabel("Freq")
plt.xlabel("Word Rank")

vocabulary = "a list of words I want to look for in the documents".split()
vect = TfidfVectorizer(sublinear_tf=True, max_df=0.5, analyzer='word',  stop_words='english', vocabulary=vocabulary)





words = pd.Series(' '.join(tweet_df['text']).split(' '))
print(words.value_counts())
for i in range(2, 6):
    print( tweet_df['text'][i])
    print( nltk.word_tokenize(tweet_df['text'][i]))
    print ()