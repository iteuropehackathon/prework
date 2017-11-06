
import tweepy
import json
from datetime import date
from s3_utils import s3_save
import settings

class TweetsImport():
    def __init__(self):
        auth = tweepy.OAuthHandler(settings.consumer_key, settings.consumer_secret)
        auth.set_access_token(settings.access_token, settings.access_token_secret)
        self.api = tweepy.API(auth)

    # todo - free version allows to download only ~3300 records
    def load_twitter_history(self, name):
        all_tweets = []
        new_tweets = self.api.user_timeline(screen_name=name, count=200)
        all_tweets.extend(new_tweets)
        last = all_tweets[-1].id - 1
        while len(new_tweets) > 0:
            new_tweets = self.api.user_timeline(screen_name=name, count=200, max_id=last)
            all_tweets.extend(new_tweets)
            last = all_tweets[-1].id - 1
            print("Downloaded {} tweets.. ".format(len(all_tweets)))
        self.write_to_s3(name, all_tweets)

    def write_to_s3(self,name,  tweets):
        file_path = 'twitter/history/run_date={day}/{name}.txt'.format(day=date.today().isoformat(),name=name)
        body = "\n".join([json.dumps(tweet._json).replace("\n", " ") for tweet in tweets])
        s3_save(file_path, body)


if __name__ == '__main__':
    ti = TweetsImport()
    for account in settings.twitter_history_accounts:
        print "Load twitter history: {}".format(account)
        ti.load_twitter_history(account)