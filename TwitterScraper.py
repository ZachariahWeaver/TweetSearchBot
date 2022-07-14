import configparser
import string
import requests
import tweepy
import psycopg2

config = configparser.ConfigParser()
config.read('CONFIG.INI')

consumer_key = config['twitter']['consumerkey']  # initialize tweepy authentication
consumer_secret = config['twitter']['consumersecret']
access_token = config['twitter']['accesstoken']
access_token_secret = config['twitter']['accesstokensecret']
bearer_token = config['twitter']['bearertoken']

lasttweet = None
client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret, return_type=dict,
                       wait_on_rate_limit=False)
dict = client.get_users_tweets(id=1544738842611154946, max_results=100, since_id = lasttweet, user_auth=False, tweet_fields=['created_at','source,id','text','public_metrics'])
print(dict)

temp = dict.get('data')
meta = dict.get('meta')
lasttweet = meta.get('oldest_id')
conn = psycopg2.connect(
    host=config['postgresql']['host'],
    database=config['postgresql']['database'],
    user=config['postgresql']['user'],
    password=config['postgresql']['password'])

cursor = conn.cursor()

for d in temp:
    metrics = d.get('public_metrics')
    postgreSQL_insert_Query = "INSERT INTO tweetid (tweetnumber, tweettext, tweetdate, tweetimage, tweetsource, tweetlikecount, tweetquotecount, tweetretweetcount) VALUES(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (d.get('id'),d.get('text'),d.get('created_at'),'none',d.get('source'),metrics.get('like_count'),metrics.get('quote_count'),metrics.get('retweet_count'))
    cursor.execute(postgreSQL_insert_Query)

    numbers = d.get('id')
    text = d.get('text').lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    word = text.split()
    word = list(set(word))
    print(word)


    for w in word:
        postgreSQL_select_Query = "DO $$ BEGIN IF EXISTS( SELECT 1 FROM tweet WHERE word = '%s') THEN UPDATE tweet SET word = word, tweetnumber = array_append(tweetnumber, %s) WHERE word = '%s'; ELSE INSERT INTO tweet(word, tweetnumber) VALUES('%s', '{%s}'); END IF; END $$;" % (w, numbers, w, w, numbers)
        cursor.execute(postgreSQL_select_Query)
        conn.commit()
        count = cursor.rowcount
        print("Record inserted successfully into table", w, numbers)


cursor.close()
conn.close()
