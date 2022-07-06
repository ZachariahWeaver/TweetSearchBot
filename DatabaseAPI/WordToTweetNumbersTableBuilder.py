for words in tweettext: #messy psuedo code for building word to tweet number table
    if db.contains word:
        db.addNumber(word, number)
    else:
        db.addRow(word, number)
