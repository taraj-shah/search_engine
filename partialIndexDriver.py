import json
import html2text
import indexer as ind
import tokenizer as tok
from bs4 import BeautifulSoup
import re

# can be changed - idk if it should be a global var
DEVPATH = "DEV"

# DOCID increment with each document


DOCINDEX = dict()
INDEX = dict()


def main():
    # user_query = input()
    DOCID = 0
    INDEX = dict()

    numPartial = 1

    INDEX = dict()

    filtfiles = open("validDocs2", "r")

    uniqueTokens = list()

    for ln in filtfiles.readlines():

        fname = ln.strip()

        if DOCID % 12000 == 0 and DOCID != 0:
            for i in INDEX:
                '''
                print('partialIndex/' + str(numPartial) + '_' + str(i))
                file = open('partialIndex/' + str(numPartial) + '_' + str(i), 'w')
                file.write(str(INDEX[i]))
                file.close()
                '''
                uniqueTokens.extend(list(INDEX[i].keys()))
                json.dump(INDEX[i], open('partialIndex/' + str(numPartial) + '_' + str(i), 'w'))

            numPartial += 1

        # Increment the DOCID
        DOCID += 1

        # print the full file path
        print(fname)

        # parse json, tokenize the body
        h2t = html2text.HTML2Text()

        # open single webpage file
        file = open(fname)

        # JSON dict contains: 'url', 'content', 'encoding'
        pageDict = json.loads(file.read())

        # close file to get memory back
        file.close()

        # get html formatted content
        htmlContent = pageDict['content']

        soup = BeautifulSoup(htmlContent, 'html.parser')
        titles = ''
        bolds = ''
        h1 = ''
        h2 = ''
        h3 = ''
        if soup.title is not None:
            titles = soup.title.string
        for tag in soup.find_all("b"):
            if tag.string is not None and bolds is not None:
                bolds += (" " + tag.string)
        for tag in soup.find_all("h1"):
            if tag.string is not None and h1 is not None:
                h1 += (" " + tag.string)
        for tag in soup.find_all("h2"):
            if tag.string is not None and h2 is not None:
                h2 += (" " + tag.string)
        for tag in soup.find_all("h3"):
            if tag.string is not None and h3 is not None:
                h3 += (" " + tag.string)


        # get plain text content
        plainContent = h2t.handle(htmlContent)

        # get tokens in order of appearance
        tokens = tok.getTokens(plainContent)

        imp_words = dict()
        imp_words['titles_tokens'] = tok.getTokens(titles)
        imp_words['bolds_tokens'] = tok.getTokens(bolds)
        imp_words['h1_tokens'] = tok.getTokens(h1)
        imp_words['h2_tokens'] = tok.getTokens(h2)
        imp_words['h3_tokens'] = tok.getTokens(h3)
        #print('imp_words = ', imp_words)

        # Index the tokens
        ind.indexTokens(tokens, imp_words, DOCID, INDEX)

        DOCINDEX[DOCID] = (fname, pageDict['url'])

    for i in INDEX:
        '''
        file = open('partialIndex/' + str(numPartial) + '_' + str(i), 'w')
        file.write(str(INDEX[i]))
        file.close()
        '''
        json.dump(INDEX[i], open('partialIndex/' + str(numPartial) + '_' + str(i), 'w'))

    json.dump(DOCINDEX, open('docindex', 'w'))

    # Print Final Statistics
    print("Number of Documents:     {}".format(DOCID))

    print("Number of Unique Tokens: {}".format(len(set(uniqueTokens))))


if __name__ == "__main__":
    main()
