from nltk.stem import PorterStemmer
import tokenizer as tok
import json
import numpy as np
import time as tm
import re

STOPWORD_REGEX = "^(a|about|above|after|again|against|all|am|an|and|any|are|aren't|as|at|be|because|been|before|being|below|between|both|but|by|can't|cannot|could|couldn't|did|didn't|do|does|doesn't|doing|don't|down|during|each|few|for|from|further|had|hadn't|has|hasn't|have|haven't|having|he|he'd|he'll|he's|her|here|here's|hers|herself|him|himself|his|how|how's|i|i'd|i'll|i'm|i've|if|in|into|is|isn't|it|it's|its|itself|let's|me|more|most|mustn't|my|myself|no|nor|not|of|off|on|once|only|or|other|ought|our|ours|ourselves|out|over|own|same|shan't|she|she'd|she'll|she's|should|shouldn't|so|some|such|than|that|that's|the|their|theirs|them|themselves|then|there|there's|these|they|they'd|they'll|they're|they've|this|those|through|to|too|under|until|up|very|was|wasn't|we|we'd|we'll|we're|we've|were|weren't|what|what's|when|when's|where|where's|which|while|who|who's|whom|why|why's|with|won't|would|wouldn't|you|you'd|you'll|you're|you've|your|yours|yourself|yourselves)$"

DO_NOT_STEM = ['acm', 'ics', 'cs', 'eppstein', 'game', 'pattis', 'school', 'information', 'bren', 
                'thornton', 'management', 'retrieval', 'science', 'videra', 'david', 'science', 
                'learning', 'lopes', 'vision', 'donald', 'computer', 'structures', 'alex', 'undergraduate', 
                'data', 'kay', 'business', 'cristina', 'degree', 'human', 'engineering', 'richard', 'graduate', 
                'software', 'interaction', 'machine', 'undergrad', 'grad', 'artificial', 'intelligence', 'statistical', 
                'science', 'cs', '121', 'intelligent', 'systems', 'general', 'and', 'software', 'visual', 'computing', 
                'embedded', 'networked']

GRAMS_2 = ['machine learning', 'computer science', 'information retrieval', 'software engineering', 'data science', 
            'data structures', 'computer vision', 'undergraduate degree', 'undergrad degree', 'graduate degree', 'grad degree', 'richard pattis', 'david eppstein', 
            'david kay', 'alex thornton', 'cristina lopes', 'donald bren', 'artifical intelligence', 'statistical science', 'cs 121', 'intelligent systems', 
            'visual computing', 'embedded systems', 'networked systems']

GRAMS_3 = ['cristina videra lopes', 'human computer interaction', 'business information management', 'computer game science', 
        'donald bren school', 'general computer science', 'systems and software']

CACHE = [ 'cs', 'uci', 'of', 'to', 'be', 'or', 'not', 'computer science', 'machine learning', 'ics', 'software engineering', 'cristina lopes', 
            'human computer interaction', 'computer game science', 'acm']


#INDEX_FILE_DICT = dict()
#SEEK_DICT = dict()

def openIndex():
    ''' open all the indices organized by letter
    '''
    INDEX_FILE_DICT = dict()    
     
    for letter in "abcdefghijklmnopqrstuvwxyz0123456789":
        INDEX_FILE_DICT[letter] = open('splitIndex/' + letter, 'r')

    return INDEX_FILE_DICT


def openSeekDict():
    ''' open a dictionary with the position to seek each token line in the 
        index files
    '''
    seekfile = open('seekdict', 'r')
    SEEK_DICT = json.loads(seekfile.readline())
    SEEK_DICT = dict(SEEK_DICT)

    seekfile.close()
    return SEEK_DICT


def closeFiles(INDEX_FILE_DICT):
    ''' close all the indices organized by letter
    '''
    for letter in "abcdefghijklmnopqrstuvwxyz0123456789":
        INDEX_FILE_DICT[letter].close()


def loadCache(INDEX_FILE_DICT, SEEK_DICT, tokinfodict):
    ''' cache common or slow queries ahead of time
    '''
    for tok in CACHE:
        tokinfodict[tok] = getTokenStatsFromIndex(INDEX_FILE_DICT, SEEK_DICT, tok)




def getTokenStatsFromIndex(INDEX_FILE_DICT, SEEK_DICT, token: str):
    # get first letter of token
    letter = token[0]

    # get position in letter index from seek dictionary
    position = int(SEEK_DICT[token])

    # seek the position within the file
    #INDEX_FILE_DICT[letter].seek(0)
    INDEX_FILE_DICT[letter].seek(position)

    # read in the line containing the token
    tokline = INDEX_FILE_DICT[letter].readline()

    # evaluate the token into something usable by the program
    info = eval(tokline.split("=")[1])

    return info




def removeStopWordsAndStem(tokens:list(), numTokens:list()):
    ''' removes the stopwords from the query if they dont remove over 40% of the query
        tokens
        stems the tokens
        keeps the n-grams within a query as a single toke
    '''
    stemmedTok = []
    shortTok = []
    numToksWoStop = 0
    num = 0

    i = 0
    ps = PorterStemmer()

    while i  < numTokens:
        has2gram = False
        has3gram = False
        if re.match(r"{}".format(STOPWORD_REGEX), tokens[i]):
            stemmedTok.append(ps.stem(tokens[i]))
            i += 1

        elif tokens[i] in DO_NOT_STEM:
            # check if its 
            # keep 2 grams as a single token
            if i+1 < numTokens:
                gram2 = tokens[i] + ' ' + tokens[i+1]
                if gram2 in GRAMS_2:
                    stemmedTok.append(gram2)
                    shortTok.append(gram2)
                    i += 2
                    has2gram = True
                    numToksWoStop += 2
                    num +=1

            # keep 3 grams as a single token
            if i+2 < numTokens and not has2gram:
                gram3 = tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2]
                if gram3 in GRAMS_3:
                    stemmedTok.append(gram3)
                    shortTok.append(gram3)
                    i += 3
                    has3gram = True
                    numToksWoStop += 3
                    num += 1

            # keep non-stemmed words, unstemmed
            if not has2gram and not has3gram:
                stemmedTok.append(tokens[i])
                shortTok.append(tokens[i])
                i += 1

                numToksWoStop += 1
                num += 1

        else:
            shortTok.append(ps.stem(tokens[i]))
            stemmedTok.append(ps.stem(tokens[i]))

            numToksWoStop += 1
            num += 1
            i += 1

    if numTokens ==  0:
        return list(), 0

    #print(((numTokens - numToksWoStop) / numTokens))
    if ((numTokens - numToksWoStop) / numTokens) > 0.4:
        return stemmedTok, numTokens
    else:
        return shortTok, num




            


def main(INDEX_FILE_DICT, SEEK_DICT, DOC_INDEX, tokinfodict, query):
    
    # start the timer
    t1 = tm.perf_counter()

    # get the tokens
    tokens = tok.getTokens(query)
    numTokens = len(tokens)
    # filter/modify tokens
    tokens,numTokens = removeStopWordsAndStem(tokens, numTokens)

    result = list()
    if numTokens == 0:
        t2 = tm.perf_counter()
        return list(), t2-t1

    print(tokens)
    scoreToks = []
    
    # get the tokens and cache the info
    for t in tokens:
        try:
            tokinfodict[t]
            scoreToks.append(t)
            
        except KeyError:
            try:
                tokinfodict[t] = getTokenStatsFromIndex(INDEX_FILE_DICT,SEEK_DICT,t)
                scoreToks.append(t)
            except KeyError:
                continue

        docs = list()

        try:                
            docs.extend( list(set(tokinfodict[t]['doclist']) ))

        except IOError:
            break

        result.append(set(docs))

    # if no results i.e. token doesnt exist
    # return no results
    if len(result) == 0:
        t2 = tm.perf_counter()
        return [], t2-t1

    # use tfidf if there is only one token to rank documents
    elif numTokens == 1:
        output = result[0]
        if len(result) > 1:
            for i in range(1, len(result)):
                output = output.intersection(result[i])

        output = list(output)
        scores = [1]*len(output)

        for t in scoreToks:
            letter = t[0]
            scoretype = 1

            if t in GRAMS_2 or t in GRAMS_3:
                scoretype = 0
            
            for i in range(len(output)):
                doc = output[i]
                #print(doc)
                try:
                    score = tokinfodict[t][doc][scoretype]
                except KeyError:
                    score = 0
                scores[i] += score
            
        scorearr = np.array(scores)


    # DO COSINE SIMILARITY IF MORE THAN ONE TOKEN
    else:
       
        docs = []
        for i in range(len(result)):
            docs += result[i]
        documents = np.unique(np.array(docs))
        print(documents)

        tokens,cts = np.unique(np.array(tokens), return_counts=True)
        qtfidf = np.log(cts)
        qtfidf += 1

        # create empty matrices
        num = np.zeros((len(tokens), documents.shape[0]))
        denom = np.zeros((len(tokens), documents.shape[0]))

        df = np.zeros(tokens.shape)
        print(tokens.shape)
        for i in range(len(tokens)):
            df[i] = tokinfodict[tokens[i]]['total']

        qtfidf = np.divide(qtfidf, df)

        # create the cosine similarity matrices from the scores
        for ti in range(len(tokens)):
            for di in range(len(documents)):
                try:
                    num[ti][di] = tokinfodict[tokens[ti]][docs[di]][1]
                    denom[ti][di] = tokinfodict[tokens[ti]][docs[di]][1]

                except KeyError:
                    pass

        # compute the cosine similarity from the matrices
        num = num * qtfidf[:,None]
        num = np.sum(num, axis=0)

        denom = np.square(denom)
        denom = np.multiply(np.sqrt(np.sum(denom, axis=0)), np.sqrt(np.sum(np.square(qtfidf))))

        scorearr = num / denom
        docs = documents

    # rank the documents by score
    topscores = scorearr.argsort()[::-1]

    t2 = tm.perf_counter()

    print("Outputting result...")
    count = 0
    seenFaculty = False

    urls = []

    print(np.max(scorearr))
    topUrl = []
    for ind in topscores:
        doc = docs[ind]

        if count == 10:
            break

        url = DOC_INDEX[doc][1].split("#")[0]
        if url in urls:
            continue
        urls.append(url)

        # display the top 10 queries
        if "faculty/area" in DOC_INDEX[doc][1]:
            if seenFaculty:
                continue
            else:
                seenFaculty = True
        topUrl.append(url)
        print(DOC_INDEX[doc][1], end='\n')
        count += 1

    # get time to result
    time = t2-t1

    return topUrl, time


if __name__ == "__main__":
    main()




