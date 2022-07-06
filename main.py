import praw
#import re
import string
#import time


def getLink(tweetNumber): #method to pull the link from a specified tweet in database
    return "https://twitter.com/settings/" + str(tweetNumber)   #placeholder data, needs to be formatted


def getImage(tweetNumber):
    #if tweet contains image: #method to return a image if there was attached to specified tweet
    return "https://i.imgur.com/RdduwZo.png" #sample image, real method will pull from data base
   #else:
        #return "" #if no image return nothing


def getDate(tweetNumber):
    return '{tweetTime} · {tweetDay} · {tweetYear} · {tweetSource}\n\n'.format(tweetTime=tweetTime,tweetDay=tweetDay, tweetYear= tweetYear, tweetSource=tweetSource) # returning the date and time tweet was posted
def getText(tweetNumber):
    return '{tweetText}'.format(tweetText = tweetText) #return the text body from specified tweet

def main(): #main method which runs on a loop to take in all new comments in specified subreddit
    reddit = praw.Reddit(
        client_id = "sample", #dummy data to keep keys private
        client_secret="sample",
        password="sample",
        user_agent="Console:SaleNotifierBot:v1.0 (by u/z_weaver))",
        username="TweetSearchBot",
    )
    twitterUser_dict = { #sample data which will eventually be stored in database
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
        print("New comment detected! \n") #console statement to show bot is detecting new comments
        reply = "" #Start with an empty string which will be added to making the final reply
        fail = "\n \n Unfortunately the words you requested were not found all at once in any one tweet! Try again using fewer terms or checking your spelling."
        if comment.body[:4] == "!TSB" and len(comment.body) < 286: #check for request marker and refuse requests that are too long
            print("Comment requests bot utility!\n \n")
            reply_opening = "The words you want to search are: "

            s = comment.body[5:]  #take the comment without the bot tag  and leading space(!SNB )
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
                for id, tweet in enumerate(a): # add all tweets that match to comment reply
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
