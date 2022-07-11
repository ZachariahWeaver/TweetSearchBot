import configparser
import string
import psycopg2
import praw
import random


config = configparser.ConfigParser()
config.read('CONFIG.INI')

reddit = praw.Reddit(
    client_id=config['reddit']['clientid'],  # dummy data to keep keys private
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


def getLink(tweetnumber):
    account = 'fake'
    return ("https://twitter.com/user/status/%s") % (tweetnumber, )


for comment in reddit.subreddit("test").stream.comments(skip_existing=True):
    print("New comment detected! \n" + comment.body)  # console statement to show bot is detecting new comments
    reply = ""  # Start with an empty string which will be added to making the final reply
    fail = False
    if comment.body[:4] == "!TSB" and len(
            comment.body) < 286:  # check for request marker and refuse requests that are too long
        print("Comment requests bot utility!\n \n")
        reply_opening = "The words you want to search are: "

        s = comment.body[5:]  # take the comment without the bot tag  and leading space(!SNB )
        s = s.translate(str.maketrans('', '', string.punctuation))  # remove punctionation
        s = s.lower()
        s = s.split()  # create an array of lower case words to check f

        if s:
            postgres_select_query = """SELECT tweetnumber FROM tweet WHERE word = '%s'""" % (s[0], )
            cursor.execute(postgres_select_query)
            a = cursor.fetchone()[0]
            print(a)
            for word in s:
                postgres_select_query = """SELECT tweetnumber FROM tweet WHERE word = '%s'""" % (word, )
                cursor.execute(postgres_select_query)
                tweetnumber_records = cursor.fetchone()[0]
                a = list(set(a) & set(tweetnumber_records))
                print(a)
        else:
            fail = True
            print("fail 2")

        if a:
            for id, tweet in enumerate(a):  # add all tweets that match to comment reply
                print(tweet)
                reply = reply +(
                "←       Tweet\n"\
                "    ⬛⬛⬛ Ryan Cohen 🅥                                     …\n"
                "    ⬛🧔⬛ @ryancohen\n"
                "    ⬜⬜⬜\n"
                "\n"
                "    I’m sick of seeing failed executives make millions in risk\n"
                "    free compensation while shareholders are left holding the\n"
                "    bag\n"
                "\n"
                "    10:56 AM · Jun 29, 2022 · Twitter for iPhone\n"
                "    ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n"
                "\n"
                "    4,323 Retweets      302 Quote Tweets      25.9K Likes\n"
                "    ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n"
                "           🗨️             🔄             ❤️             🔗
                "    ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n")
                [Tweet " + str(id + 1) + "]" + "(" + getLink(tweet) + ") \n"
        else:
            fail = True
            print("fail 3")

        word_list = str(s)
        word_list = word_list.replace("\'", "")
        if(fail):
            print("Unfortunately the words you requested were not found all at once in any one tweet! Try again using "
                  "fewer terms or checking your spelling.")
            comment.reply(body=("Unfortunately the words you requested were not found all at once in any one tweet! "
                                "Try again using fewer terms or checking your spelling."))
        else:
            print(reply_opening + "\n" + word_list + "\n" + reply)

            comment.reply(body = (reply_opening + word_list + "\n\n" + reply))
