#import praw
#import tweepy
#import re
#import string
#import time
import configparser



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

    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
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
main()