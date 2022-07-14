import configparser
import string
import psycopg2
import praw
from datetime import datetime

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


def getlink(tweetnumber):
    return "https://twitter.com/user/status/%s" % (tweetnumber,)

def getdate(iso_string):
    date_time = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return "%s:%s %s· %s %s, %s · " % (date_time.strftime('%I'), date_time.strftime('%M'), date_time.strftime('%p'), date_time.strftime('%b'), date_time.strftime('%d'), date_time.strftime('%Y'))

def gettext(tweettext):
    formattedtweettext = "    "
    index = 0
    tweettext = tweettext.replace("\n", " ")
    print(tweettext)
    tweettext = list(tweettext.split(" "))
    print(tweettext)
    while index < len(tweettext):
        formattedtweettext = formattedtweettext + tweettext[index] + " "
        index = index + 1
        if index % 10 == 0:
            formattedtweettext = formattedtweettext + "\n    "

    if index % 10 != 0:
        formattedtweettext = formattedtweettext + "\n    "

    return formattedtweettext


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
                       'here)](' \
                       'https://github.com/ZachariahWeaver/TweetSearchBot) '
        s = comment.body[5:]  # take the comment without the bot tag  and leading space(!SNB )
        s = s.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
        s = s.lower()
        s = s.split()  # create an array of lower case words to check f

        if s:
            postgres_select_query = """SELECT tweetnumber FROM tweet WHERE word = '%s'""" % (s[0],)
            cursor.execute(postgres_select_query)
            a = cursor.fetchone()[0]
            print(a)
            for word in s:
                postgres_select_query = """SELECT tweetnumber FROM tweet WHERE word = '%s'""" % (word,)
                cursor.execute(postgres_select_query)
                tweetnumber_records = cursor.fetchone()[0]
                a = list(set(a) & set(tweetnumber_records))
                print(a)
            if a:
                for id, tweet in enumerate(a):  # add all tweets that match to comment reply
                    print(tweet)
                    postgres_tweetid_select_query = """SELECT * FROM tweetid WHERE tweetnumber = %s""" % (tweet,)
                    cursor.execute(postgres_tweetid_select_query)
                    tweetinfo = cursor.fetchone()
                    print(tweetinfo)
                    reply = "{0}{1}".format(reply, (
                            '    ←       Tweet\n'
                            '    ⬛⬛⬛ Ryan Cohen 🅥                                     \n'
                            '    ⬛🧔⬛ @ryancohen\n'
                            '    ⬜⬜⬜\n'
                            '    \n'
                            + gettext(tweetinfo[1]) +
                            '\n'
                            '    %s%s\n' % (getdate(tweetinfo[2]), tweetinfo[4]) +  # variable that has date and source
                            '    ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n'
                            '\n'
                            '    %s Retweets      %s Quote Tweets      %s Likes\n' % (
                            tweetinfo[7], tweetinfo[6], tweetinfo[5]) +
                            '    ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n'
                            '           🗨️             🔄             ❤️             🔗\n'
                            '    ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n'
                            '[Tweet ' + str(id + 1) + "]" + "(" + getlink(tweet) + ") \n\n"))
            else:
                fail = True
                print("fail 1")
        else:
            fail = True
            print("fail 2")

        word_list = str(s)
        word_list = word_list.replace("\'", "")
        if fail:
            print("Unfortunately the words you requested were not found all at once in any one tweet! Try again using "
                  "fewer terms or checking your spelling.")
            comment.reply(body=("Unfortunately the words you requested were not found all at once in any one tweet! "
                                "Try again using fewer terms or checking your spelling. " + reply_ending))

        else:
            print(reply_opening + "\n" + word_list + "\n" + reply)

            comment.reply(body=(reply_opening + word_list + "\n\n" + reply + reply_ending))
