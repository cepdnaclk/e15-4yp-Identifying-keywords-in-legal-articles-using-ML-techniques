#import preprocess as pre

def computeTF(wordDict,bow):
    '''Computing TF(Term Frequency of the vocab) '''
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict


def computeIDF(doclist):
    '''Computing IDF for the vocab '''
    import math 
    count = 0
    idfDict = {}
    for element in doclist:
        for j in element:
            count+=1
    N = count

    # count no of documents that contain the word w
    idfDict = dict.fromkeys(doclist[0].keys(),0)

    for doc in doclist:
        for word,val in doc.items():
            if val>0:
                idfDict[word]+= 1

    # divide N by denominator above
    for word,val in idfDict.items():
        if val == 0:
            idfDict[word] = 0.0
        else:
            idfDict[word] = math.log(N / float(val))

    return idfDict

def computeTfidf(tf,idf):
    '''Computing TF-IDF for the words in text '''
    tfidf = {}
    sorted_list = []
    for word , val in tf.items():
        tfidf[word] = val * idf[word]

    ranking_list  = sorted(tfidf.items(),reverse=True, key = lambda kv:(kv[1], kv[0]))[:5]
    for i, _ in ranking_list:
        sorted_list.append(i)

    return sorted_list

# vocab_dict , arr = textProcessing(given_text)
# tf = computeTF(vocab_dict,arr)
# idf = computeIDF([vocab_dict])
# tfidf = computeTfidf(tf,idf)

# print(tfidf)

'''
file = open("myfile.txt", "rt")
data = file.read()
vocab_dict , arr = textProcessing(data)
tf = computeTF(vocab_dict,arr)
idf = computeIDF([vocab_dict])
tfidf = computeTfidf(tf,idf)

print(tfidf)'''