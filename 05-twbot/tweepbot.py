import tweepy
import time
from conf import consumer_key,consumer_secret,access_token,access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()
print (user.name) #prints your name.
print (user.screen_name)
print (user.followers_count)

search = "Kika"
numberOfTweets = 2

# if get RateLimitError from API take a break
def limit_handle(cursor):
  while True:
    try:
      yield cursor.next()
    except tweepy.RateLimitError:
      time.sleep(1000)

# get followers, if follower name eq - follow
for follower in limit_handle(tweepy.Cursor(api.followers).items()):
  if follower.name == 'Kika':
    print(follower.name)
    follower.follow()

# search/get tweet to fav
for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
    try:
        tweet.favorite()
        print('Retweeted the tweet')
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break