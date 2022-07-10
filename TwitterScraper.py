import configparser

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

client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret, return_type=dict,
                       wait_on_rate_limit=False)
dict = client.get_users_tweets(id=1544738842611154946, max_results=100, user_auth=False)
print(dict)

temp = dict.get('data')
conn = psycopg2.connect(
    host=config['postgresql']['host'],
    database=config['postgresql']['database'],
    user=config['postgresql']['user'],
    password=config['postgresql']['password'])

cursor = conn.cursor()

postgres_insert_query = """ INSERT INTO tweet (word, tweetnumber) VALUES (%s,%s)"""

for d in temp:
    word = d.get('text')
    numbers = [d.get('id')]

    record_to_insert = (word, numbers)
    cursor.execute(postgres_insert_query, record_to_insert)

    conn.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into mobile table")

