consumer_key = getTwitterConsumerKey() #initialize tweepy authentication
consumer_secret = getTwitterConsumerKey()
access_token = getTwitterAccessToken()
access_token_secret = getTwitterAccessTokenSecret()

    auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)
for comment in reddit.subreddit("test").stream.comments(skip_existing=True): #copied stream initializer NEEDS CHANGE
    TweetNumbertoDataBuilder(tweet)
