# Kaitlyn Randolph
# HW2 Part 5
# 2/7/2020

import csv
import sys
import string
import math
import random

# Increases field size so that large speeches may be printed out
csv.field_size_limit(sys.maxsize)
# Adapted from: https://docs.python.org/2/library/csv.html
with open('state-of-the-union.csv') as csvfile:
    fieldnames = ["year", "text"]
    reader = csv.DictReader(csvfile, fieldnames)
    docNum = 0
    tf = {}
    yeartf = {}
    documents = {}
    vocabcount = {}
    idf = {}
    tfidf = {}
    temp = {}
    for row in reader:
        translator = str.maketrans('', '', string.punctuation)
        row["text"] = str(row["text"]).translate(translator).lower().split()
        if row['year'] not in documents.keys():
            documents[str(row['year'])] = row['text']
    for year, doc in documents.items():
        for word in doc:
            if word not in tf.keys():
                tf[str(word)] = doc.count(word) / len(doc)
        yeartf[str(year)] = tf
        tf = {}
    for doc in yeartf.values():
        for word in doc:
            if word not in vocabcount.keys():
                vocabcount[str(word)] = 1
            else:
                vocabcount[str(word)] += 1
    for word, count in vocabcount.items():
            idf[str(word)] = math.log2(len(documents)/count)
    for year, doc in yeartf.items():
        for word in doc:
            temp[str(word)] = yeartf[str(year)][str(word)] * idf[str(word)] / len(yeartf[str(year)])
        tfidf[str(year)] = temp
        temp = {}
    selected_speech = random.choice(list(tfidf.keys()))
    num = 0
    print("Top twenty words from State of the Union in", selected_speech, ":")
    for word in sorted(tfidf[selected_speech], key=tfidf[selected_speech].get, reverse=True):
        print(word, end=": ")
        print(tfidf[selected_speech][word], end="\n")
        num += 1
        if num == 21:
            break

    temp = {}
    decsum = {}
    decade = {"1900", "1901", "1902", "1903", "1904", "1905", "1906", "1907", "1908", "1909"}
    print("Top twenty words from State of the Union in 1900s:")
    for year, doc in tfidf.items():
        if year in decade:
            for word in doc:
                if str(word) not in decsum.values():
                    temp[str(word)] = tfidf[str(word)]
                else:
                    temp[str(word)] += tfidf[str(word)]
        decsum[str(word)] = temp
        temp = {}
    for word in sorted(decsum, key=decsum.get, reverse=True):
        print(word, end=": ")
        print(decsum[word], end="\n")
        num += 1
        if num == 21:
            break
