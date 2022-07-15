import configparser
import string
import psycopg2
import praw
from datetime import datetime


def getlink(tweet_number):
    return "https://twitter.com/user/status/%s" % (tweet_number,)


def getdate(iso_string):
    date_time = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return "%s:%s %s· %s %s, %s · " % (
        date_time.strftime('%I'), date_time.strftime('%M'), date_time.strftime('%p'), date_time.strftime('%b'),
        date_time.strftime('%d'), date_time.strftime('%Y'))


def gettext(tweet_text):
    formatted_tweet_text = "    "
    count = 0
    tweet_text = tweet_text.replace("\n", " ")
    tweet_text = list(tweet_text.split(" "))
    while count < len(tweet_text):
        formatted_tweet_text = formatted_tweet_text + tweet_text[count] + " "
        count = count + 1
        if count % 10 == 0:
            formatted_tweet_text = formatted_tweet_text + "\n    "

    if count % 10 != 0:
        formatted_tweet_text = formatted_tweet_text + "\n    "

    return formatted_tweet_text


config = configparser.ConfigParser()
config.read('CONFIG.INI')

reddit = praw.Reddit(
    client_id=config['reddit']['clientid'],
    client_secret=config['reddit']['clientsecret'],
    password=config['reddit']['password'],
    user_agent="Console:SaleNotifierBot:v1.0 (by u/z_weaver))",
    username="TweetSearchBot",
)

conn = psycopg2.connect(
    host=config['postgresql']['host'],
    database=config['postgresql']['database'],
    user=config['postgresql']['user'],
    password=config['postgresql']['password'])

cursor = conn.cursor()

for comment in reddit.subreddit("testingground4bots").stream.comments(skip_existing=True):
    print("New comment detected! \n")  # console statement to show bot is detecting new comments
    reply = ""  # Start with an empty string which will be added to making the final reply
    fail = False
    if comment.body[:4] == "!TSB" and len(
            comment.body) < 286:  # check for request marker and refuse requests that are too long
        print("Comment requests bot utility!\n \n")
        reply_opening = "The words you want to search are: "
        reply_ending = '_____ \n^(Hello, I\'m TweetSearchBot, I find tweets for you' \
                       'and reply with a formatted version ^(For more info, requests or complaints go ' \
                       'here)' \
                       'https://github.com/ZachariahWeaver/TweetSearchBot) '
        reply_fail = "No results found, try again considering the following error: "
        s = comment.body[5:]  # take the comment without the bot tag  and leading space(!SNB )
        s = s.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
        s = s.lower()
        s = s.split()  # create an array of lower case words to check f

        if s:
            postgres_select_query = """SELECT tweetnumber FROM tweet WHERE word = '%s'""" % (s[0],)
            cursor.execute(postgres_select_query)
            a = cursor.fetchone()
            if a is not None:
                a = a[0]
                for word in s:
                    postgres_select_query = """SELECT tweetnumber FROM tweet WHERE word = '%s'""" % (word,)
                    cursor.execute(postgres_select_query)
                    tweet_number_records = cursor.fetchone()
                    if tweet_number_records is not None:
                        tweet_number_records = tweet_number_records[0]
                    else:
                        a = None
                        fail = True
                        break
                    a = list(set(a) & set(tweet_number_records))
                 if a:
                    for index, tweet in enumerate(a) and index < 10:  # add all tweets that match to comment reply
                        postgres_tweet_id_select_query = """SELECT * FROM tweetid WHERE tweetnumber = %s""" % (tweet,)
                        cursor.execute(postgres_tweet_id_select_query)
                        tweet_info = cursor.fetchone()
                        reply = "{0}{1}".format(reply, (
                                '    ←       Tweet\n'
                                '    ⬛⬛⬛ Ryan Cohen 🅥                                     \n'
                                '    ⬛🧔⬛ @ryancohen\n'
                                '    ⬜⬜⬜\n'
                                '    \n'
                                + gettext(tweet_info[1]) +
                                '\n'
                                '    %s%s\n' % (
                                    getdate(tweet_info[2]), tweet_info[4]) +  # variable that has date and source
                                '    ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n'
                                '\n'
                                '    %s Retweets      %s Quote Tweets      %s Likes\n' % (
                                    tweet_info[7], tweet_info[6], tweet_info[5]) +
                                '    ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n'
                                '           🗨️             🔄             ❤️             🔗\n'
                                '    ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n'
                                '[Tweet ' + str(index + 1) + "]" + "(" + getlink(tweet) + ") \n\n"))
                else:
                    fail = True
                    reply_fail = reply_fail + "The words given were not found in any one single tweet"
            else:
                fail = True
                reply_fail = reply_fail + "One of the words was not in any tweets currently indexed"

        else:
            fail = True
            reply_fail = reply_fail + "There were no valid words after the !TSB tag"

        word_list = str(s)
        word_list = word_list.replace("\'", "")
        if fail:
            print(reply_fail)
            comment.reply(body=("Unfortunately the words you requested were not found all at once in any one tweet! "
                                "Try again using fewer terms or checking your spelling. " + reply_ending))

        else:
            print(reply_opening + "\n" + word_list + "\n" + reply)

            comment.reply(body=(reply_opening + word_list + "\n\n" + reply + reply_ending))
