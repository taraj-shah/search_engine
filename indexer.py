# indexer.py

from nltk.stem import PorterStemmer
import json


# from nltk.tokenize import sent_tokenize, word_tokenize

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


def indexTokens(tokens: [str], imp_words: dict, docid: int, index: dict(dict(dict()))) -> None:
    '''
    Indexes the tokens into an inverted index based on their id
    '''

    # create porter stemmer object
    ps = PorterStemmer()

    position = 0

    docid = str(docid)

    numtoks = len(tokens)
    tokind = 0


    for tok in tokens:
        # get the stem of the token
        has2gram = False
        has3gram = False
        gram2 = None
        gram3 = None
        if tok not in DO_NOT_STEM:
            tok = ps.stem(tok)

        letter = tok[0]

        if tokind + 1 < numtoks:
            gram2 = tokens[tokind] + ' ' + tokens[tokind + 1]
            if gram2 in GRAMS_2:
                has2gram = True
                try:
                    letterDict = index[letter]
                except KeyError:
                    # create the dictionary corresponding to certain letter
                    index[letter] = dict()

                # create the token dictionary if not already created
                try:
                    tokenDict = index[letter][gram2]
                except KeyError:
                    # create dictionary corresponding to certain token
                    index[letter][gram2] = dict()

                # create the list to store the token positions within that document
                # if it doesn't already exist
                try:
                    docPositionDict = index[letter][gram2][docid]
                except KeyError:
                    # create list corresponding to positions within certain document for that token
                    index[letter][gram2][docid] = [list(), 0, 0, 0, 0, 0]
                index[letter][gram2][docid][0].append(position)
                print(index[letter][gram2][docid])

        if tokind + 2 < numtoks:
            gram3 = tokens[tokind] + ' ' + tokens[tokind + 1] + ' ' + tokens[tokind + 2]
            if gram3 in GRAMS_3:
                has3gram = True
                try:
                    letterDict = index[letter]
                except KeyError:
                    # create the dictionary corresponding to certain letter
                    index[letter] = dict()

                # create the token dictionary if not already created
                try:
                    tokenDict = index[letter][gram3]
                except KeyError:
                    # create dictionary corresponding to certain token
                    index[letter][gram3] = dict()

                # create the list to store the token positions within that document
                # if it doesn't already exist
                try:
                    docPositionDict = index[letter][gram3][docid]
                except KeyError:
                    # create list corresponding to positions within certain document for that token
                    index[letter][gram3][docid] = [list(), 0, 0, 0, 0, 0]

                index[letter][gram3][docid][0].append(position)
                print(index[letter][gram3][docid])

        tokind += 1
        # ENSURE ALL NECESSARY DICTIONARIES EXIST IN LAYERED DICTIONARY
        # IF THEY DO NOT EXIST, CREATE THEM

        # create the letter dictionary if not already created
        try:
            letterDict = index[letter]
        except KeyError:
            # create the dictionary corresponding to certain letter
            index[letter] = dict()

        # create the token dictionary if not already created
        try:
            tokenDict = index[letter][tok]
        except KeyError:
            # create dictionary corresponding to certain token
            index[letter][tok] = dict()

        # create the list to store the token positions within that document
        # if it doesn't already exist
        try:
            docPositionDict = index[letter][tok][docid]
        except KeyError:
            # create list corresponding to positions within certain document for that token
            index[letter][tok][docid] = [list(), 0, 0, 0, 0, 0]

        # add the position to the dictionary
        # EX:
        #       token is "hello" at position 3
        #       letter is 'h'
        #       docid is 12
        #       this entry would be in the H letter dictionary
        #       within the H letter dictionary we would key for the token "hello"
        #       we add position 3 to the list of positions corresponding to 
        #       hello for this document
        index[letter][tok][docid][0].append(position)

        # if imp_words['titles_tokens'] is not None and tok in imp_words['titles_tokens']:
        #     index[letter][tok][docid][1] = 1
        # if imp_words['h1_tokens'] is not None and tok in imp_words['headers_tokens']:
        #     index[letter][tok][docid][2] = 1
        # if imp_words['bolds_tokens'] is not None and tok in imp_words['bolds_tokens']:
        #     index[letter][tok][docid][3] = 1

        i = 1


        keys = list(imp_words.keys())
        for key in keys:

            if imp_words[key] is not None:
                for word in imp_words[key]:
                    if word not in DO_NOT_STEM:
                        word = ps.stem(word)
                    if word == tok:
                        index[letter][tok][docid][i] = 1

        # if tok in imp_words['titles_tokens']:
        #     index[letter][tok][docid][1] = 1
        # if tok in imp_words['h1_tokens']:
        #     index[letter][tok][docid][2] = 1
        # if tok in imp_words['h2_tokens']:
        #     index[letter][tok][docid][3] = 1
        # if tok in imp_words['h3_tokens']:
        #     index[letter][tok][docid][4] = 1
        # if tok in imp_words['bolds_tokens']:
        #     index[letter][tok][docid][5] = 1


        # increment the position
        position += 1

    print(docid)


def mergeIndex(partialIndexPath: str, fullIndexPath: str, numPartials: int):
    for char in "abcdefghijklmnopqrstuvwxyz0123456789":
        charDict = dict()
        for i in range(numPartials):

            print("Merging all indexes that start with character {} . . .".format(char))

            # open and read partial index file
            try:
                filename = "{}{}_{}".format(partialIndexPath, i + 1, char)
                partialFile = open(filename, 'r')

                # create partial dictionary from key
                dct = json.loads(partialFile.readline())

                partialFile.close()

                # if first iteration, just set the dictionary
                if i == 0:
                    charDict = dct

                # otherwise, append to the dictionary
                else:
                    for token in dct.keys():
                        # ensure token exists in character dictionary
                        try:
                            _ = charDict[token]
                        except KeyError:
                            charDict[token] = dict()

                        for docid in dct[token].keys():
                            docid = str(docid)
                            # ensure document exists in token dictionary
                            try:
                                _ = charDict[token][docid]
                            except KeyError:
                                charDict[token][docid] = [list(), 0, 0, 0, 0, 0]

                            # add position list to the dictionary
                            charDict[token][docid][0].extend(dct[token][docid][0])

                            for i in range(1, 5):
                                if dct[token][docid][i] == 1:
                                    charDict[token][docid][i] = 1

            except FileNotFoundError:
                pass

        # write the full index to the file
        json.dump(charDict, open(fullIndexPath + char, 'w'))


def splitIndex(scoredIndexPath: str, fullIndexPath: str):
    SEEKDICT = dict()

    for firstlet in "abcdefghijklmnopqrstuvwxyz0123456789":

        # open the first letter file for reading
        file = open(scoredIndexPath + firstlet, 'r')
        letterDict = json.loads(file.readline())
        file.close()

        startLine = 0
        outFile = open("{}{}".format(fullIndexPath, firstlet), 'a')
        for key in letterDict.keys():
            tokenInfo = "{}={}\n".format(key, letterDict[key])
            # tokeninfo = str()
            outFile.write(tokenInfo)
            SEEKDICT[key] = str(startLine)
            startLine += len(tokenInfo)

        outFile.close()

    json.dump(SEEKDICT, open('seekdict', 'w'))

    # json.dump(splitDict[key], open(fullIndexPath + firstLet))
