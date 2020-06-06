# tokenizer.py


import re


# handles 'U.S.A.' and 'USA'
def handleAcronym(s: str) -> str:
    ''' Handles strings that contain acronyms
    '''
    newS = ""

    # if length contains "."
    if "." not in s:
        return s

    # if length is 0, return empty str
    if len(s) == 0:
        return newS

    # if last char is '.' do not include it
    if s[-1] == '.':
        s = s[0:-1]

    # Normalize acronyms
    for i in range(len(s) - 1):
        if s[i] == '.' and s[i + 1].isalpha():
            newS += s[i + 1]
        else:
            newS += s[i]
    if len(s) > 0:
        newS += s[-1]

    return newS


def normalizePeriod(rawTok: [str]) -> [str]:
    ''' Normalizes acronyms for all tokens in a file
    '''
    normalized = []

    for t in rawTok:
        normalized.append(handleAcronym(t))
    return normalized


def removeURL(rawTok: [str]) -> [str]:
    ''' Gets raw tokens split by whitespace without URLs but still containing
        symbols
    '''
    noUrlTok = []
    # split by '(http'
    for t1 in rawTok:
        noHttp = t1.split('http')
        for t2 in noHttp:
            try:
                # if it contains '://' in the first s[0:4] its a link
                # and discard it
                if '://' in t2[0:4]:
                    pass
                else:
                    noUrlTok.append(t2)
            except IndexError:
                noUrlTok.append(t2)
    return noUrlTok


def splitBySymbol(rawTok: [str]) -> [str]:
    ''' splits each raw token by any remaining symbols
    '''
    noSym = []
    for t1 in rawTok:
        # regex from https://stackoverflow.com/questions/336210/regular-expression-for-alphanumeric-and-underscores
        toks = re.split("[^a-zA-Z0-9]", t1.lower(), flags=re.IGNORECASE)
        for t2 in toks:
            if t2 != "":
                noSym.append(t2)
    return noSym


def getTokens(plainContent: str) -> str:
    ''' combines above functions to get fully processed tokens
        does not remove stop words
    '''

    if plainContent is None or plainContent == '':
        return None

    # split by whitespace
    # https://stackoverflow.com/questions/8113782/split-string-on-whitespace-in-python
    noWS = re.split('\s+', plainContent)

    # remove any URLs from raw tokens
    noUrl = removeURL(noWS)

    # normalize any acronyms
    norm = normalizePeriod(noUrl)

    # add in porter stemmer

    # split raw tokens by symbol
    noSym = splitBySymbol(norm)

    return noSym

























    
