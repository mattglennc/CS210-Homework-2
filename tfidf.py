import re
from collections import Counter
from collections import defaultdict
import math

def stemming(word):
    res1 = re.search('(.*)ly$',word)
    if (res1):
        return word[:len(word)-2]
    res2 = re.search('(.*)ing$',word)
    if (res2):
        return word[:len(word)-3]
    res3 = re.search('(.*)ment$',word)
    if (res3):
        return word[:len(word)-4]
    return word

def uniqueWords(f):
    words=[]
    numWords = 0
    wordOccs = defaultdict(list)
    for line in open(f.strip('\n')):
        for line2 in open("preproc_" + line.strip('\n')):
            getLine = line2.split(' ')
            for w in getLine:
                if(line.strip('\n') not in wordOccs[w]):
                    wordOccs[w].append(line.strip('\n'))
                if w not in words:
                    words.append(w)
    return words,wordOccs

def listFiles(f):
    for line in open(f):
        fileName = line.strip('\n')
        preproc(fileName)
    numFiles = 0
    uniqWords,wordsPerFile = uniqueWords(f)
    for line in open(f):
        numFiles+=1
    idfDict = idf(f,uniqWords,numFiles,wordsPerFile)
    for line in open(f):
        fileName = line.strip('\n')
        tfDict = tf(fileName)
        tfidAll = tfidf(tfDict,idfDict)
        top5(fileName,tfidAll)
    

def preproc(f):   
    stopwords = []
    for line in open('stopwords.txt'):
        stopwords.append(line.strip('\n'))
    output = ''
    sentence = []
    for line in open(f,encoding="utf8"):   # read one line at a time
        getLine = line.split(' ')
        getLine = [''.join(c for c in word if c.isalnum() or c == '_').lower() for word in getLine if len(word) > 0 and 'http' not in word]
        getLine = [word for word in getLine if word not in stopwords]
        getLine = [stemming(word) for word in getLine]
        sentence.extend(getLine)
    output=' '.join(sentence)
    outfile = open('preproc_' + f,'w',)
    outfile.write(output)
    outfile.close()
    
def tf(f):
    wordCounts = Counter()
    numWords = 0
    for line in open("preproc_" + f):
        getLine = line.split(' ')
        numWords += len(getLine)
        wordCounts.update([word.strip() for word in getLine])
    wordCounts=dict(sorted(wordCounts.items(), key=lambda wc:wc[1], reverse=True))
    tfDict = {}
    for word, num in wordCounts.items():
        tfDict[word] = (num/numWords)

    return tfDict
    
def idf(f,uniqWords,numFiles,wordsPerFile):
    occurenceDict={}
    for word, files in wordsPerFile.items():
        occurenceDict[word] = len(files)
    idfDict={}
    for word, occ in occurenceDict.items():
        idfDict[word]=(math.log(numFiles/occ) + 1)
    return idfDict

def tfidf(tfDict,idfDict):
    tfidfAll = {}
    for word, tf in tfDict.items():
        tfidfAll[word] = (round(idfDict[word]*float(tf),2))
    return tfidfAll

        
def top5(f,tfidfAll):
        outfile = open("tfidf_" + f.strip('\n'),'w')
        tfidfDict = defaultdict(list)
        for word, tfidf in tfidfAll.items():
                tfidfDict[tfidf].append(word)
        for words in tfidfDict.values():
                words.sort()
        lastList = []
        top = 0
        tfidfDict = dict(sorted(tfidfDict.items(), key=lambda x:x[0], reverse=True))
        for tfidf,words in tfidfDict.items():
            for word in words:
                if(top==5):
                    break
                lastList.append((word,tfidf))
                top+=1
        print(lastList)
        outfile.write(str(lastList))
        outfile.close()
                
                
        
        
        
        
def main():
    listFiles('tfidf_docs.txt')
main()
    
    