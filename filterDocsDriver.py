import re
from simhash import Simhash, SimhashIndex
import os
import json
import html2text


# taken from https://leons.im/posts/a-python-implementation-of-simhash-algorithm/
def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]



# can be changed - idk if it should be a global var
DEVPATH = "DEV"

# DOCID increment with each document


DOCINDEX = dict()
INDEX = dict()


def main():
    # user_query = input()
    DOCID = 0


    numPartial = 1 

    index = SimhashIndex([])

    totaldocs = 0
    docnum = 0

    validDocFile = open('validDocs2', 'w')

    for root, dirs, files in os.walk(DEVPATH):
        for fname in files:
            if not fname.endswith(".json"):
                continue
            totaldocs += 1
            h2t = html2text.HTML2Text()

            file = open(root + "/" + fname)

            pageDict = json.loads(file.read())

            # close file to get memory back
            file.close()

            # get html formated content
            htmlContent = pageDict['content']

            print(pageDict['url'])

            plainContent = h2t.handle(htmlContent)

            feat = get_features(plainContent)

            sim = Simhash(feat)

            if len(index.get_near_dups(sim)) > 0:
                continue

            print(docnum, totaldocs)

            index.add(str(docnum), sim)

            validDocFile.write(root + "/" + fname + "\n")

            docnum+=1


    validDocFile.close()


if __name__ == "__main__":
    main()


