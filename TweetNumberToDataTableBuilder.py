# this loop collects new tweets and stores the data points Number to data table
# psuedo code placeholder, need to find how to stream tweets from an twitter account

WordsToTweetNumbers(tweet.text)

INSERT INTO Tweets(number, source, created_at, attachments, text, public_metrics, id)
VALUES (tweet.source, tweet.created_at, tweet.attachments, tweet.text, tweet.public_metrics, tweet.index);


