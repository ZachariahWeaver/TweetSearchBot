import praw
#import re
import string
#import time


def getLink(tweetNumber):
    return "https://twitter.com/settings/" + str(tweetNumber)


def getImage(tweetNumber):
    #if tweet contains image:
    return "https://i.imgur.com/RdduwZo.png"
   #else:
        #return ""


def getDate(tweetNumber):
    return '{tweetTime} · {tweetDay} · {tweetYear} · {tweetSource}\n\n'.format(tweetTime=tweetTime,tweetDay=tweetDay, tweetYear= tweetYear, tweetSource=tweetSource)
def getText(tweetNumber):
    return '{tweetText}'.format()

def main():
    reddit = praw.Reddit(
        client_id = "123",
        client_secret="abc",
        password="xyz",
        user_agent="Console:SaleNotifierBot:v1.0 (by u/z_weaver))",
        username="TweetSearchBot",
    )
    ryancohen_dict = {
        "i": [149],
        "have": [149],
        "a": [149, 148],
        "crush": [149],
        "on": [149],
        "china": [149, 148],
        "emoji": [149],
        "has": [148],
        "nationwide": [148],
        "high": [148],
        "speed": [148],
        "rail": [148],
        "network": [148],
        "that": [148],
        "spans": [148],
        "almost": [148],
        "22000": [148],
        "miles": [148],
        "this": [148],
        "is": [148],
        "an": [148],
        "amazing": [148],
        "achievement": [148],

    }

    reply_opening = "The words you want to search are: "

    for comment in reddit.subreddit("test").stream.comments(skip_existing=True):
        print("New comment detected! \n")
        reply = ""
        fail = "\n \n Unfortunately the words you requested were not found all at once in any one tweet!"
        if comment.body[:4] == "!SNB" and len(comment.body) < 286:
            print("Comment requests bot utility!\n \n")
            reply_opening = "The words you want to search are: "

            s = comment.body[5:]  # take the comment without the bot tag  and leading space(!SNB )
            s = s.translate(str.maketrans('', '', string.punctuation))  # remove punctionation
            s = s.lower()
            s = s.split()  # create an array of lower case words to check f

            if s:
                a = ryancohen_dict[s[0]]
                for word in s:
                    if word in ryancohen_dict.keys():
                        b = ryancohen_dict[word]
                        a = list(set(a) & set(b))
                    else:
                        reply = fail
                        break
            else:
                reply = fail

            if a:
                for id, tweet in enumerate(a):
                    reply = reply + "[Tweet " + str(id + 1) + "]" + "(" + getLink(tweet) + ") " +\
                            "[Image " + str(id + 1) + "]" + "(" + getImage(tweet) + ") " +\
                            getDate(tweet)
            else:
                reply = fail


            word_list = str(s)
            word_list = word_list.replace("\'", "")

            print(reply_opening + "\n" + word_list + "\n" + reply)

            comment.reply(reply_opening + word_list + "\n\n" + reply)


main()
