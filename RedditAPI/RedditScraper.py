reddit = praw.Reddit(
    client_id=getRedditClientID(),  # dummy data to keep keys private
    client_secret=getRedditClientSecret(),
    password=getRedditPassword(),
    user_agent="Console:SaleNotifierBot:v1.0 (by u/z_weaver))",
    username="TweetSearchBot",
)

for comment in reddit.subreddit("test").stream.comments(skip_existing=True):
    print("New comment detected! \n")  # console statement to show bot is detecting new comments
    reply = ""  # Start with an empty string which will be added to making the final reply
    fail = "\n \n Unfortunately the words you requested were not found all at once in any one tweet! Try again using fewer terms or checking your spelling."
    if comment.body[:4] == "!TSB" and len(
            comment.body) < 286:  # check for request marker and refuse requests that are too long
        print("Comment requests bot utility!\n \n")
        reply_opening = "The words you want to search are: "

        s = comment.body[5:]  # take the comment without the bot tag  and leading space(!SNB )
        s = s.translate(str.maketrans('', '', string.punctuation))  # remove punctionation
        s = s.lower()
        s = s.split()  # create an array of lower case words to check f

        if s:
            a = twitterUserdict[s[0]]
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
            for id, tweet in enumerate(a):  # add all tweets that match to comment reply
                reply = reply + "[Tweet " + str(id + 1) + "]" + "(" + getLink(tweet) + ") " + \
                        "[Image " + str(id + 1) + "]" + "(" + getImage(tweet) + ") " + \
                        getDate(tweet)
        else:
            reply = fail

        word_list = str(s)
        word_list = word_list.replace("\'", "")

        print(reply_opening + "\n" + word_list + "\n" + reply)

        comment.reply(reply_opening + word_list + "\n\n" + reply)
