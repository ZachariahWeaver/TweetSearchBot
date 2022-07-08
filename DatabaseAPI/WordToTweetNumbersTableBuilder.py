for words in tweettext: #messy psuedo code for building word to tweet number table
    if db.contains word:
        db.addNumber(word, number)
        newNumbers =numbers + SELECT numbers FROM Words
        UPDATE Words SET number = newNumbers, WHERE CustomerID = word
    else:
        INSERT INTO Words(word, number)