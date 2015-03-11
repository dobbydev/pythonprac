import twitter
import json
import sys
from csv import writer
import pandas as pd
import time
from datetime import datetime

class TimelineMiner(object):
    def __init__(self):
        self.df =pd.DataFrame()
        self.twitter_api=None
      
    def oauth_login(self):
        CONSUMER_KEY='PH4kOU5UjVGA6WToxuXIgdQNa'
        CONSUMER_SECRET='B7J9QjJgklw0az3tAAoqWwdmCuwlP6Rrv5x0Pmwtnj7YkrgXnS'
        OAUTH_TOKEN='2773642093-uJA8WbUQriMHJky0HSi4kJBXkBLvRzBOpdcV8Hd'
        OAUTH_TOKEN_SECRET ='v5jyJ92d10pHViefZx0QqYMRvLnsfWcbahd0eeTKqqn6a'
        auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)
        self.twitter_api = twitter.Twitter(auth=auth)
     
    def __get_date(self, timelinedate):
        timest = datetime.strptime(timelinedate, "%a %b %d %H:%M:%S +0000 %Y")
        date = timest.strftime("%Y-%d-%m %H:%M:%S")
        return date
   
    def saveas_csv(self, path):
        self.df.to_csv(path, encoding ='utf-8')
        print(self.df)
    
        
        
    def get_timeline(self,userName, max=0):
        tweet_ids = [self.twitter_api.statuses.user_timeline(screen_name=userName, count=1)[0]['id']] # the ID of my last tweet
        last_count = 200
        counter =0
        while last_count ==200:
            timeline = self.twitter_api.statuses.user_timeline(screen_name= userName, count=200, max_id=tweet_ids[-1])
            print(len(timeline))
            for i in range(len(timeline)):
                 self.df.loc[counter,'text']= timeline[i]['text'] 
                 self.df.loc[counter,'date'] =self.__get_date(timeline[i]['created_at'])
                 self.df.loc[counter,'retweet_count'] =timeline[i]['retweet_count'] 
                 self.df.loc[counter,'favorite_count'] =timeline[i]['favorite_count'] 
                 if 'retweeted_status' in timeline[i]:
                      self.df.loc[counter,'retweet_by'] =timeline[i]['retweeted_status']['user']['screen_name']
                 self.df.loc[counter,'mentions1'] = [(timeline[i]['entities']['user_mentions'][0]['screen_name'] if len(timeline[i]['entities']['user_mentions']) >= 1 else None)]
                 self.df.loc[counter,'mentions2'] = [(timeline[i]['entities']['user_mentions'][1]['screen_name'] if len(timeline[i]['entities']['user_mentions']) >= 2 else None) ]
                 self.df.loc[counter,'hashtags1'] = [(timeline[i]['entities']['hashtags'][0]['text'] if len(timeline[i]['entities']['hashtags']) >= 1 else None) ]
                 self.df.loc[counter,'hashtags2'] = [(timeline[i]['entities']['hashtags'][1]['text'] if len(timeline[i]['entities']['hashtags']) >= 2 else None) ]
                 counter += 1
                 if max and counter >= max:
                    break
                 sys.stdout.flush()   
                 sys.stdout.write('\rTweets downloaded: %s' %counter)  
            if max and counter >= max:
                print(max)
                print(counter >= max)
                break
            last_count = len(timeline)
            tweet_ids.append(timeline[-1]['id'])
            time.sleep(1)
        print()
                 



tm = TimelineMiner()
tm.oauth_login()
tm.get_timeline("PMOIndia",1000)
tm.saveas_csv("PMOIndia_tweets2.csv")

tm.get_timeline("narendramodi",1000)
tm.saveas_csv("narendramodi_tweets3.csv")
 
