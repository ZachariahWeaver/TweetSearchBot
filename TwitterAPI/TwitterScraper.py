consumer_key = config['twitter']['consumerkey'] #initialize tweepy authentication
consumer_secret = config['twitter']['consumersecret']
access_token = config['twitter']['accesstoken']
access_token_secret = config['twitter']['accesstokensecret']

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
for comment in reddit.subreddit("test").stream.comments(skip_existing=True): #copied stream initializer NEEDS CHANGE
    TweetNumbertoDataBuilder(tweet)
