import pandas as pd
import os
from textblob import TextBlob
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')

def compiler(files):
    #added files by taking away headers from each csv and adding generic header names of Name and Purpose
    #for first file, it will be the base dataframe
    #and then the rest of the files will be appended to the main dataframe
    for i in range(0,len(files)):
        if i == 0:
            pd1 = pd.read_csv(files[0], header=None, skiprows=1,
                              names=["Name", "Purpose"]).iloc[:, -2:]
        else:
            pd2 = pd.read_csv(files[i], header=None, skiprows=1,
                              names=["Name", "Purpose"]).iloc[:, -2:]
            pd1 = pd1.append(pd2, ignore_index=True)
    return(pd1)

def bestworstsentiment(df):
    ##finds best worst sentiment by doing polarity from TextBlob and goes through each of the purposes in main dataframe
    ##and then sort sentiment
    polarity = []
    for index,row in df.iterrows():
        purpose = row['Purpose']
        polaritynum = TextBlob(purpose).sentiment.polarity
        polarity.append(polaritynum)

    polarityseries = pd.Series(polarity)
    df['Sentiment Score']=polarityseries

    sorted = df.sort_values(by=['Sentiment Score'])
    worst = sorted.head(1)
    for i in worst['Purpose']:
        worstpurpose = i
    print("Worst Idea: " + worstpurpose)
    best = sorted.tail(1)
    for i in best['Purpose']:
        bestpurpose = i
    print("Best Idea: " + bestpurpose)

def commonwords(df):
    ##finds common words by doing nltk by doing tokenize and then using FreqDist to find the most frequent
    ##I took off stop words to find more useful frequent words
    listofwords = df['Purpose'].str.cat(sep=" ")
    words = nltk.tokenize.word_tokenize(listofwords)
    lowerwords = [word.lower() for word in words]
    stopwords = nltk.corpus.stopwords.words('english')
    finalwords = [word for word in lowerwords if word not in stopwords]
    freq = nltk.FreqDist(finalwords)
    commonwords=freq.most_common(10)
    print("Most Common Words:")
    [print(word[0]) for word in commonwords]



if __name__ == '__main__':
    files = ['C:/Users/vasu530/Downloads/finalcompanyinfo.csv', 'C:/Users/vasu530/Downloads/scrapes.csv',
             'C:/Users/vasu530/Downloads/RandomCompanyExport.csv', 'C:/Users/vasu530/Downloads/fe595export.csv']
    finaldf = compiler(files)
    print(finaldf)
    bestworstsentiment(finaldf)
    commonwords(finaldf)