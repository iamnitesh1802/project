import os
import nltk 
import re
import pandas as pd
from nltk.tokenize import RegexpTokenizer, sent_tokenize
import numpy as np
from newspaper import Article


#extracing only title and article text
url1 = "https://insights.blackcoffer.com/man-and-machines-together-machines-are-more-diligent-than-humans-blackcoffe/"
art = Article(url1)
art.download()
art.parse()
scrap_data = art.text
title = art.title
DF=title + scrap_data
DF1 = DF.lower()
l1 = len(DF1)
#print(DF)

def cleantext(text):
    text = re.sub(r'@[A-za-z0-9]+','',text)
    text = re.sub(r'#','',text)
    text = re.sub(r'RT[\s]+','',text)
    text = re.sub(r'http?:\/\/\S+','',text)
    return text
DF2 = cleantext(DF1)
l2 = len(DF2)

def tokenizer(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    filtered_words = list(filter(lambda token: token not in stopWordList, tokens))
    return filtered_words

my_file = "C:\\Users\\iamlo\\Downloads\\StopWords_Auditor.txt"
with open(my_file ,'r') as stop_words:
    stopWords = stop_words.read().lower()
stopWordList = stopWords.split('\n')
stopWordList[-1:] = []

my_file1 = "C:\\Users\\iamlo\\Downloads\\StopWords_Currencies.txt"
with open(my_file1 ,'r') as stop_words:
    stopWords = stop_words.read().lower()
stopWordList = stopWords.split('\n')
stopWordList[-1:] = []

my_file2 = "C:\\Users\\iamlo\\Downloads\\StopWords_DatesandNumbers.txt"
with open(my_file2 ,'r') as stop_words:
    stopWords = stop_words.read().lower()
stopWordList = stopWords.split('\n')
stopWordList[-1:] = []

my_file3 = "C:\\Users\\iamlo\\Downloads\\StopWords_Generic.txt"
with open(my_file3 ,'r') as stop_words:
    stopWords = stop_words.read().lower()
stopWordList = stopWords.split('\n')
stopWordList[-1:] = []

my_file4 = "C:\\Users\\iamlo\\Downloads\\StopWords_GenericLong.txt"
with open(my_file4 ,'r') as stop_words:
    stopWords = stop_words.read().lower()
stopWordList = stopWords.split('\n')
stopWordList[-1:] = []

my_file5 = "C:\\Users\\iamlo\\Downloads\\StopWords_Geographic.txt"
with open(my_file5 ,'r') as stop_words:
    stopWords = stop_words.read().lower()
stopWordList = stopWords.split('\n')
stopWordList[-1:] = []

my_file6 = "C:\\Users\\iamlo\\Downloads\\StopWords_Names.txt"
with open(my_file6 ,'r') as stop_words:
    stopWords = stop_words.read().lower()
stopWordList = stopWords.split('\n')
stopWordList[-1:] = []

positiveWordsFile = "C:\\Users\\iamlo\\Downloads\\positive-words.txt"
with open(positiveWordsFile,'r') as posfile:
    positivewords=posfile.read().lower()
positiveWordList=positivewords.split('\n')

nagitiveWordsFile = "C:\\Users\\iamlo\\Downloads\\negative-words.txt"
with open(nagitiveWordsFile ,'r') as negfile:
    negativeword=negfile.read().lower()
negativeWordList=negativeword.split('\n')


def text_process(text):
    nopunc = [char for char in text if char not in ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~','*']]
    nopunc=''.join(nopunc)
    txt = ' '.join([word for word in nopunc.split() if word.lower() not in my_file])
    txt1 = ' '.join([word for word in txt.split() if word.lower() not in my_file1])
    txt2 = ' '.join([word for word in txt1.split() if word.lower() not in my_file2])
    txt3 = ' '.join([word for word in txt2.split() if word.lower() not in my_file3])
    txt4 = ' '.join([word for word in txt3.split() if word.lower() not in my_file4])
    txt5 = ' '.join([word for word in txt4.split() if word.lower() not in my_file5])
    return ' '.join([word for word in txt5.split() if word.lower() not in my_file6])

DF3 = text_process(DF2)
l3 = len(DF3)

DF4=tokenizer(DF3)
DF4
l4 = len(DF4)
total_Words_after_cleaning = l4

print("word count(after cleaning)", total_Words_after_cleaning)

def positive_score(text):
    numPosWords = 0
    rawToken = tokenizer(text)
    for word in rawToken:
        if word in positiveWordList:
            numPosWords  += 1
    
    sumPos = numPosWords
    return sumPos

Positive_Score= positive_score(DF3)
print("Positive Score: ", Positive_Score)


def negative_score(text):
    numNegWords=0
    rawToken = tokenizer(text)
    for word in rawToken:
        if word in negativeWordList:
            numNegWords -=1
    sumNeg = numNegWords 
    sumNeg = sumNeg * -1
    return sumNeg

Negative_Score= negative_score(DF3)
print("Negative Score: ", Negative_Score)


def polarity_score(Positive_Score, Negative_Score):
    pol_score = (Positive_Score - Negative_Score) / ((Positive_Score + Negative_Score) + 0.000001)
    return pol_score

Polarity_score = polarity_score(Positive_Score, Negative_Score)
print("Polarity Score",Polarity_score)


def subjactive_score(num1,num2,num3):
    sub_score = (Positive_Score + Negative_Score)/ ((total_Words_after_cleaning) + 0.000001)
    return sub_score

Subjective_Score=subjactive_score(Positive_Score, Negative_Score,total_Words_after_cleaning)
print("Subjective score",Subjective_Score)


no_sent= nltk.sent_tokenize(DF1) 
LS = len(no_sent)


no_words_before= nltk.word_tokenize(DF1) 
LW = len(no_words_before)
print(LW)

Average_Sentence_Length = l2/LS
print("Average Sentence length: ",Average_Sentence_Length)


def complex_word_count(text):
    tokens = tokenizer(text)
    complexWord = 0
    
    for word in tokens:
        vowels=0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w=='a' or w=='e' or w=='i' or w=='o' or w=='u'):
                    vowels += 1
            if(vowels > 2):
                complexWord += 1
    return complexWord

complex_words=complex_word_count(DF1)
print("complex words: ",complex_words)

pc=tokenizer(DF1)
pcl=len(pc)
pcw= complex_words/pcl

print("percentage of complex word", pcw)


def fog_index(averageSentenceLength, percentageComplexWord):
    fogIndex = 0.4 * (averageSentenceLength + percentageComplexWord)
    return fogIndex

Fog_index = fog_index(Average_Sentence_Length,pcw)
print("fog index:", Fog_index )

average_number_of_word_per_sent = LW/LS

print("word per sent: ", average_number_of_word_per_sent)

def syllable_count(text):
    text = text.lower()
    count = 0
    vowels = "aeiouy"
    if text[0] in vowels:
        count += 1
    for index in range(1, len(text)):
        if text[index] in vowels and text[index - 1] not in vowels:
            count += 1
    if text.endswith("e"):
        count -= 1
    if text.endswith("ed"):
        count -= 1
    if text.endswith("es"):
        count -= 1
    if count == 0:
        count += 1
    return count

s = syllable_count(DF1)
ss= s/pcl

print("syllables per word: ",ss )

pronouns=['i','we','my','ours','us','I','WE','MY','OURS']
count=0
for i in DF:
    if i in pronouns:
        count+=1
personal_pronouns = count
print("pro count: ",personal_pronouns)


numb_w=tokenizer(DF1)
num_wl=len(numb_w)
Average_Word_Length= l1/num_wl
#print(num_wl)
#print(l1)
print("Average Word Length : ", Average_Word_Length)


nit = [Positive_Score,Negative_Score,Polarity_score,Subjective_Score,Average_Sentence_Length,pcw,Fog_index,average_number_of_word_per_sent,complex_words,total_Words_after_cleaning,ss,personal_pronouns,Average_Word_Length]
print(nit)
